#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
VALIDATOR = ROOT / "coordination" / "validate_agent_response.py"


def fail(msg: str) -> None:
    raise SystemExit(f"Apply turn failed: {msg}")


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


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-").lower()
    return value[:48] or "task"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("proposal")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="actually write work-product, message, and state",
    )
    args = parser.parse_args()

    proposal_path = Path(args.proposal)
    subprocess.run(
        [sys.executable, str(VALIDATOR), str(proposal_path)],
        cwd=ROOT,
        check=True,
    )

    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    current_blob = git("hash-object", "coordination/state.json")

    planned = [op["path"] for op in proposal["operations"]]
    recipient = proposal["next_actor"]
    actor = proposal["actor"]
    timestamp = datetime.now(timezone.utc)
    file_stamp = timestamp.strftime("%Y%m%d-%H%M%S")
    slug = slugify(state["active_task"])
    message_rel = (
        f"coordination/messages/{file_stamp}-{actor}-to-{recipient}-"
        f"{slug}-t{proposal['turn_id']}.md"
    )
    message_path = ROOT / message_rel

    if message_path.exists():
        fail(f"handoff message already exists: {message_rel}")

    print("Apply plan:")
    print(f"  actor={actor}")
    print(f"  next_actor={recipient}")
    print(f"  turn={proposal['turn_id']}")
    print(f"  state_parent={current_blob}")
    print(f"  handoff={message_rel}")
    for path in planned:
        print(f"  operation={path}")

    if not args.apply:
        print("Dry-run only; pass --apply to write files")
        return

    for op in proposal["operations"]:
        target = ROOT / op["path"]
        if op["action"] == "create" and target.exists():
            fail(f"create target already exists: {op['path']}")
        if op["action"] == "update" and not target.exists():
            fail(f"update target does not exist: {op['path']}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(op["content"], encoding="utf-8")

    recipient_label = "ChatGPT" if recipient == "chatgpt" else "Grok"
    actor_label = "ChatGPT" if actor == "chatgpt" else "Grok"
    message = (
        f"# Handoff: {actor_label} → {recipient_label}\n\n"
        f"- Message ID: `{proposal['message_id']}`\n"
        f"- Active task: `{state['active_task']}`\n"
        f"- Recipient: {recipient_label}\n"
        f"- Status: `{proposal['status']}`\n"
        f"- Turn ID: `{proposal['turn_id']}`\n"
        f"- Parent state SHA: `{current_blob}`\n\n"
        f"## Summary\n\n{proposal['summary']}\n\n"
        f"## Handoff\n\n{proposal['handoff_body']}\n"
    )
    message_path.write_text(message, encoding="utf-8")

    next_state = dict(state)
    next_state["updated_at"] = timestamp.isoformat()
    next_state["status"] = proposal["status"]
    next_state["next_actor"] = proposal["next_actor"]
    next_state["message_path"] = message_rel
    next_state["turn_id"] = proposal["turn_id"]
    next_state["parent_state_sha"] = current_blob
    next_state["hop_count"] = state["hop_count"] + 1
    next_state["blocker_fingerprint"] = proposal["blocker_fingerprint"]
    next_state["notes"] = proposal["summary"]
    next_state["broker"] = dict(state["broker"])
    next_state["broker"]["lease_owner"] = None
    next_state["broker"]["lease_expires_at"] = None

    if actor == "chatgpt":
        next_state["last_chatgpt_message_id"] = proposal["message_id"]
    else:
        next_state["last_grok_message_id"] = proposal["message_id"]

    temp = STATE.with_suffix(".json.tmp")
    temp.write_text(
        json.dumps(next_state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp.replace(STATE)

    subprocess.run(
        [sys.executable, str(ROOT / "coordination" / "validate_state.py")],
        cwd=ROOT,
        check=True,
    )
    print("Turn applied to working tree; commit is still required")


if __name__ == "__main__":
    main()
