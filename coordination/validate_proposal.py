#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
TASKS = ROOT / "coordination" / "tasks.json"
POLICY = ROOT / "coordination" / "broker_policy.json"
ALLOWED_ACTORS = {"chatgpt", "grok"}
ALLOWED_OUTCOMES = {"completed", "qa_pass", "qa_fail", "blocked"}


def fail(msg: str) -> None:
    raise SystemExit(f"Coordination v4 proposal validation failed: {msg}")


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        fail(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path}: {exc}")


def norm_path(value: str) -> str:
    if not isinstance(value, str) or not value or value.startswith("/") or "\\" in value:
        fail(f"invalid operation path: {value!r}")
    p = Path(value)
    if any(part in {".", ".."} for part in p.parts):
        fail(f"path traversal forbidden: {value}")
    return p.as_posix()


def under(path: str, prefix: str) -> bool:
    return path.startswith(prefix.rstrip("/") + "/")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_proposal.py PROPOSAL.json")
    proposal = load(Path(sys.argv[1]))
    state = load(STATE)
    tasks_doc = load(TASKS)
    policy = load(POLICY)

    required = {
        "schema_version", "actor", "message_id", "task_id", "expected_state_sha",
        "turn_id", "outcome", "summary", "handoff_body", "operations", "blocker_fingerprint",
    }
    missing = sorted(required - set(proposal))
    if missing:
        fail(f"missing proposal keys: {', '.join(missing)}")
    extra = sorted(set(proposal) - required)
    if extra:
        fail(f"unexpected proposal keys: {', '.join(extra)}")
    if proposal["schema_version"] != 4:
        fail("proposal schema_version must be 4")

    actor = proposal["actor"]
    if actor not in ALLOWED_ACTORS:
        fail(f"invalid actor: {actor}")
    if state.get("schema_version") != 4:
        fail("canonical state is not schema v4")
    if state.get("next_actor") != actor:
        fail(f"actor does not own turn: expected {state.get('next_actor')}, got {actor}")
    if proposal["task_id"] != state.get("active_task"):
        fail("proposal task_id does not match active_task")

    prefix = "cg-" if actor == "chatgpt" else "gk-"
    if not isinstance(proposal["message_id"], str) or not proposal["message_id"].startswith(prefix):
        fail(f"message_id must start with {prefix}")
    if proposal["outcome"] not in ALLOWED_OUTCOMES:
        fail(f"invalid outcome: {proposal['outcome']}")
    if proposal["turn_id"] != state.get("turn_id") + 1:
        fail("turn_id must equal current turn_id + 1")

    state_blob = git("hash-object", "coordination/state.json")
    if proposal["expected_state_sha"] != state_blob:
        fail(f"stale proposal: expected_state_sha must equal {state_blob}")

    tasks = {t.get("id"): t for t in tasks_doc.get("tasks", [])}
    task = tasks.get(proposal["task_id"])
    if not task:
        fail("active task absent from task DB")
    if actor == task.get("qa_actor"):
        if task.get("status") != "qa_pending" or proposal["outcome"] not in {"qa_pass", "qa_fail", "blocked"}:
            fail("QA actor may only submit qa_pass/qa_fail/blocked for qa_pending task")
    elif proposal["outcome"] in {"qa_pass", "qa_fail"}:
        fail("non-QA actor cannot submit QA outcome")

    fingerprint = proposal["blocker_fingerprint"]
    if proposal["outcome"] == "blocked":
        if not isinstance(fingerprint, str) or not fingerprint.strip():
            fail("blocked outcome requires blocker_fingerprint")
        if fingerprint == task.get("blocker_fingerprint"):
            fail("unchanged blocker fingerprint rejected")
    elif fingerprint is not None:
        fail("non-blocked outcome requires blocker_fingerprint=null")

    if not isinstance(proposal["summary"], str) or not proposal["summary"].strip():
        fail("summary must be non-empty text")
    if not isinstance(proposal["handoff_body"], str):
        fail("handoff_body must be text")

    operations = proposal["operations"]
    if not isinstance(operations, list):
        fail("operations must be an array")
    if len(operations) > int(policy.get("max_operations_per_turn", 40)):
        fail("too many operations")

    protected_files = set(policy.get("protected_files", []))
    protected_prefixes = list(policy.get("protected_prefixes", []))
    allowed_files = set(policy.get("allowed_operation_files", []))
    allowed_prefixes = list(policy.get("allowed_operation_prefixes", []))
    allowed_ext = set(policy.get("allowed_text_extensions", []))
    max_chars = int(policy.get("max_text_chars_per_operation", 250000))
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
        if path in protected_files or any(under(path, p) for p in protected_prefixes):
            fail(f"protected path: {path}")
        if path not in allowed_files and not any(under(path, p) for p in allowed_prefixes):
            fail(f"path outside broker work-product allowlist: {path}")
        if Path(path).suffix.lower() not in allowed_ext:
            fail(f"non-text extension not allowed in proposal: {path}")
        if not isinstance(op["content"], str) or len(op["content"]) > max_chars:
            fail(f"invalid/oversized operation content: {path}")
        exists = (ROOT / path).exists()
        if op["action"] == "create" and exists:
            fail(f"create target exists: {path}")
        if op["action"] == "update" and not exists:
            fail(f"update target missing: {path}")

    print(
        "Coordination v4 proposal OK:",
        f"actor={actor}", f"task={proposal['task_id']}",
        f"turn={proposal['turn_id']}", f"outcome={proposal['outcome']}",
        f"ops={len(operations)}",
    )


if __name__ == "__main__":
    main()
