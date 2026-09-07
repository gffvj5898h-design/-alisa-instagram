#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = ROOT / "coordination" / "apply_human_intake.py"
STATE = ROOT / "coordination" / "state.json"
CAPS = ROOT / "coordination" / "capabilities.json"


def run(args: list[str], expect: int = 0) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if (p.returncode == 0) != (expect == 0):
        raise AssertionError(
            f"unexpected rc={p.returncode} for {' '.join(args)}\nstdout={p.stdout}\nstderr={p.stderr}"
        )
    return p.stdout + p.stderr


def main() -> None:
    from broker import apply_verified_capability_probe  # type: ignore

    caps = json.loads(CAPS.read_text(encoding="utf-8"))
    synthetic_caps = deepcopy(caps)
    synthetic_caps["actors"]["grok"]["identity_reference_still_generation"] = False
    probe_task = {
        "id": "probe",
        "capability_probe": {
            "actor": "grok",
            "capability": "identity_reference_still_generation",
        },
    }
    assert apply_verified_capability_probe(probe_task, "completed", synthetic_caps) is False
    assert synthetic_caps["actors"]["grok"]["identity_reference_still_generation"] is False
    assert apply_verified_capability_probe(probe_task, "qa_pass", synthetic_caps) is True
    assert synthetic_caps["actors"]["grok"]["identity_reference_still_generation"] is True

    baseline = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    baseline_state = json.loads(STATE.read_text(encoding="utf-8"))
    assert baseline_state["task_status"] == "idle"
    assert baseline_state["next_actor"] is None

    intake = {
        "schema_version": 1,
        "intake_id": "human-ci-intake-smoke",
        "summary": "CI smoke for guarded human intake",
        "tasks": [
            {
                "id": "human-intake-ci-task",
                "description": "No-op task created only inside ephemeral CI checkout.",
                "priority": 99999,
                "status": "ready",
                "requires": ["github_read", "github_text_proposal_write"],
                "dependencies": [],
                "preferred_actor": "chatgpt",
                "qa_actor": None,
                "attempts": 0,
                "max_attempts": 2,
                "blocked_on": [],
                "blocker_fingerprint": None,
            }
        ],
        "context_files": [],
    }
    f = tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False)
    json.dump(intake, f, ensure_ascii=False)
    f.write("\n")
    f.close()

    try:
        run([sys.executable, str(APPLY), f.name])
        state = json.loads(STATE.read_text(encoding="utf-8"))
        assert state["turn_id"] == baseline_state["turn_id"] + 1
        assert state["active_task"] == "human-intake-ci-task"
        assert state["task_status"] == "ready"
        assert state["next_actor"] == "chatgpt"
        assert state["message_path"].startswith("coordination/messages/")
        assert (ROOT / state["message_path"]).is_file()
        assert (ROOT / "coordination/intakes/human-ci-intake-smoke.json").is_file()
        run([sys.executable, "coordination/validate_state.py"])
    finally:
        subprocess.run(["git", "reset", "--hard", baseline], cwd=ROOT, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "clean", "-fd", "coordination/intakes", "coordination/messages"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    print("Coordination v4 human intake + capability probe tests OK")


if __name__ == "__main__":
    main()
