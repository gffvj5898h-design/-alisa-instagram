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


def read_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def assert_workflow_guards() -> None:
    broker_wf = (ROOT / ".github/workflows/coordination-v4-broker.yml").read_text(encoding="utf-8")
    importer_wf = (ROOT / ".github/workflows/import-generated-assets.yml").read_text(encoding="utf-8")
    repair_wf = (ROOT / ".github/workflows/identity-repair.yml").read_text(encoding="utf-8")

    # Regression for production run #15: optional/missing pathspecs made
    # `git add ... || true` silently stage nothing after a valid broker apply.
    assert "git add -A" in broker_wf
    assert "git add coordination/state.json" not in broker_wf

    # All Actions that can write canonical main must serialize through one lock.
    for name, text in {
        "broker": broker_wf,
        "binary importer": importer_wf,
        "identity repair": repair_wf,
    }.items():
        assert "group: alisa-main-writer" in text, f"{name} missing shared main-writer lock"


def main() -> None:
    run([sys.executable, "coordination/validate_state.py"])
    assert_workflow_guards()

    # Pure validation/dry-run guards.
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

    # Local two-agent state-machine smoke. This mutates only the ephemeral CI checkout,
    # never pushes, then restores the checkout before the test exits.
    baseline = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    try:
        first = write_tmp(
            proposal(
                message_id="gk-v4-e2e-complete",
                outcome="completed",
                summary="Grok half of v4 e2e smoke",
                handoff_body="Broker should route QA to ChatGPT.",
            )
        )
        run([sys.executable, str(VALIDATE), str(first)])
        run([sys.executable, str(BROKER), str(first), "--apply"])
        s1 = read_state()
        assert s1["turn_id"] == 1
        assert s1["active_task"] == "coordination-v4-e2e-smoke"
        assert s1["task_status"] == "qa_pending"
        assert s1["next_actor"] == "chatgpt"
        run([sys.executable, "coordination/validate_state.py"])

        second = write_tmp(
            proposal(
                message_id="cg-v4-e2e-qa-pass",
                outcome="qa_pass",
                summary="ChatGPT QA half of v4 e2e smoke",
                handoff_body="Smoke passed; scheduler should enter idle because remaining tasks are blocked.",
            )
        )
        run([sys.executable, str(VALIDATE), str(second)])
        run([sys.executable, str(BROKER), str(second), "--apply"])
        s2 = read_state()
        assert s2["turn_id"] == 2
        assert s2["active_task"] is None
        assert s2["task_status"] == "idle"
        assert s2["next_actor"] is None
        assert s2["scheduler"]["idle_reason"] == "no_runnable_task"
        run([sys.executable, "coordination/validate_state.py"])
    finally:
        subprocess.run(["git", "reset", "--hard", baseline], cwd=ROOT, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "clean", "-fd", "coordination/messages", "coordination/proposals"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    print("Coordination v4 guard + two-turn broker smoke tests OK")


if __name__ == "__main__":
    main()
