#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
TASKS = ROOT / "coordination" / "tasks.json"
CAPABILITIES = ROOT / "coordination" / "capabilities.json"
ALLOWED_ACTORS = {"chatgpt", "grok"}
ALLOWED_TASK_STATUS = {"ready", "in_progress", "qa_pending", "blocked", "completed", "idle"}


def fail(msg: str) -> None:
    raise SystemExit(f"Coordination v4 state validation failed: {msg}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        fail(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def main() -> None:
    for path in (STATE, TASKS, CAPABILITIES):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    state = load_json(STATE)
    tasks_doc = load_json(TASKS)
    caps = load_json(CAPABILITIES)

    required = {
        "schema_version", "turn_id", "updated_at", "active_task", "task_status",
        "next_actor", "message_path", "last_chatgpt_message_id", "last_grok_message_id",
        "parent_state_sha", "blocker_fingerprint", "scheduler", "agent_last_seen", "notes",
    }
    missing = sorted(required - set(state))
    if missing:
        fail(f"missing state keys: {', '.join(missing)}")
    if state["schema_version"] != 4:
        fail("schema_version must be 4")
    if not isinstance(state["turn_id"], int) or state["turn_id"] < 0:
        fail("turn_id must be a non-negative integer")
    if state["task_status"] not in ALLOWED_TASK_STATUS:
        fail(f"invalid task_status: {state['task_status']}")
    if state["next_actor"] is not None and state["next_actor"] not in ALLOWED_ACTORS:
        fail(f"invalid next_actor: {state['next_actor']}")
    if state.get("scheduler", {}).get("mode") != "broker_v4":
        fail("scheduler.mode must be broker_v4")

    if tasks_doc.get("schema_version") != 1 or not isinstance(tasks_doc.get("tasks"), list):
        fail("coordination/tasks.json has unsupported schema")
    task_map = {}
    for task in tasks_doc["tasks"]:
        tid = task.get("id")
        if not isinstance(tid, str) or not tid:
            fail("task without valid id")
        if tid in task_map:
            fail(f"duplicate task id: {tid}")
        task_map[tid] = task

    actors = caps.get("actors")
    if caps.get("schema_version") != 1 or not isinstance(actors, dict):
        fail("coordination/capabilities.json has unsupported schema")
    if set(actors) != ALLOWED_ACTORS:
        fail("capabilities actors must be exactly chatgpt and grok")

    active = state["active_task"]
    if active is None:
        if state["task_status"] != "idle":
            fail("active_task=null requires task_status=idle")
        if state["next_actor"] is not None:
            fail("idle state requires next_actor=null")
    else:
        if active not in task_map:
            fail(f"active_task missing from task DB: {active}")
        task = task_map[active]
        if task.get("status") != state["task_status"]:
            fail(
                f"state/task status mismatch for {active}: "
                f"state={state['task_status']} tasks={task.get('status')}"
            )
        if state["task_status"] in {"ready", "in_progress", "qa_pending"} and state["next_actor"] is None:
            fail(f"{state['task_status']} requires next_actor")
        if state["task_status"] in {"blocked", "completed"} and state["next_actor"] is not None:
            fail(f"{state['task_status']} must not retain next_actor")

    message_path = state["message_path"]
    if message_path is not None:
        if not isinstance(message_path, str) or not message_path.startswith("coordination/messages/"):
            fail("message_path must be null or live under coordination/messages/")
        msg = (ROOT / message_path).resolve()
        try:
            msg.relative_to(ROOT / "coordination" / "messages")
        except ValueError:
            fail("message_path escapes coordination/messages/")
        if not msg.is_file():
            fail(f"message_path does not exist: {message_path}")
        text = msg.read_text(encoding="utf-8")
        if "Message ID:" not in text:
            fail("current message has no Message ID")
        if state["next_actor"] == "chatgpt" and "Recipient: ChatGPT" not in text:
            fail("next_actor=chatgpt but message recipient differs")
        if state["next_actor"] == "grok" and "Recipient: Grok" not in text:
            fail("next_actor=grok but message recipient differs")
    elif state["next_actor"] is not None:
        fail("non-idle next_actor requires message_path")

    if "--git-transition" in sys.argv:
        try:
            parent_text = git("show", "HEAD^:coordination/state.json")
        except SystemExit:
            parent_text = ""
        if parent_text:
            parent = json.loads(parent_text)
            parent_blob = git("rev-parse", "HEAD^:coordination/state.json")
            if state["turn_id"] != parent.get("turn_id", -1) + 1:
                fail("turn_id must increment exactly by one")
            if state["parent_state_sha"] != parent_blob:
                fail("parent_state_sha must equal parent state blob SHA")

    print(
        "Coordination v4 state OK:",
        f"turn={state['turn_id']}",
        f"task={state['active_task']}",
        f"status={state['task_status']}",
        f"next_actor={state['next_actor']}",
    )


if __name__ == "__main__":
    main()
