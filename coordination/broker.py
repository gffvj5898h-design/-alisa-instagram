#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
VALIDATE_PROPOSAL = ROOT / "coordination" / "validate_proposal.py"
VALIDATE_STATE = ROOT / "coordination" / "validate_state.py"


def fail(msg: str) -> None:
    raise SystemExit(f"Coordination v4 broker failed: {msg}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        fail(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def actor_capable(actor: str, task: dict, caps: dict) -> bool:
    values = caps.get("actors", {}).get(actor, {})
    return all(values.get(req) is True for req in task.get("requires", []))


def capable_actors(task: dict, caps: dict) -> list[str]:
    return [a for a in ("chatgpt", "grok") if actor_capable(a, task, caps)]


def deps_complete(task: dict, task_map: dict[str, dict]) -> bool:
    return all(task_map.get(dep, {}).get("status") == "completed" for dep in task.get("dependencies", []))


def refresh_capability_blockers(tasks: list[dict], caps: dict) -> None:
    for task in tasks:
        blockers = task.get("blocked_on") or []
        if task.get("status") != "blocked" or not blockers:
            continue
        if all(isinstance(b, str) and b.startswith("capability:") for b in blockers):
            if capable_actors(task, caps):
                task["status"] = "ready"
                task["blocked_on"] = []
                task["blocker_fingerprint"] = None


def schedule_next(tasks: list[dict], caps: dict) -> tuple[dict | None, str | None, str | None]:
    task_map = {t["id"]: t for t in tasks}
    refresh_capability_blockers(tasks, caps)
    candidates = sorted(tasks, key=lambda t: (-int(t.get("priority", 0)), t["id"]))
    for task in candidates:
        if task.get("status") != "ready":
            continue
        if task.get("blocked_on"):
            continue
        if int(task.get("attempts", 0)) >= int(task.get("max_attempts", 1)):
            task["status"] = "blocked"
            task["blocked_on"] = ["attempts:max"]
            task["blocker_fingerprint"] = "attempts:max"
            continue
        if not deps_complete(task, task_map):
            continue
        actors = capable_actors(task, caps)
        if not actors:
            missing = sorted(task.get("requires", []))
            fp = "capability:" + ",".join(missing or ["no_capable_actor"])
            task["status"] = "blocked"
            task["blocked_on"] = [fp]
            task["blocker_fingerprint"] = fp
            continue
        preferred = task.get("preferred_actor")
        actor = preferred if preferred in actors else actors[0]
        return task, actor, None
    return None, None, "no_runnable_task"


def safe_slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower()
    return value[:64] or "event"


def apply(proposal_path: Path, do_apply: bool) -> None:
    subprocess.run([sys.executable, str(VALIDATE_STATE)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(VALIDATE_PROPOSAL), str(proposal_path)], cwd=ROOT, check=True)

    proposal = load(proposal_path)
    state = load(STATE)
    tasks_doc = load(TASKS)
    caps = load(CAPS)
    tasks = deepcopy(tasks_doc["tasks"])
    task_map = {t["id"]: t for t in tasks}
    task = task_map[proposal["task_id"]]
    actor = proposal["actor"]
    outcome = proposal["outcome"]
    now = datetime.now(timezone(timedelta(hours=3)))
    parent_blob = git("hash-object", "coordination/state.json")

    for op in proposal["operations"]:
        target = ROOT / op["path"]
        if do_apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(op["content"], encoding="utf-8")

    if actor != task.get("qa_actor"):
        task["attempts"] = int(task.get("attempts", 0)) + 1

    next_task: dict | None = None
    next_actor: str | None = None
    idle_reason: str | None = None

    if outcome == "completed":
        qa_actor = task.get("qa_actor")
        if qa_actor and qa_actor != actor:
            task["status"] = "qa_pending"
            task["blocked_on"] = []
            task["blocker_fingerprint"] = None
            next_task, next_actor = task, qa_actor
        else:
            task["status"] = "completed"
            task["blocked_on"] = []
            task["blocker_fingerprint"] = None
    elif outcome == "qa_pass":
        task["status"] = "completed"
        task["blocked_on"] = []
        task["blocker_fingerprint"] = None
    elif outcome == "qa_fail":
        task["attempts"] = int(task.get("attempts", 0)) + 1
        if task["attempts"] >= int(task.get("max_attempts", 1)):
            task["status"] = "blocked"
            task["blocked_on"] = ["qa:max_attempts"]
            task["blocker_fingerprint"] = "qa:max_attempts"
        else:
            task["status"] = "ready"
            task["blocked_on"] = []
            task["blocker_fingerprint"] = None
    elif outcome == "blocked":
        fp = proposal["blocker_fingerprint"]
        task["status"] = "blocked"
        task["blocked_on"] = [fp]
        task["blocker_fingerprint"] = fp

    if next_task is None:
        next_task, next_actor, idle_reason = schedule_next(tasks, caps)

    next_state = deepcopy(state)
    next_state["turn_id"] = proposal["turn_id"]
    next_state["updated_at"] = now.isoformat(timespec="seconds")
    next_state["parent_state_sha"] = parent_blob
    next_state["agent_last_seen"] = dict(state.get("agent_last_seen") or {})
    next_state["agent_last_seen"][actor] = now.isoformat(timespec="seconds")
    next_state["notes"] = proposal["summary"]
    next_state["scheduler"] = {"mode": "broker_v4", "idle_reason": idle_reason}

    if next_task is None:
        next_state["active_task"] = None
        next_state["task_status"] = "idle"
        next_state["next_actor"] = None
        next_state["blocker_fingerprint"] = None
    else:
        next_state["active_task"] = next_task["id"]
        next_state["task_status"] = next_task["status"]
        next_state["next_actor"] = next_actor
        next_state["blocker_fingerprint"] = next_task.get("blocker_fingerprint")

    if actor == "chatgpt":
        next_state["last_chatgpt_message_id"] = proposal["message_id"]
    else:
        next_state["last_grok_message_id"] = proposal["message_id"]

    recipient = "ChatGPT" if next_actor == "chatgpt" else "Grok" if next_actor == "grok" else "Scheduler"
    current_task = proposal["task_id"]
    next_task_label = next_state["active_task"] or "idle"
    stamp = now.strftime("%Y%m%d-%H%M%S")
    message_rel = f"coordination/messages/{stamp}-broker-{safe_slug(actor)}-{safe_slug(current_task)}-t{proposal['turn_id']}.md"
    message = (
        f"# Broker event — turn {proposal['turn_id']}\n\n"
        f"- Message ID: `{proposal['message_id']}`\n"
        f"- Actor: `{actor}`\n"
        f"- Completed task: `{current_task}`\n"
        f"- Outcome: `{outcome}`\n"
        f"- Recipient: {recipient}\n"
        f"- Next task: `{next_task_label}`\n"
        f"- Parent state SHA: `{parent_blob}`\n\n"
        f"## Summary\n\n{proposal['summary']}\n\n"
        f"## Handoff\n\n{proposal['handoff_body']}\n"
    )
    next_state["message_path"] = message_rel
    archive_rel = f"coordination/proposals/t{proposal['turn_id']:06d}-{safe_slug(proposal['message_id'])}.json"

    print("Broker plan:")
    print(f"  proposal={proposal_path}")
    print(f"  current_task={current_task}")
    print(f"  outcome={outcome}")
    print(f"  next_task={next_state['active_task']}")
    print(f"  next_actor={next_state['next_actor']}")
    print(f"  event={message_rel}")
    print(f"  archive={archive_rel}")

    if not do_apply:
        print("Dry-run only")
        return

    write_json(TASKS, {"schema_version": 1, "tasks": tasks})
    write_json(STATE, next_state)
    event_path = ROOT / message_rel
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event_path.write_text(message, encoding="utf-8")
    archive = ROOT / archive_rel
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, str(VALIDATE_STATE)], cwd=ROOT, check=True)
    print("Broker applied proposal to working tree")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("proposal")
    ap.add_argument("--apply", action="store_true")
    ns = ap.parse_args()
    apply(Path(ns.proposal).resolve(), ns.apply)


if __name__ == "__main__":
    main()
