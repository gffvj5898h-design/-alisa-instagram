#!/usr/bin/env python3
"""Queue a local JPG/PNG/WEBP/MP4 as UTF-8 base64 chunks for GitHub Actions import."""
from __future__ import annotations
import argparse, base64, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("target_path")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--chunk-size", type=int, default=50000)
    ns = ap.parse_args()

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

    data = src.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    b64 = base64.b64encode(data).decode("ascii")
    chunk_dir = ROOT / "production" / "import-queue" / "chunks" / ns.slug
    chunk_dir.mkdir(parents=True, exist_ok=True)
    rels = []
    for i in range(0, len(b64), ns.chunk_size):
        n = len(rels) + 1
        rel = f"production/import-queue/chunks/{ns.slug}/part-{n:02d}.txt"
        (ROOT / rel).write_text(b64[i:i + ns.chunk_size], encoding="utf-8")
        rels.append(rel)

    manifest = {
        "base64_chunks": rels,
        "target_path": ns.target_path,
        "replace": bool(ns.replace),
        "max_bytes": 52428800,
        "expected_sha256": sha,
        "note": ns.note,
    }
    out = ROOT / "production" / "import-queue" / f"{ns.slug}.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"queued {src.name} -> {ns.target_path}")
    print(f"bytes {len(data)}")
    print(f"sha256 {sha}")
    print(f"chunks {len(rels)}")
    print(f"manifest {out.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
