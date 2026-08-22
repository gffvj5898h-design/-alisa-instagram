#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
VALIDATOR = ROOT / "coordination" / "validate_agent_response.py"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def run(proposal: dict, expect_ok: bool, label: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump(proposal, fh, ensure_ascii=False, indent=2)
        path = fh.name
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), path],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    Path(path).unlink(missing_ok=True)
    ok = proc.returncode == 0
    if ok != expect_ok:
        raise SystemExit(
            f"{label}: expected {'success' if expect_ok else 'failure'}, "
            f"got rc={proc.returncode}\n{proc.stdout}"
        )
    print(f"PASS {label}: rc={proc.returncode}")


def base_proposal(state: dict, state_sha: str) -> dict:
    actor = state["next_actor"]
    return {
        "schema_version": 3,
        "actor": actor,
        "message_id": ("cg-test-v3-001" if actor == "chatgpt" else "gk-test-v3-001"),
        "expected_parent_state_sha": state_sha,
        "turn_id": state["turn_id"] + 1,
        "status": ("waiting_for_grok" if actor == "chatgpt" else "waiting_for_chatgpt"),
        "next_actor": ("grok" if actor == "chatgpt" else "chatgpt"),
        "summary": "guard test",
        "handoff_body": "guard test",
        "operations": [],
        "blocker_fingerprint": None,
    }


def main() -> None:
    original_text = STATE.read_text(encoding="utf-8")
    state = json.loads(original_text)
    state_sha = git("hash-object", "coordination/state.json")

    proposal = base_proposal(state, state_sha)
    run(proposal, True, "valid proposal")

    log_update = dict(proposal)
    log_update["operations"] = [
        {
            "action": "update",
            "path": "GROK_CONTEXT_AND_LOG.md",
            "content": "test content",
        }
    ]
    run(log_update, True, "exact allowed project log path accepted")

    stale = dict(proposal)
    stale["expected_parent_state_sha"] = "0" * 40
    run(stale, False, "stale state SHA rejected")

    protected = dict(proposal)
    protected["operations"] = [
        {"action": "update", "path": "coordination/state.json", "content": "{}"}
    ]
    run(protected, False, "broker-owned state write rejected")

    canon = dict(proposal)
    canon["operations"] = [
        {
            "action": "update",
            "path": "character/references/alice-master-face.jpg",
            "content": "not-a-binary",
        }
    ]
    run(canon, False, "canonical face write rejected")

    outside = dict(proposal)
    outside["operations"] = [
        {"action": "update", "path": "README.md", "content": "not allowed"}
    ]
    run(outside, False, "outside work-product path rejected")

    repeated = dict(proposal)
    repeated["status"] = "blocked_tooling"
    repeated["blocker_fingerprint"] = state["blocker_fingerprint"]
    run(repeated, False, "repeated blocker fingerprint rejected")

    try:
        limited = dict(state)
        limited["hop_count"] = limited["hop_limit"]
        STATE.write_text(json.dumps(limited, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        limited_sha = git("hash-object", "coordination/state.json")
        hop = base_proposal(limited, limited_sha)
        run(hop, False, "hop limit rejected")
    finally:
        STATE.write_text(original_text, encoding="utf-8")

    print("All v3 guard tests passed")


if __name__ == "__main__":
    main()
