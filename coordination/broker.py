#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"


def fail(msg: str) -> None:
    raise SystemExit(f"AI broker failed: {msg}")


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--mode", choices=["dry_run", "product_mailbox"])
    args = parser.parse_args()

    subprocess.run(
        [sys.executable, str(ROOT / "coordination" / "validate_state.py")],
        cwd=ROOT,
        check=True,
    )

    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("schema_version") != 3:
        fail("broker requires schema v3 state")
    if state["hop_count"] >= state["hop_limit"]:
        fail("hop limit reached")
    if state["status"] == "completed":
        print("AI broker: state completed; nothing to dispatch")
        return
    if state["broker"]["lease_owner"]:
        fail(f"broker lease is already held by {state['broker']['lease_owner']}")

    mode = args.mode or state["broker"]["mode"]
    message_path = ROOT / state["message_path"]
    state_blob = git("hash-object", "coordination/state.json")

    envelope = {
        "schema_version": 3,
        "mode": mode,
        "actor": state["next_actor"],
        "active_task": state["active_task"],
        "target_ref": state["target_ref"],
        "current_turn_id": state["turn_id"],
        "proposal_turn_id": state["turn_id"] + 1,
        "expected_parent_state_sha": state_blob,
        "message_path": state["message_path"],
        "message": message_path.read_text(encoding="utf-8"),
        "protocol_path": "coordination/PROTOCOL_V3.md",
        "response_schema_path": "coordination/agent_response.schema.json",
        "proposal_directory": "coordination/proposals/",
        "instruction": (
            "Read the repository instructions and referenced task files. "
            "Create exactly one JSON proposal conforming to "
            "coordination/agent_response.schema.json under coordination/proposals/. "
            "Do not write coordination/state.json or coordination/messages directly."
        ),
    }

    payload = json.dumps(envelope, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
        print(f"AI broker envelope written to {args.output}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
