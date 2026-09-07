#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
TASKS = ROOT / "coordination" / "tasks.json"
CAPS = ROOT / "coordination" / "capabilities.json"
VALIDATE_STATE = ROOT / "coordination" / "validate_state.py"

ALLOWED_ACTORS = {"chatgpt", "grok"}
ALLOWED_CONTEXT_PREFIXES = ("content/briefs/", "content/reels/")
ALLOWED_CONTEXT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}


def fail(msg: str) -> None:
    raise SystemExit(f"Coordination v4 human intake failed: {msg}")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        fail(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def safe_slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower()
    return value[:96] or "human-intake"


def validate_context_path(value: str) -> None:
    if not isinstance(value, str) or not value:
        fail("context file path must be a non-empty string")
    if value.startswith("/") or ".." in Path(value).parts:
        fail(f"context path traversal rejected: {value}")
    if not value.startswith(ALLOWED_CONTEXT_PREFIXES):
        fail(f"context path outside human-input prefixes: {value}")
    if Path(value).suffix.lower() not in ALLOWED_CONTEXT_EXTENSIONS:
        fail(f"unsupported context extension: {value}")


def validate_task(task: dict, known_caps: dict) -> None:
    required = {
        "id", "description", "priority", "status", "requires", "dependencies",
        "preferred_actor", "qa_actor", "attempts", "max_attempts", "blocked_on",
        "blocker_fingerprint",
    }
    missing = sorted(required - set(task))
    if missing:
        fail(f"task missing fields {missing}: {task.get('id')}")
    if not isinstance(task["id"], str) or not task["id"]:
        fail("task id must be a non-empty string")
    if task["status"] != "ready":
        fail(f"human intake may add only ready tasks: {task['id']}")
    if task["preferred_actor"] is not None and task["preferred_actor"] not in ALLOWED_ACTORS:
        fail(f"invalid preferred_actor for {task['id']}")
    if task["qa_actor"] is not None and task["qa_actor"] not in ALLOWED_ACTORS:
        fail(f"invalid qa_actor for {task['id']}")
    if not isinstance(task["requires"], list) or not all(isinstance(x, str) for x in task["requires"]):
        fail(f"requires must be a string list for {task['id']}")
    if not isinstance(task["dependencies"], list) or not all(isinstance(x, str) for x in task["dependencies"]):
        fail(f"dependencies must be a string list for {task['id']}")
    if not isinstance(task["attempts"], int) or task["attempts"] != 0:
        fail(f"new task attempts must be 0: {task['id']}")
    if not isinstance(task["max_attempts"], int) or task["max_attempts"] < 1:
        fail(f"invalid max_attempts: {task['id']}")
    if task["blocked_on"] != [] or task["blocker_fingerprint"] is not None:
        fail(f"new task cannot enter pre-blocked: {task['id']}")

    probe = task.get("capability_probe")
    if probe is not None:
        if not isinstance(probe, dict) or set(probe) != {"actor", "capability"}:
            fail(f"invalid capability_probe metadata: {task['id']}")
        actor = probe["actor"]
        cap = probe["capability"]
        if actor not in ALLOWED_ACTORS:
            fail(f"invalid capability probe actor: {task['id']}")
        if cap not in known_caps.get("actors", {}).get(actor, {}):
            fail(f"unknown capability in probe: {task['id']} -> {actor}.{cap}")
        if cap in task["requires"]:
            fail(f"probe cannot require capability being tested: {task['id']}")
        if task["preferred_actor"] != actor:
            fail(f"probe preferred_actor must equal probe actor: {task['id']}")
        if task["qa_actor"] is None or task["qa_actor"] == actor:
            fail(f"probe requires independent qa_actor: {task['id']}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: apply_human_intake.py /path/to/intake.json")

    subprocess.run([sys.executable, str(VALIDATE_STATE)], cwd=ROOT, check=True)
    intake_path = Path(sys.argv[1]).resolve()
    intake = load(intake_path)
    state = load(STATE)
    tasks_doc = load(TASKS)
    caps = load(CAPS)

    if state.get("task_status") != "idle" or state.get("next_actor") is not None:
        fail("human intake is accepted only while canonical scheduler is idle")
    if intake.get("schema_version") != 1:
        fail("schema_version must be 1")
    intake_id = intake.get("intake_id")
    if not isinstance(intake_id, str) or not intake_id:
        fail("intake_id must be a non-empty string")
    summary = intake.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        fail("summary must be non-empty")
    tasks = intake.get("tasks")
    context_files = intake.get("context_files", [])
    if not isinstance(tasks, list) or not tasks:
        fail("tasks must be a non-empty list")
    if not isinstance(context_files, list):
        fail("context_files must be a list")

    archive_rel = f"coordination/intakes/{safe_slug(intake_id)}.json"
    if (ROOT / archive_rel).exists():
        fail(f"duplicate intake_id already archived: {intake_id}")

    existing_tasks = deepcopy(tasks_doc["tasks"])
    existing_ids = {t["id"] for t in existing_tasks}
    new_ids: list[str] = []
    for task in tasks:
        if not isinstance(task, dict):
            fail("every task must be an object")
        validate_task(task, caps)
        tid = task["id"]
        if tid in existing_ids or tid in new_ids:
            fail(f"duplicate task id: {tid}")
        new_ids.append(tid)

    all_ids = existing_ids | set(new_ids)
    for task in tasks:
        missing_deps = [dep for dep in task["dependencies"] if dep not in all_ids]
        if missing_deps:
            fail(f"unknown dependencies for {task['id']}: {missing_deps}")

    seen_context: set[str] = set()
    for item in context_files:
        if not isinstance(item, dict) or set(item) != {"path", "content"}:
            fail("context file must contain exactly path/content")
        validate_context_path(item["path"])
        if item["path"] in seen_context:
            fail(f"duplicate context path: {item['path']}")
        seen_context.add(item["path"])
        if not isinstance(item["content"], str):
            fail(f"context content must be UTF-8 text: {item['path']}")
        target = ROOT / item["path"]
        if target.exists():
            fail(f"human intake refuses to overwrite existing context file: {item['path']}")

    merged_tasks = existing_tasks + deepcopy(tasks)
    # Import after validation so the intake path cannot influence module loading.
    from broker import schedule_next  # type: ignore

    next_task, next_actor, idle_reason = schedule_next(merged_tasks, caps)
    now = datetime.now(timezone(timedelta(hours=3)))
    parent_blob = git("hash-object", "coordination/state.json")
    next_state = deepcopy(state)
    next_state["turn_id"] = int(state["turn_id"]) + 1
    next_state["updated_at"] = now.isoformat(timespec="seconds")
    next_state["parent_state_sha"] = parent_blob
    next_state["notes"] = summary.strip()
    next_state["scheduler"] = {"mode": "broker_v4", "idle_reason": idle_reason}
    next_state["blocker_fingerprint"] = None

    if next_task is None:
        next_state["active_task"] = None
        next_state["task_status"] = "idle"
        next_state["next_actor"] = None
    else:
        next_state["active_task"] = next_task["id"]
        next_state["task_status"] = next_task["status"]
        next_state["next_actor"] = next_actor
        next_state["blocker_fingerprint"] = next_task.get("blocker_fingerprint")

    recipient = "ChatGPT" if next_actor == "chatgpt" else "Grok" if next_actor == "grok" else "Scheduler"
    stamp = now.strftime("%Y%m%d-%H%M%S")
    msg_rel = f"coordination/messages/{stamp}-human-intake-{safe_slug(intake_id)}-t{next_state['turn_id']}.md"
    next_state["message_path"] = msg_rel
    message = (
        f"# Human intake event — turn {next_state['turn_id']}\n\n"
        f"- Message ID: `{intake_id}`\n"
        f"- Actor: `human`\n"
        f"- Recipient: {recipient}\n"
        f"- Next task: `{next_state['active_task'] or 'idle'}`\n"
        f"- Parent state SHA: `{parent_blob}`\n\n"
        f"## Summary\n\n{summary.strip()}\n\n"
        f"## Added tasks\n\n" + "\n".join(f"- `{tid}`" for tid in new_ids) + "\n"
    )

    for item in context_files:
        target = ROOT / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item["content"], encoding="utf-8")

    write_json(TASKS, {"schema_version": 1, "tasks": merged_tasks})
    write_json(STATE, next_state)
    archive = ROOT / archive_rel
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(json.dumps(intake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    message_path = ROOT / msg_rel
    message_path.parent.mkdir(parents=True, exist_ok=True)
    message_path.write_text(message, encoding="utf-8")

    subprocess.run([sys.executable, str(VALIDATE_STATE)], cwd=ROOT, check=True)
    print(
        "Human intake applied:",
        f"id={intake_id}",
        f"tasks={len(new_ids)}",
        f"next_task={next_state['active_task']}",
        f"next_actor={next_state['next_actor']}",
    )


if __name__ == "__main__":
    main()
