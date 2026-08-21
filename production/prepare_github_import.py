#!/usr/bin/env python3
"""Prepare a local binary for the GitHub Actions import queue.

Works without git credentials. Writes UTF-8 chunk files + a JSON manifest
that `.github/workflows/import-generated-assets.yml` can import.

Typical Grok flow:
  1. python3 production/prepare_github_import.py SRC content/... --slug SLUG
  2. Commit the printed files with the text-only GitHub tool (push_files).
  3. Wait for workflow "Import generated assets".
  4. Verify content/... and production/import-receipts/SLUG.md
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("target_path")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--chunk-size", type=int, default=50000)
    ap.add_argument(
        "--root",
        default="",
        help="Repository root. Default: parent of production/ if this file lives there.",
    )
    ns = ap.parse_args()

    root = Path(ns.root).resolve() if ns.root else Path(__file__).resolve().parents[1]
    src = Path(ns.src).resolve()
    if not src.is_file():
        print(f"missing file: {src}", file=sys.stderr)
        return 1
    if Path(ns.target_path).suffix.lower() not in ALLOWED:
        print("unsupported target extension", file=sys.stderr)
        return 1
    if not ns.target_path.startswith("content/"):
        print("target_path must be under content/", file=sys.stderr)
        return 1
    if ns.chunk_size < 1000:
        print("chunk-size too small", file=sys.stderr)
        return 1

    data = src.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    b64 = base64.b64encode(data).decode("ascii")
    chunk_dir = root / "production" / "import-queue" / "chunks" / ns.slug
    chunk_dir.mkdir(parents=True, exist_ok=True)
    rels: list[str] = []
    for i in range(0, len(b64), ns.chunk_size):
        n = len(rels) + 1
        rel = f"production/import-queue/chunks/{ns.slug}/part-{n:02d}.txt"
        (root / rel).write_text(b64[i : i + ns.chunk_size], encoding="utf-8")
        rels.append(rel)

    manifest = {
        "base64_chunks": rels,
        "target_path": ns.target_path,
        "replace": bool(ns.replace),
        "max_bytes": 52428800,
        "expected_sha256": sha,
        "note": ns.note,
    }
    out = root / "production" / "import-queue" / f"{ns.slug}.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"queued {src.name} -> {ns.target_path}")
    print(f"bytes {len(data)}")
    print(f"sha256 {sha}")
    print(f"chunks {len(rels)}")
    print(f"manifest {out.relative_to(root)}")
    print("commit these files:")
    for rel in rels + [str(out.relative_to(root))]:
        print(f"  {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
