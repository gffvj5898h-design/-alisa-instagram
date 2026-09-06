#!/usr/bin/env python3
"""Strict technical QA for Alice profile avatars.

Canonical image integrity is validated before identity comparison. An exact byte
copy of a truncated/corrupt master can therefore never pass merely because the
SHA-256 values match.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER = ROOT / "character" / "references" / "alice-master-face.jpg"
DEFAULT_AVATAR = ROOT / "content" / "profile" / "avatar-candidate.jpg"
PROFILE_DIR = ROOT / "content" / "profile"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MIN_SIDE = 320
PREFERRED_SIDE = 1080
MIN_BYTES = 2_000
MAX_BYTES = 8 * 1024 * 1024
ASPECT_WARN = 0.08
AHASH_SIZE = 16
AHASH_WARN = 24
AHASH_FAIL = 56
MAE_WARN = 18.0
MAE_FAIL = 36.0


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pillow_image():
    try:
        from PIL import Image
        return Image
    except Exception as exc:
        raise RuntimeError(f"Pillow is required for integrity QA: {exc}") from exc


def sniff(data: bytes) -> str:
    if data.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WEBP":
        return "WEBP"
    raise ValueError("unrecognized image signature")


def inspect(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise ValueError(f"unsupported extension: {suffix}")
    fmt = sniff(data)
    if fmt == "JPEG" and not data.endswith(b"\xff\xd9"):
        raise ValueError("truncated JPEG: EOI marker missing")

    Image = pillow_image()
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            mode = image.mode
    except Exception as exc:
        raise ValueError(f"full image decode failed: {type(exc).__name__}: {exc}") from exc
    if width <= 0 or height <= 0:
        raise ValueError("invalid image dimensions")

    return {
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "bytes": len(data),
        "sha256": sha256(data),
        "suffix": suffix,
        "format": fmt,
        "width": width,
        "height": height,
        "mode": mode,
        "min_side": min(width, height),
        "max_side": max(width, height),
        "aspect_delta": abs(width - height) / max(width, height),
        "decode_integrity": "pass",
    }


def ahash(image: Any, size: int = AHASH_SIZE) -> str:
    gray = image.convert("L").resize((size, size))
    pixels = list(gray.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if px >= avg else "0" for px in pixels)


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def center_square(image: Any) -> Any:
    w, h = image.size
    side = min(w, h)
    return image.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))


def mae64(a: Any, b: Any) -> float:
    ga = center_square(a).convert("L").resize((64, 64))
    gb = center_square(b).convert("L").resize((64, 64))
    pa = list(ga.getdata())
    pb = list(gb.getdata())
    return sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa)


def compare(avatar_path: Path, master_path: Path) -> dict[str, Any]:
    Image = pillow_image()
    with Image.open(avatar_path) as av, Image.open(master_path) as mf:
        av.load(); mf.load()
        return {
            "ahash_hamming": hamming(ahash(av), ahash(mf)),
            "mae64": round(mae64(av, mf), 3),
        }


def evaluate(avatar_path: Path, master_path: Path, master: dict[str, Any]) -> dict[str, Any]:
    try:
        avatar = inspect(avatar_path)
    except Exception as exc:
        return {
            "avatar": {"path": str(avatar_path)},
            "master": master,
            "verdict": "fail",
            "errors": [f"invalid avatar: {type(exc).__name__}: {exc}"],
            "warnings": [],
            "identity": {"kind": "not_evaluated", "exact_master": False},
        }

    errors: list[str] = []
    warnings: list[str] = []
    if avatar["bytes"] < MIN_BYTES:
        errors.append(f"file too small: {avatar['bytes']} bytes")
    if avatar["bytes"] > MAX_BYTES:
        errors.append(f"file too large: {avatar['bytes']} bytes")
    if avatar["min_side"] < MIN_SIDE:
        errors.append(f"min side {avatar['min_side']} < {MIN_SIDE}")
    if avatar["min_side"] < PREFERRED_SIDE:
        warnings.append(f"min side {avatar['min_side']} < preferred {PREFERRED_SIDE}")
    square = avatar["aspect_delta"] <= ASPECT_WARN
    if not square:
        warnings.append(f"not square ({avatar['width']}x{avatar['height']})")

    exact = avatar["sha256"] == master["sha256"]
    identity: dict[str, Any] = {"exact_master": exact}
    if exact:
        identity["kind"] = "exact_master_fallback"
        warnings.append("candidate is an exact byte copy of the valid canonical master, not a dense avatar crop")
    else:
        cmp = compare(avatar_path, master_path)
        identity.update(cmp)
        if cmp["ahash_hamming"] > AHASH_FAIL and cmp["mae64"] > MAE_FAIL:
            identity["kind"] = "identity_fail"
            errors.append(f"identity drift: ahash={cmp['ahash_hamming']} mae64={cmp['mae64']:.1f}")
        elif cmp["ahash_hamming"] > AHASH_WARN or cmp["mae64"] > MAE_WARN:
            identity["kind"] = "approximate_identity"
            warnings.append(f"identity approximate: ahash={cmp['ahash_hamming']} mae64={cmp['mae64']:.1f}")
        else:
            identity["kind"] = "likely_same_identity"

    verdict = "fail" if errors else "warn" if warnings else "pass"
    return {
        "avatar": avatar,
        "master": master,
        "verdict": verdict,
        "errors": errors,
        "warnings": warnings,
        "identity": identity,
        "instagram": {
            "usable_as_profile_photo": verdict != "fail",
            "preferred_square_1080": square and avatar["min_side"] >= PREFERRED_SIDE,
            "circular_crop_safe": avatar["min_side"] >= MIN_SIDE,
        },
    }


def targets(explicit: list[Path]) -> list[Path]:
    if explicit:
        return [p if p.is_absolute() else ROOT / p for p in explicit]
    found = sorted(p for p in PROFILE_DIR.glob("*") if p.is_file() and p.suffix.lower() in ALLOWED_EXT)
    return found or [DEFAULT_AVATAR]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--master", type=Path, default=DEFAULT_MASTER)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-receipt", type=Path, nargs="?", const=ROOT / "production" / "qa-receipts" / "avatar-latest.json")
    ns = ap.parse_args()
    master_path = ns.master if ns.master.is_absolute() else ROOT / ns.master

    try:
        master = inspect(master_path)
        master_error = None
    except Exception as exc:
        master = {"path": str(master_path)}
        master_error = f"canonical master integrity failed: {type(exc).__name__}: {exc}"

    if master_error:
        results = [{
            "avatar": {"path": str(p)}, "master": master, "verdict": "fail",
            "errors": [master_error], "warnings": [],
            "identity": {"kind": "not_evaluated", "exact_master": False},
        } for p in targets(ns.paths)]
        overall = "fail"
    else:
        results = [evaluate(p, master_path, master) for p in targets(ns.paths)]
        overall = "fail" if any(r["verdict"] == "fail" for r in results) else "warn" if any(r["verdict"] == "warn" for r in results) else "pass"

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "master": str(master_path.relative_to(ROOT)) if master_path.is_relative_to(ROOT) else str(master_path),
        "master_integrity": "fail" if master_error else "pass",
        "overall": overall,
        "strict": bool(ns.strict),
        "results": results,
    }
    if ns.write_receipt:
        ns.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        ns.write_receipt.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if ns.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Avatar QA overall={overall} master_integrity={report['master_integrity']}")
        for item in results:
            print(f"- {item['avatar'].get('path')} {item['verdict']} identity={item.get('identity', {}).get('kind')}")
            for err in item.get("errors", []): print(f"  ERROR {err}")
            for warn in item.get("warnings", []): print(f"  WARN  {warn}")
    return 1 if overall == "fail" or (ns.strict and overall == "warn") else 0


if __name__ == "__main__":
    raise SystemExit(main())
