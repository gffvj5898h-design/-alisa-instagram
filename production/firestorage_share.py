#!/usr/bin/env python3
"""Narrow downloader for public firestorage.ai shares used by project data-plane jobs.

The public share page is HTML. Its client calls the firestorage file API to obtain
an expiring raw download URL. This module performs that flow without persisting
or logging the signed URL, and always validates the downloaded bytes elsewhere
with an expected SHA-256.
"""
from __future__ import annotations

import ipaddress
import json
import re
import socket
from urllib.parse import urlparse
from urllib.request import Request, urlopen

API_BASE = "https://api.firestorage.ai/dev/file"
SHARE_RE = re.compile(r"^/(?:ja/|en/)?f/([0-9A-Za-z_-]{12})/?$")
USER_AGENT = "alisa-instagram-firestorage-bridge/1.0"


class FirestorageError(RuntimeError):
    pass


def _fail(message: str) -> None:
    raise FirestorageError(message)


def assert_public_https(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        _fail("download URL must be public HTTPS")
    for info in socket.getaddrinfo(parsed.hostname, parsed.port or 443, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            _fail(f"download URL resolved to non-public address: {ip}")


def parse_share_id(share_url: str) -> str:
    parsed = urlparse(share_url)
    if parsed.scheme != "https" or parsed.hostname != "firestorage.ai" or parsed.query or parsed.fragment:
        _fail("firestorage_share_url must be a plain https://firestorage.ai/... share URL")
    match = SHARE_RE.fullmatch(parsed.path)
    if not match:
        _fail("unsupported firestorage share URL shape")
    return match.group(1)


def _json_request(url: str, method: str = "GET") -> dict:
    req = Request(url, method=method, data=b"" if method == "POST" else None, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=45) as response:
        raw = response.read(2 * 1024 * 1024)
        if response.read(1):
            _fail("firestorage API response unexpectedly large")
    try:
        value = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        _fail(f"invalid firestorage API JSON: {exc}")
    if not isinstance(value, dict):
        _fail("firestorage API returned non-object JSON")
    return value


def download_share_file(
    share_url: str,
    *,
    expected_filename: str,
    expected_bytes: int | None,
    max_bytes: int,
) -> bytes:
    """Download exactly one named file from an unprotected public share."""
    if not expected_filename or "/" in expected_filename or "\\" in expected_filename:
        _fail("invalid expected_filename")
    if max_bytes <= 0:
        _fail("max_bytes must be positive")

    share_id = parse_share_id(share_url)
    endpoint = f"{API_BASE}/shares/{share_id}"
    listing = _json_request(f"{endpoint}/files?maxResults=1000")
    if listing.get("passwordProtected") is True:
        _fail("password-protected firestorage shares are not supported")
    files = listing.get("files")
    if not isinstance(files, list):
        _fail("firestorage share response has no files array")

    matches = [item for item in files if isinstance(item, dict) and item.get("fileName") == expected_filename]
    if len(matches) != 1:
        _fail(f"expected exactly one file named {expected_filename!r}, found {len(matches)}")
    item = matches[0]
    file_id = item.get("fileId")
    size = item.get("sizeBytes")
    if not isinstance(file_id, str) or not file_id:
        _fail("firestorage file has no fileId")
    if not isinstance(size, int) or size < 1:
        _fail("firestorage file has invalid sizeBytes")
    if expected_bytes is not None and size != expected_bytes:
        _fail(f"firestorage metadata size mismatch: expected {expected_bytes}, got {size}")
    if size > max_bytes:
        _fail(f"firestorage file exceeds max_bytes: {size} > {max_bytes}")

    ticket = _json_request(f"{endpoint}/files/{file_id}/download", method="POST")
    download_url = ticket.get("downloadUrl")
    if not isinstance(download_url, str) or not download_url:
        _fail("firestorage download response has no downloadUrl")
    assert_public_https(download_url)

    req = Request(download_url, headers={"User-Agent": USER_AGENT})
    chunks: list[bytes] = []
    total = 0
    with urlopen(req, timeout=60) as response:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                _fail("downloaded firestorage asset exceeds max_bytes")
            chunks.append(chunk)
    data = b"".join(chunks)
    if expected_bytes is not None and len(data) != expected_bytes:
        _fail(f"downloaded byte count mismatch: expected {expected_bytes}, got {len(data)}")
    if len(data) != size:
        _fail(f"downloaded byte count differs from firestorage metadata: {len(data)} != {size}")
    return data
