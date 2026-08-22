#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
POLICY = ROOT / "coordination" / "broker_policy.json"


def fail(msg: str) -> None:
    raise SystemExit(f"Agent response validation failed: {msg}")


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(proc.stderr.strip() or "git command failed")
    return proc.stdout.strip()


def norm_path(path: str) -> str:
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path:
        fail(f"invalid path: {path!r}")
    parts = Path(path).parts
    if ".." in parts or "." in parts:
        fail(f"path traversal is forbidden: {path}")
    return Path(*parts).as_posix()


def is_under(path: str, prefix: str) -> bool:
    return path == prefix.rstrip("/") or path.startswith(prefix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("proposal")
    args = parser.parse_args()

    proposal = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    policy = json.loads(POLICY.read_text(encoding="utf-8"))

    if state.get("schema_version") != 3:
        fail("state must be schema v3")

    required = {
        "schema_version",
        "actor",
        "message_id",
        "expected_parent_state_sha",
        "turn_id",
        "status",
        "next_actor",
        "summary",
        "handoff_body",
        "operations",
        "blocker_fingerprint",
    }
    missing = sorted(required - set(proposal))
    if missing:
        fail(f"missing keys: {', '.join(missing)}")

    if proposal["schema_version"] != 3:
        fail("proposal schema_version must be 3")
    if proposal["actor"] != state["next_actor"]:
        fail("proposal actor does not own the current turn")

    state_blob = git("hash-object", "coordination/state.json")
    if proposal["expected_parent_state_sha"] != state_blob:
        fail(
            "stale proposal: expected_parent_state_sha must equal "
            f"current state blob {state_blob}"
        )
    if proposal["turn_id"] != state["turn_id"] + 1:
        fail("proposal turn_id must equal current turn_id + 1")

    if proposal["actor"] == "chatgpt" and not str(proposal["message_id"]).startswith("cg-"):
        fail("ChatGPT message_id must start cg-")
    if proposal["actor"] == "grok" and not str(proposal["message_id"]).startswith("gk-"):
        fail("Grok message_id must start gk-")

    semantic = {
        "waiting_for_grok": "grok",
        "waiting_for_chatgpt": "chatgpt",
    }
    expected = semantic.get(proposal["status"])
    if expected and proposal["next_actor"] != expected:
        fail(f"{proposal['status']} requires next_actor={expected}")

    operations = proposal["operations"]
    if not isinstance(operations, list):
        fail("operations must be an array")
    max_ops = int(policy.get("max_operations_per_turn", 50))
    if len(operations) > max_ops:
        fail(f"too many operations: {len(operations)} > {max_ops}")

    protected = set(policy.get("protected_paths", []))
    broker_owned = policy.get("broker_owned_paths", [])
    allowed_prefixes = policy.get("allowed_write_prefixes", [])
    seen: set[str] = set()

    for op in operations:
        if not isinstance(op, dict) or set(op) != {"action", "path", "content"}:
            fail("each operation must contain exactly action, path, content")
        if op["action"] not in {"create", "update"}:
            fail("operation action must be create or update")
        path = norm_path(op["path"])
        if path in seen:
            fail(f"duplicate operation path: {path}")
        seen.add(path)
        if path in protected:
            fail(f"protected path cannot be changed by agent proposal: {path}")
        if any(is_under(path, prefix) for prefix in broker_owned):
            fail(f"broker-owned path cannot be changed by agent proposal: {path}")
        if not any(is_under(path, prefix) for prefix in allowed_prefixes):
            fail(f"path is outside allowed prefixes: {path}")
        if not isinstance(op["content"], str):
            fail(f"operation content must be string: {path}")

    blocked = proposal["status"] in {"blocked_binary", "blocked_tooling"}
    fingerprint = proposal["blocker_fingerprint"]
    if blocked and (not isinstance(fingerprint, str) or not fingerprint.strip()):
        fail("blocked proposal requires blocker_fingerprint")
    if not blocked and fingerprint is not None:
        fail("non-blocked proposal must use blocker_fingerprint=null")
    if blocked and fingerprint == state.get("blocker_fingerprint"):
        fail("repeated blocker fingerprint rejected; do not ping-pong without a changed condition")

    if state["hop_count"] >= state["hop_limit"]:
        fail("hop limit already reached")

    print(
        "Agent response OK:",
        f"actor={proposal['actor']}",
        f"turn={proposal['turn_id']}",
        f"next_actor={proposal['next_actor']}",
        f"ops={len(operations)}",
    )


if __name__ == "__main__":
    main()
