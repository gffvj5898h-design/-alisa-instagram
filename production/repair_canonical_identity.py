#!/usr/bin/env python3
"""One-shot integrity repair for Alice canonical identity.

This maintenance path is intentionally narrow: exact target, exact corrupt current
SHA, exact verified replacement SHA and dimensions. It cannot be reused to redesign
the face. Source bytes may arrive either as repository base64 chunks or via a
public firestorage.ai share; both modes are verified against the same hard-coded
replacement hash before any canonical write.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import tempfile
from io import BytesIO
from pathlib import Path

from firestorage_share import download_share_file

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "character/references/alice-master-face.jpg"
IDENTITY = ROOT / "character/identity.json"
ALLOWED_OLD_SHA = "2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2"
ALLOWED_NEW_SHA = "d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767"
EXPECTED_SIZE = (1237, 1536)
EXPECTED_BYTES = 606787
EXPECTED_FILENAME = "alice-master-face-original.jpeg"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(msg: str) -> None:
    raise RuntimeError(msg)


def load_source(obj: dict) -> tuple[bytes, str]:
    chunks = obj.get("base64_chunks")
    share_url = obj.get("firestorage_share_url")
    modes = int(bool(chunks)) + int(bool(share_url))
    if modes != 1:
        fail("manifest requires exactly one of base64_chunks or firestorage_share_url")

    if share_url:
        if obj.get("expected_filename") not in {None, EXPECTED_FILENAME}:
            fail("manifest expected_filename is not authorized")
        if obj.get("expected_bytes") not in {None, EXPECTED_BYTES}:
            fail("manifest expected_bytes is not authorized")
        data = download_share_file(
            str(share_url),
            expected_filename=EXPECTED_FILENAME,
            expected_bytes=EXPECTED_BYTES,
            max_bytes=EXPECTED_BYTES,
        )
        return data, "verified firestorage public share"

    if not isinstance(chunks, list) or not chunks:
        fail("base64_chunks must be a non-empty list")
    parts: list[str] = []
    for raw in chunks:
        p = (ROOT / str(raw)).resolve()
        try:
            rel = p.relative_to(ROOT).as_posix()
        except ValueError:
            fail("chunk path escapes repository root")
        if not rel.startswith("production/identity-repair-queue/chunks/"):
            fail(f"unsafe chunk path: {rel}")
        if not p.is_file():
            fail(f"missing repair chunk: {rel}")
        parts.append(p.read_text(encoding="utf-8").strip())
    try:
        data = base64.b64decode("".join(parts), validate=True)
    except Exception as exc:
        fail(f"invalid repair base64: {exc}")
    return data, "repository base64 chunks"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ns = ap.parse_args()
    manifest = (ROOT / ns.manifest).resolve()
    try:
        manifest.relative_to(ROOT / "production" / "identity-repair-queue")
    except ValueError:
        fail("repair manifest must live under production/identity-repair-queue")
    obj = json.loads(manifest.read_text(encoding="utf-8"))

    if obj.get("target_path") != "character/references/alice-master-face.jpg":
        fail("target_path is not canonical Alice path")
    if obj.get("expected_current_sha256") != ALLOWED_OLD_SHA:
        fail("manifest old SHA is not authorized")
    if obj.get("expected_sha256") != ALLOWED_NEW_SHA:
        fail("manifest replacement SHA is not authorized")

    current = TARGET.read_bytes()
    current_sha = sha(current)
    if current_sha == ALLOWED_NEW_SHA:
        print("canonical already repaired")
        return 0
    if current_sha != ALLOWED_OLD_SHA:
        fail(f"current canonical SHA changed unexpectedly: {current_sha}")

    data, source = load_source(obj)
    if len(data) != EXPECTED_BYTES:
        fail(f"replacement byte count mismatch: {len(data)} != {EXPECTED_BYTES}")
    if sha(data) != ALLOWED_NEW_SHA:
        fail("replacement SHA mismatch")
    if not data.startswith(b"\xff\xd8\xff") or not data.endswith(b"\xff\xd9"):
        fail("replacement is not a complete JPEG")

    from PIL import Image
    with Image.open(BytesIO(data)) as im:
        im.verify()
    with Image.open(BytesIO(data)) as im:
        im.load()
        if im.size != EXPECTED_SIZE:
            fail(f"unexpected dimensions: {im.size}")
        mode = im.mode

    with tempfile.NamedTemporaryFile(dir=TARGET.parent, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, TARGET)

    identity = {
        "schema_version": 1,
        "active": {
            "path": "character/references/alice-master-face.jpg",
            "sha256": ALLOWED_NEW_SHA,
            "bytes": len(data),
            "width": EXPECTED_SIZE[0],
            "height": EXPECTED_SIZE[1],
            "format": "JPEG",
            "mode": mode,
            "source": "verified original user upload recovered 2026-09-06",
            "transport": source,
            "status": "canonical"
        },
        "repaired_from": {
            "sha256": ALLOWED_OLD_SHA,
            "bytes": len(current),
            "status": "truncated-corrupt",
            "note": "Historical corrupt bytes remain in Git history; this repair restores the same canonical identity."
        }
    }
    IDENTITY.write_text(json.dumps(identity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"canonical repaired bytes={len(data)} sha256={ALLOWED_NEW_SHA} size={EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]} source={source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
