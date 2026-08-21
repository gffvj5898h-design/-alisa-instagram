#!/usr/bin/env python3
"""Technical Instagram-avatar QA for Alice.

This does not replace a visual identity review by Grok when the candidate is
not an exact byte copy of the canonical master face. It fails the obvious
broken cases automatically: missing file, wrong codec, tiny resolution,
identity drift, or a non-image payload.
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
MAX_BYTES = 8 * 1024 * 1024
MIN_BYTES = 2_000
ASPECT_WARN = 0.08  # |w-h|/max(w,h)
AHASH_SIZE = 16
AHASH_WARN = 24
AHASH_FAIL = 56
MAE_WARN = 18.0
MAE_FAIL = 36.0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jpeg_size(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("not a JPEG")
    i = 2
    n = len(data)
    while i + 9 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0xFF:
            i += 1
            continue
        if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            i += 2
            continue
        if i + 4 > n:
            break
        length = int.from_bytes(data[i + 2 : i + 4], "big")
        if marker in {0xC0, 0xC1, 0xC2, 0xC3}:
            if i + 9 > n:
                raise ValueError("truncated JPEG SOF segment")
            height = int.from_bytes(data[i + 5 : i + 7], "big")
            width = int.from_bytes(data[i + 7 : i + 9], "big")
            return width, height
        if length < 2 or i + 2 + length > n:
            raise ValueError("truncated JPEG segment before SOF")
        i += 2 + length
    raise ValueError("JPEG SOF not found")


def png_size(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24:
        raise ValueError("not a PNG")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def webp_size(data: bytes) -> tuple[int, int]:
    if not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
        raise ValueError("not a WEBP")
    if data[12:16] == b"VP8X" and len(data) >= 30:
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if data[12:16] == b"VP8 " and len(data) >= 30:
        width = int.from_bytes(data[26:28], "little") & 0x3FFF
        height = int.from_bytes(data[28:30], "little") & 0x3FFF
        return width, height
    raise ValueError("unsupported WEBP layout")


def sniff_format(data: bytes, suffix: str) -> str:
    if data.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "WEBP"
    raise ValueError(f"unrecognized image signature for {suffix}")


def image_size(data: bytes, fmt: str) -> tuple[int, int]:
    if fmt == "JPEG":
        return jpeg_size(data)
    if fmt == "PNG":
        return png_size(data)
    return webp_size(data)


def try_pillow():
    try:
        from PIL import Image  # type: ignore

        return Image
    except Exception:
        return None


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
    left = (w - side) // 2
    top = (h - side) // 2
    return image.crop((left, top, left + side, top + side))


def mae64(a: Any, b: Any) -> float:
    ga = center_square(a).convert("L").resize((64, 64))
    gb = center_square(b).convert("L").resize((64, 64))
    pa = list(ga.getdata())
    pb = list(gb.getdata())
    return sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa)


def basic_record(path: Path, data: bytes) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "suffix": path.suffix.lower(),
    }


def inspect(path: Path, data: bytes) -> dict[str, Any]:
    rec = basic_record(path, data)
    fmt = sniff_format(data, rec["suffix"])
    rec["format"] = fmt
    rec["width"], rec["height"] = image_size(data, fmt)
    rec["min_side"] = min(rec["width"], rec["height"])
    rec["max_side"] = max(rec["width"], rec["height"])
    rec["aspect_delta"] = abs(rec["width"] - rec["height"]) / rec["max_side"]
    rec["square"] = rec["aspect_delta"] <= ASPECT_WARN
    return rec


def judge(avatar: dict[str, Any], master: dict[str, Any], pillow_cmp: dict[str, Any] | None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if avatar["suffix"] not in ALLOWED_EXT:
        errors.append(f"unsupported extension: {avatar['suffix']}")
    if avatar["bytes"] < MIN_BYTES:
        errors.append(f"file too small: {avatar['bytes']} bytes")
    if avatar["bytes"] > MAX_BYTES:
        errors.append(f"file too large for Instagram avatar: {avatar['bytes']} bytes")
    if avatar["min_side"] < MIN_SIDE:
        errors.append(f"min side {avatar['min_side']} < {MIN_SIDE}")
    if avatar["min_side"] < PREFERRED_SIDE:
        warnings.append(f"min side {avatar['min_side']} < preferred {PREFERRED_SIDE}")
    if not avatar["square"]:
        warnings.append(
            f"not square ({avatar['width']}x{avatar['height']}); Instagram circular-crops the center"
        )

    exact = avatar["sha256"] == master["sha256"]
    identity = {
        "exact_master": exact,
        "kind": "exact_master_fallback" if exact else "divergent",
    }
    if exact:
        warnings.append("candidate is an exact Git/byte copy of master face, not a dense avatar crop")
    elif pillow_cmp is None:
        errors.append("candidate differs from master and Pillow identity check is unavailable")
    else:
        identity.update(pillow_cmp)
        if pillow_cmp["ahash_hamming"] > AHASH_FAIL and pillow_cmp["mae64"] > MAE_FAIL:
            errors.append(
                f"identity drift: ahash={pillow_cmp['ahash_hamming']} mae64={pillow_cmp['mae64']:.1f}"
            )
            identity["kind"] = "identity_fail"
        elif pillow_cmp["ahash_hamming"] > AHASH_WARN or pillow_cmp["mae64"] > MAE_WARN:
            warnings.append(
                f"identity is only approximate: ahash={pillow_cmp['ahash_hamming']} mae64={pillow_cmp['mae64']:.1f}"
            )
            identity["kind"] = "approximate_identity"
        else:
            identity["kind"] = "likely_same_identity"

    if errors:
        verdict = "fail"
    elif warnings:
        verdict = "warn"
    else:
        verdict = "pass"

    return {
        "verdict": verdict,
        "errors": errors,
        "warnings": warnings,
        "identity": identity,
        "instagram": {
            "usable_as_profile_photo": verdict != "fail",
            "preferred_square_1080": avatar["square"] and avatar["min_side"] >= PREFERRED_SIDE,
            "circular_crop_safe": avatar["min_side"] >= MIN_SIDE,
        },
    }


def compare_pillow(avatar_path: Path, master_path: Path) -> dict[str, Any] | None:
    Image = try_pillow()
    if Image is None:
        return None
    with Image.open(avatar_path) as av, Image.open(master_path) as mf:
        av.load()
        mf.load()
        return {
            "ahash_hamming": hamming(ahash(av), ahash(mf)),
            "mae64": round(mae64(av, mf), 3),
            "avatar_mode": av.mode,
            "master_mode": mf.mode,
        }


def invalid_result(path: Path, data: bytes, message: str) -> dict[str, Any]:
    return {
        "avatar": basic_record(path, data),
        "verdict": "fail",
        "errors": [message],
        "warnings": [],
        "identity": {"exact_master": False, "kind": "not_evaluated"},
        "instagram": {
            "usable_as_profile_photo": False,
            "preferred_square_1080": False,
            "circular_crop_safe": False,
        },
    }


def evaluate_pair(avatar_path: Path, master_path: Path) -> dict[str, Any]:
    if not avatar_path.is_file():
        return {
            "avatar": {"path": str(avatar_path)},
            "verdict": "fail",
            "errors": [f"missing avatar: {avatar_path}"],
            "warnings": [],
        }

    avatar_data = avatar_path.read_bytes()
    master_data = master_path.read_bytes()

    try:
        avatar = inspect(avatar_path, avatar_data)
    except Exception as exc:
        return invalid_result(
            avatar_path,
            avatar_data,
            f"invalid avatar image {avatar_path.name}: {type(exc).__name__}: {exc}",
        )

    try:
        master = inspect(master_path, master_data)
    except Exception as exc:
        result = invalid_result(
            avatar_path,
            avatar_data,
            f"canonical master is invalid: {type(exc).__name__}: {exc}",
        )
        result["master"] = basic_record(master_path, master_data)
        return result

    pillow_cmp = None
    if avatar["sha256"] != master["sha256"]:
        try:
            pillow_cmp = compare_pillow(avatar_path, master_path)
        except Exception as exc:
            return {
                "avatar": avatar,
                "master": master,
                "verdict": "fail",
                "errors": [f"Pillow could not decode/compare avatar: {type(exc).__name__}: {exc}"],
                "warnings": [],
                "identity": {"exact_master": False, "kind": "not_evaluated"},
                "instagram": {
                    "usable_as_profile_photo": False,
                    "preferred_square_1080": False,
                    "circular_crop_safe": False,
                },
            }

    judged = judge(avatar, master, pillow_cmp)
    return {"avatar": avatar, "master": master, **judged}


def default_targets(explicit: list[Path]) -> list[Path]:
    if explicit:
        return explicit
    found = sorted(
        p
        for p in PROFILE_DIR.glob("*")
        if p.is_file() and p.suffix.lower() in ALLOWED_EXT
    )
    return found or [DEFAULT_AVATAR]


def main() -> int:
    ap = argparse.ArgumentParser(description="QA Alice Instagram avatars")
    ap.add_argument("paths", nargs="*", type=Path, help="avatar files; default: content/profile/*")
    ap.add_argument("--master", type=Path, default=DEFAULT_MASTER)
    ap.add_argument("--strict", action="store_true", help="treat warnings as failure")
    ap.add_argument("--json", action="store_true", help="print JSON report")
    ap.add_argument("--write-receipt", type=Path, nargs="?", const=ROOT / "production" / "qa-receipts" / "avatar-latest.json")
    ns = ap.parse_args()

    if not ns.master.is_file():
        print(f"Avatar QA failed: missing master face {ns.master}", file=sys.stderr)
        return 1

    results = [evaluate_pair(path if path.is_absolute() else ROOT / path, ns.master) for path in default_targets(ns.paths)]
    worst = "pass"
    for item in results:
        if item["verdict"] == "fail":
            worst = "fail"
        elif item["verdict"] == "warn" and worst != "fail":
            worst = "warn"

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "master": str(ns.master.relative_to(ROOT)) if ns.master.is_relative_to(ROOT) else str(ns.master),
        "overall": worst,
        "strict": bool(ns.strict),
        "results": results,
    }

    if ns.write_receipt:
        ns.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        ns.write_receipt.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ns.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Avatar QA overall={worst} master={report['master']}")
        for item in results:
            av = item.get("avatar", {})
            print(
                f"- {av.get('path')} {item['verdict']} "
                f"{av.get('width')}x{av.get('height')} bytes={av.get('bytes')} "
                f"sha256={av.get('sha256', '')[:12]}… identity={item.get('identity', {}).get('kind')}"
            )
            for err in item.get("errors", []):
                print(f"  ERROR {err}")
            for warn in item.get("warnings", []):
                print(f"  WARN  {warn}")

    if worst == "fail" or (ns.strict and worst == "warn"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
