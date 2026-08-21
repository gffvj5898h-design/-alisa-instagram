#!/usr/bin/env python3
"""Import binary assets into the repository from text-only queue manifests.

Grok can create UTF-8 JSON manifests under production/import-queue/. GitHub Actions
runs this script, downloads the binary, validates basic safety/integrity, writes it
under content/, and records a receipt with SHA-256.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "production" / "import-queue"
RECEIPTS = ROOT / "production" / "import-receipts"
MAX_GITHUB_BYTES = 95 * 1024 * 1024
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}


def fail(msg: str) -> None:
    raise RuntimeError(msg)


def safe_target(raw: str) -> Path:
    if not raw or raw.startswith("/"):
        fail("target_path must be a relative repository path")
    target = (ROOT / raw).resolve()
    try:
        rel = target.relative_to(ROOT)
    except ValueError:
        fail("target_path escapes repository root")
    if ".." in Path(raw).parts:
        fail("target_path may not contain '..'")
    if not str(rel).startswith("content/"):
        fail("binary import target must live under content/")
    if target.suffix.lower() not in ALLOWED_EXT:
        fail(f"unsupported target extension: {target.suffix}")
    return target


def assert_public_https(url: str) -> None:
    p = urlparse(url)
    if p.scheme != "https" or not p.hostname:
        fail("source_url must be an https URL")
    host = p.hostname
    try:
        infos = socket.getaddrinfo(host, p.port or 443, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        fail(f"cannot resolve source host: {exc}")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            fail(f"source host resolves to a non-public address: {ip}")


def download_url(url: str, limit: int) -> bytes:
    assert_public_https(url)
    req = Request(url, headers={"User-Agent": "alisa-instagram-asset-import/1.0"})
    with urlopen(req, timeout=60) as r:
        length = r.headers.get("Content-Length")
        if length and int(length) > limit:
            fail(f"asset too large: Content-Length={length}, limit={limit}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > limit:
                fail(f"asset too large while downloading: {total} > {limit}")
            chunks.append(chunk)
    return b"".join(chunks)


def decode_base64(value: str, limit: int) -> bytes:
    if value.startswith("data:"):
        try:
            value = value.split(",", 1)[1]
        except IndexError:
            fail("invalid data URL")
    try:
        data = base64.b64decode(value, validate=True)
    except Exception as exc:
        fail(f"invalid base64 payload: {exc}")
    if len(data) > limit:
        fail(f"base64 asset too large: {len(data)} > {limit}")
    return data


def validate_magic(data: bytes, suffix: str) -> None:
    if len(data) < 12:
        fail("asset is too small to be valid")
    s = suffix.lower()
    ok = False
    if s in {".jpg", ".jpeg"}:
        ok = data.startswith(b"\xff\xd8\xff")
    elif s == ".png":
        ok = data.startswith(b"\x89PNG\r\n\x1a\n")
    elif s == ".webp":
        ok = data.startswith(b"RIFF") and data[8:12] == b"WEBP"
    elif s in {".mp4", ".mov"}:
        ok = data[4:8] == b"ftyp"
    if not ok:
        fail(f"file signature does not match target extension {suffix}")


def receipt_path(manifest: Path) -> Path:
    return RECEIPTS / f"{manifest.stem}.md"


def public_source_label(manifest_data: dict) -> str:
    if "source_url" in manifest_data:
        p = urlparse(manifest_data["source_url"])
        return f"https://{p.hostname}{p.path} (query omitted)"
    return "embedded base64 payload"


def process(manifest: Path) -> bool:
    receipt = receipt_path(manifest)
    if receipt.exists():
        print(f"SKIP {manifest.name}: receipt already exists")
        return False

    obj = json.loads(manifest.read_text(encoding="utf-8"))
    target = safe_target(str(obj.get("target_path", "")))
    replace = bool(obj.get("replace", False))
    requested_limit = int(obj.get("max_bytes", MAX_GITHUB_BYTES))
    limit = min(max(requested_limit, 1), MAX_GITHUB_BYTES)

    if target.exists() and not replace:
        fail(f"target already exists and replace=false: {target.relative_to(ROOT)}")

    has_url = bool(obj.get("source_url"))
    has_b64 = bool(obj.get("base64"))
    if has_url == has_b64:
        fail("manifest must contain exactly one of source_url or base64")

    data = download_url(obj["source_url"], limit) if has_url else decode_base64(obj["base64"], limit)
    validate_magic(data, target.suffix)

    expected = str(obj.get("expected_sha256", "")).strip().lower()
    sha = hashlib.sha256(data).hexdigest()
    if expected and expected != sha:
        fail(f"SHA-256 mismatch: expected {expected}, got {sha}")

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, target)

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    imported = datetime.now(timezone.utc).isoformat(timespec="seconds")
    receipt.write_text(
        "# Binary import receipt\n\n"
        f"- Manifest: `{manifest.relative_to(ROOT)}`\n"
        f"- Target: `{target.relative_to(ROOT)}`\n"
        f"- Bytes: {len(data)}\n"
        f"- SHA-256: `{sha}`\n"
        f"- Source: {public_source_label(obj)}\n"
        f"- Imported UTC: {imported}\n"
        f"- Replace allowed: `{replace}`\n",
        encoding="utf-8",
    )
    print(f"IMPORTED {target.relative_to(ROOT)} bytes={len(data)} sha256={sha}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="?", help="one manifest path")
    ap.add_argument("--all", action="store_true", help="process all queue manifests without receipts")
    ns = ap.parse_args()

    if ns.all:
        manifests = sorted(QUEUE.glob("*.json"))
    elif ns.manifest:
        manifests = [Path(ns.manifest)]
        if not manifests[0].is_absolute():
            manifests[0] = ROOT / manifests[0]
    else:
        ap.error("provide MANIFEST or --all")

    if not manifests:
        print("No pending manifests")
        return 0

    changed = False
    for manifest in manifests:
        try:
            changed = process(manifest) or changed
        except Exception as exc:
            print(f"ERROR {manifest}: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
