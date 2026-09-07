#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "coordination" / "validate_proposal.py"
BROKER = ROOT / "coordination" / "broker.py"
STATE = ROOT / "coordination" / "state.json"


def run(args: list[str], expect: int = 0) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if (p.returncode == 0) != (expect == 0):
        raise AssertionError(
            f"unexpected rc={p.returncode} for {' '.join(args)}\nstdout={p.stdout}\nstderr={p.stderr}"
        )
    return p.stdout + p.stderr


def state_sha() -> str:
    return subprocess.check_output(["git", "hash-object", "coordination/state.json"], cwd=ROOT, text=True).strip()


def proposal(**overrides):
    state = json.loads(STATE.read_text(encoding="utf-8"))
    actor = state["next_actor"]
    prefix = "cg" if actor == "chatgpt" else "gk"
    obj = {
        "schema_version": 4,
        "actor": actor,
        "message_id": f"{prefix}-v4-guard-smoke",
        "task_id": state["active_task"],
        "expected_state_sha": state_sha(),
        "turn_id": state["turn_id"] + 1,
        "outcome": "completed",
        "summary": "v4 guard smoke",
        "handoff_body": "dry run only",
        "operations": [],
        "blocker_fingerprint": None,
    }
    obj.update(overrides)
    return obj


def write_tmp(obj) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False)
    json.dump(obj, f, ensure_ascii=False)
    f.write("\n")
    f.close()
    return Path(f.name)


def main() -> None:
    run([sys.executable, "coordination/validate_state.py"])

    good = write_tmp(proposal())
    run([sys.executable, str(VALIDATE), str(good)])
    run([sys.executable, str(BROKER), str(good)])

    stale = write_tmp(proposal(expected_state_sha="0" * 40))
    out = run([sys.executable, str(VALIDATE), str(stale)], expect=1)
    assert "stale proposal" in out

    wrong_actor = "chatgpt" if proposal()["actor"] == "grok" else "grok"
    wrong = proposal(actor=wrong_actor, message_id=("cg-" if wrong_actor == "chatgpt" else "gk-") + "wrong")
    out = run([sys.executable, str(VALIDATE), str(write_tmp(wrong))], expect=1)
    assert "does not own turn" in out

    protected = proposal(
        operations=[{"action": "update", "path": "coordination/state.json", "content": "{}\n"}]
    )
    out = run([sys.executable, str(VALIDATE), str(write_tmp(protected))], expect=1)
    assert "protected path" in out

    executable = proposal(
        operations=[{"action": "update", "path": "production/import_generated_asset.py", "content": "pass\n"}]
    )
    out = run([sys.executable, str(VALIDATE), str(write_tmp(executable))], expect=1)
    assert "protected path" in out

    traversal = proposal(
        operations=[{"action": "create", "path": "content/../oops.md", "content": "x\n"}]
    )
    out = run([sys.executable, str(VALIDATE), str(write_tmp(traversal))], expect=1)
    assert "path traversal" in out

    print("Coordination v4 guard tests OK")


if __name__ == "__main__":
    main()
