#!/usr/bin/env python3
"""Emit a GitHub push_files payload for an already-prepared import-queue slug.

Grok cannot write binary through the text-only Contents API. After
prepare_github_import.py writes UTF-8 chunks + a JSON manifest, this
script prints a JSON array of {path, content} objects that can be passed
to github___push_files in one commit.

Usage:
  python3 production/prepare_github_import.py SRC content/... --slug SLUG
  python3 production/emit_push_files_json.py SLUG > /tmp/push-files.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--root", default="")
    ns = ap.parse_args()
    root = Path(ns.root).resolve() if ns.root else ROOT
    manifest = root / "production" / "import-queue" / f"{ns.slug}.json"
    if not manifest.is_file():
        print(f"missing manifest: {manifest}", file=sys.stderr)
        return 1
    obj = json.loads(manifest.read_text(encoding="utf-8"))
    rels = list(obj.get("base64_chunks") or [])
    rels.append(str(manifest.relative_to(root)))
    files = []
    for rel in rels:
        path = root / rel
        if not path.is_file():
            print(f"missing file: {rel}", file=sys.stderr)
            return 1
        files.append({"path": rel, "content": path.read_text(encoding="utf-8")})
    json.dump(files, sys.stdout, ensure_ascii=True)
    sys.stdout.write("\n")
    print(f"files {len(files)}", file=sys.stderr)
    for item in files:
        print(f"  {item['path']} chars={len(item['content'])}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
