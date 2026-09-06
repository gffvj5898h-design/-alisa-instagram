#!/usr/bin/env python3
"""Import one or more binary assets from text-only queue manifests.

Each manifest is an independent job. A broken manifest may create a rejection
receipt but never prevents later manifests from being attempted.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import ipaddress
import json
import os
import re
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "production" / "import-queue"
RECEIPTS = ROOT / "production" / "import-receipts"
REJECTED = ROOT / "production" / "import-rejected"
MAX_GITHUB_BYTES = 95 * 1024 * 1024
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def fail(msg: str) -> None:
    raise RuntimeError(msg)


def safe_target(raw: str) -> Path:
    if not raw or raw.startswith("/") or ".." in Path(raw).parts:
        fail("unsafe target_path")
    target = (ROOT / raw).resolve()
    try:
        rel = target.relative_to(ROOT)
    except ValueError:
        fail("target_path escapes repository root")
    if not rel.as_posix().startswith("content/"):
        fail("binary import target must live under content/")
    if target.suffix.lower() not in ALLOWED_EXT:
        fail(f"unsupported target extension: {target.suffix}")
    return target


def assert_public_https(url: str) -> None:
    p = urlparse(url)
    if p.scheme != "https" or not p.hostname:
        fail("source_url must be https")
    for info in socket.getaddrinfo(p.hostname, p.port or 443, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            fail(f"non-public source address: {ip}")


def download_url(url: str, limit: int) -> bytes:
    assert_public_https(url)
    req = Request(url, headers={"User-Agent": "alisa-instagram-asset-import/2.0"})
    chunks: list[bytes] = []
    total = 0
    with urlopen(req, timeout=60) as response:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > limit:
                fail("asset too large")
            chunks.append(chunk)
    return b"".join(chunks)


def decode_base64(value: str, limit: int) -> bytes:
    if value.startswith("data:"):
        value = value.split(",", 1)[1]
    try:
        data = base64.b64decode(value, validate=True)
    except Exception as exc:
        fail(f"invalid base64: {exc}")
    if len(data) > limit:
        fail("base64 asset too large")
    return data


def decode_base64_chunks(paths: object, limit: int) -> bytes:
    if not isinstance(paths, list) or not paths:
        fail("base64_chunks must be a non-empty list")
    parts: list[str] = []
    for raw in paths:
        p = (ROOT / str(raw)).resolve()
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            fail("chunk path escapes repository root")
        if not rel.as_posix().startswith("production/import-queue/chunks/"):
            fail("chunks must live under production/import-queue/chunks/")
        if not p.is_file():
            fail(f"missing chunk: {rel}")
        parts.append(p.read_text(encoding="utf-8").strip())
    return decode_base64("".join(parts), limit)


def validate_magic(data: bytes, suffix: str) -> None:
    if len(data) < 12:
        fail("asset too small")
    s = suffix.lower()
    ok = (
        (s in {".jpg", ".jpeg"} and data.startswith(b"\xff\xd8\xff"))
        or (s == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n"))
        or (s == ".webp" and data.startswith(b"RIFF") and data[8:12] == b"WEBP")
        or (s in {".mp4", ".mov"} and data[4:8] == b"ftyp")
    )
    if not ok:
        fail(f"signature mismatch for {suffix}")


def validate_image_decode(data: bytes, suffix: str) -> tuple[int, int] | None:
    if suffix.lower() not in IMAGE_EXT:
        return None
    if suffix.lower() in {".jpg", ".jpeg"} and not data.endswith(b"\xff\xd9"):
        fail("truncated JPEG: EOI marker missing")
    try:
        from PIL import Image
    except Exception as exc:
        fail(f"Pillow required for image integrity validation: {exc}")
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            if image.width <= 0 or image.height <= 0:
                fail("invalid image dimensions")
            return image.width, image.height
    except Exception as exc:
        fail(f"image decode failed: {type(exc).__name__}: {exc}")


def source_label(obj: dict) -> str:
    if obj.get("source_url"):
        p = urlparse(obj["source_url"])
        return f"https://{p.hostname}{p.path} (query omitted)"
    if obj.get("base64_chunks"):
        return "repository base64 chunks"
    return "embedded base64 payload"


def redact_error(value: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(0)
        p = urlparse(raw)
        if p.scheme == "https" and p.hostname:
            return f"https://{p.hostname}{p.path} (query omitted)"
        return "[url omitted]"
    return re.sub(r"https://[^\s'\"]+", repl, value)


def write_rejection(manifest: Path, exc: Exception) -> None:
    REJECTED.mkdir(parents=True, exist_ok=True)
    path = REJECTED / f"{manifest.stem}.md"
    path.write_text(
        "# Binary import rejection\n\n"
        f"- Manifest: `{manifest.relative_to(ROOT)}`\n"
        f"- Error: `{type(exc).__name__}: {redact_error(str(exc))}`\n"
        f"- Rejected UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n",
        encoding="utf-8",
    )


def process(manifest: Path) -> bool:
    receipt = RECEIPTS / f"{manifest.stem}.md"
    if receipt.exists():
        print(f"SKIP {manifest.name}: receipt exists")
        return False
    if not manifest.is_file():
        fail(f"manifest not found: {manifest}")

    obj = json.loads(manifest.read_text(encoding="utf-8"))
    target = safe_target(str(obj.get("target_path", "")))
    replace = bool(obj.get("replace", False))
    limit = min(max(int(obj.get("max_bytes", MAX_GITHUB_BYTES)), 1), MAX_GITHUB_BYTES)
    if target.exists() and not replace:
        fail(f"target exists: {target.relative_to(ROOT)}")

    modes = sum(bool(obj.get(k)) for k in ("source_url", "base64", "base64_chunks"))
    if modes != 1:
        fail("manifest must contain exactly one of source_url, base64, base64_chunks")
    if obj.get("source_url"):
        data = download_url(obj["source_url"], limit)
    elif obj.get("base64"):
        data = decode_base64(obj["base64"], limit)
    else:
        data = decode_base64_chunks(obj["base64_chunks"], limit)

    validate_magic(data, target.suffix)
    dimensions = validate_image_decode(data, target.suffix)
    sha = hashlib.sha256(data).hexdigest()
    expected = str(obj.get("expected_sha256", "")).strip().lower()
    if expected and expected != sha:
        fail(f"SHA-256 mismatch: expected {expected}, got {sha}")

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, target)

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Binary import receipt", "",
        f"- Manifest: `{manifest.relative_to(ROOT)}`",
        f"- Target: `{target.relative_to(ROOT)}`",
        f"- Bytes: {len(data)}",
        f"- SHA-256: `{sha}`",
        f"- Source: {source_label(obj)}",
        f"- Imported UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- Replace allowed: `{replace}`",
    ]
    if dimensions:
        lines.append(f"- Dimensions: {dimensions[0]}×{dimensions[1]}")
    receipt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"IMPORTED {target.relative_to(ROOT)} bytes={len(data)} sha256={sha}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--write-rejection", action="store_true")
    ns = ap.parse_args()

    if ns.all and ns.manifest:
        print("choose manifest or --all, not both", file=sys.stderr)
        return 2
    manifests = sorted(QUEUE.glob("*.json")) if ns.all else ([ROOT / Path(ns.manifest)] if ns.manifest else [])
    if not manifests:
        print("No pending manifests")
        return 0

    failures = 0
    for manifest in manifests:
        try:
            process(manifest)
        except Exception as exc:
            failures += 1
            print(f"ERROR {manifest}: {redact_error(str(exc))}", file=sys.stderr)
            if ns.write_rejection:
                write_rejection(manifest, exc)
            continue
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
