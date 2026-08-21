#!/usr/bin/env python3
"""Import generated binary assets from text-only queue manifests."""
from __future__ import annotations
import argparse, base64, hashlib, ipaddress, json, os, socket, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "production" / "import-queue"
RECEIPTS = ROOT / "production" / "import-receipts"
MAX_GITHUB_BYTES = 95 * 1024 * 1024
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}

def fail(msg): raise RuntimeError(msg)

def safe_target(raw: str) -> Path:
    if not raw or raw.startswith("/") or ".." in Path(raw).parts: fail("unsafe target_path")
    target = (ROOT / raw).resolve()
    try: rel = target.relative_to(ROOT)
    except ValueError: fail("target_path escapes repository root")
    if not str(rel).startswith("content/"): fail("binary import target must live under content/")
    if target.suffix.lower() not in ALLOWED_EXT: fail(f"unsupported target extension: {target.suffix}")
    return target

def assert_public_https(url: str):
    p = urlparse(url)
    if p.scheme != "https" or not p.hostname: fail("source_url must be https")
    for info in socket.getaddrinfo(p.hostname, p.port or 443, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            fail(f"non-public source address: {ip}")

def download_url(url: str, limit: int) -> bytes:
    assert_public_https(url)
    req = Request(url, headers={"User-Agent":"alisa-instagram-asset-import/1.1"})
    out=[]; total=0
    with urlopen(req, timeout=60) as r:
        while True:
            chunk=r.read(1024*1024)
            if not chunk: break
            total += len(chunk)
            if total > limit: fail("asset too large")
            out.append(chunk)
    return b"".join(out)

def decode_base64(value: str, limit: int) -> bytes:
    if value.startswith("data:"): value=value.split(",",1)[1]
    try: data=base64.b64decode(value, validate=True)
    except Exception as exc: fail(f"invalid base64: {exc}")
    if len(data)>limit: fail("base64 asset too large")
    return data

def decode_base64_chunks(paths, limit: int) -> bytes:
    if not isinstance(paths, list) or not paths: fail("base64_chunks must be a non-empty list")
    parts=[]
    for raw in paths:
        p=(ROOT / str(raw)).resolve()
        try: rel=p.relative_to(ROOT)
        except ValueError: fail("chunk path escapes repository root")
        if not str(rel).startswith("production/import-queue/chunks/"): fail("chunks must live under production/import-queue/chunks/")
        if not p.is_file(): fail(f"missing chunk: {rel}")
        parts.append(p.read_text(encoding="utf-8").strip())
    return decode_base64("".join(parts), limit)

def validate_magic(data: bytes, suffix: str):
    if len(data)<12: fail("asset too small")
    s=suffix.lower()
    ok=(s in {".jpg",".jpeg"} and data.startswith(b"\xff\xd8\xff")) or (s==".png" and data.startswith(b"\x89PNG\r\n\x1a\n")) or (s==".webp" and data.startswith(b"RIFF") and data[8:12]==b"WEBP") or (s in {".mp4",".mov"} and data[4:8]==b"ftyp")
    if not ok: fail(f"signature mismatch for {suffix}")

def source_label(obj):
    if obj.get("source_url"):
        p=urlparse(obj["source_url"]); return f"https://{p.hostname}{p.path} (query omitted)"
    if obj.get("base64_chunks"): return "repository base64 chunks"
    return "embedded base64 payload"

def process(manifest: Path) -> bool:
    receipt=RECEIPTS / f"{manifest.stem}.md"
    if receipt.exists(): print(f"SKIP {manifest.name}: receipt exists"); return False
    obj=json.loads(manifest.read_text(encoding="utf-8"))
    target=safe_target(str(obj.get("target_path","")))
    replace=bool(obj.get("replace",False)); limit=min(max(int(obj.get("max_bytes",MAX_GITHUB_BYTES)),1),MAX_GITHUB_BYTES)
    if target.exists() and not replace: fail(f"target exists: {target.relative_to(ROOT)}")
    modes=sum(bool(obj.get(k)) for k in ("source_url","base64","base64_chunks"))
    if modes != 1: fail("manifest must contain exactly one of source_url, base64, base64_chunks")
    if obj.get("source_url"): data=download_url(obj["source_url"],limit)
    elif obj.get("base64"): data=decode_base64(obj["base64"],limit)
    else: data=decode_base64_chunks(obj["base64_chunks"],limit)
    validate_magic(data,target.suffix)
    sha=hashlib.sha256(data).hexdigest(); expected=str(obj.get("expected_sha256","")).strip().lower()
    if expected and expected!=sha: fail(f"SHA-256 mismatch: expected {expected}, got {sha}")
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as tmp: tmp.write(data); tmp_path=Path(tmp.name)
    os.replace(tmp_path,target)
    RECEIPTS.mkdir(parents=True,exist_ok=True)
    receipt.write_text("# Binary import receipt\n\n"+f"- Manifest: `{manifest.relative_to(ROOT)}`\n- Target: `{target.relative_to(ROOT)}`\n- Bytes: {len(data)}\n- SHA-256: `{sha}`\n- Source: {source_label(obj)}\n- Imported UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n- Replace allowed: `{replace}`\n",encoding="utf-8")
    print(f"IMPORTED {target.relative_to(ROOT)} bytes={len(data)} sha256={sha}"); return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("manifest",nargs="?"); ap.add_argument("--all",action="store_true"); ns=ap.parse_args()
    manifests=sorted(QUEUE.glob("*.json")) if ns.all else ([ROOT/Path(ns.manifest)] if ns.manifest else [])
    if not manifests: print("No pending manifests"); return 0
    for m in manifests:
        try: process(m)
        except Exception as exc: print(f"ERROR {m}: {exc}",file=sys.stderr); return 1
    return 0
if __name__=="__main__": raise SystemExit(main())
