#!/usr/bin/env python3
"""One-shot integrity repair for Alice canonical identity.

This maintenance path is intentionally narrow: exact target, exact corrupt current
SHA, exact verified replacement SHA. It cannot be reused to redesign the face.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, os, tempfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "character/references/alice-master-face.jpg"
IDENTITY = ROOT / "character/identity.json"
ALLOWED_OLD_SHA = "2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2"
ALLOWED_NEW_SHA = "d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767"
EXPECTED_SIZE = (1237, 1536)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(msg: str) -> None:
    raise RuntimeError(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ns = ap.parse_args()
    manifest = (ROOT / ns.manifest).resolve()
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
    chunks = obj.get("base64_chunks")
    if not isinstance(chunks, list) or not chunks:
        fail("base64_chunks required")
    parts = []
    for raw in chunks:
        p = (ROOT / str(raw)).resolve()
        rel = p.relative_to(ROOT).as_posix()
        if not rel.startswith("production/identity-repair-queue/chunks/"):
            fail(f"unsafe chunk path: {rel}")
        parts.append(p.read_text(encoding="utf-8").strip())
    data = base64.b64decode("".join(parts), validate=True)
    if sha(data) != ALLOWED_NEW_SHA:
        fail("replacement SHA mismatch")
    if not data.startswith(b"\xff\xd8\xff") or not data.rstrip().endswith(b"\xff\xd9"):
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
    print(f"canonical repaired bytes={len(data)} sha256={ALLOWED_NEW_SHA} size={EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
