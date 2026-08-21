#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
ALLOWED_ACTORS = {"chatgpt", "grok", "user"}
ALLOWED_STATUS = {
    "waiting_for_grok",
    "waiting_for_chatgpt",
    "waiting_for_user",
    "in_progress_grok",
    "in_progress_chatgpt",
    "blocked_binary",
    "blocked_tooling",
    "qa_pending",
    "completed",
}


def fail(msg: str) -> None:
    raise SystemExit(f"AI handoff validation failed: {msg}")


def main() -> None:
    if not STATE.exists():
        fail("coordination/state.json is missing")

    try:
        data = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON: {exc}")

    required = {
        "schema_version",
        "updated_at",
        "active_task",
        "status",
        "next_actor",
        "message_path",
        "last_chatgpt_message_id",
        "last_grok_message_id",
        "requires_user",
    }
    missing = sorted(required - set(data))
    if missing:
        fail(f"missing keys: {', '.join(missing)}")

    if data["schema_version"] != 1:
        fail("schema_version must be 1")
    if data["next_actor"] not in ALLOWED_ACTORS:
        fail(f"unsupported next_actor: {data['next_actor']}")
    if data["status"] not in ALLOWED_STATUS:
        fail(f"unsupported status: {data['status']}")
    if not isinstance(data["requires_user"], bool):
        fail("requires_user must be boolean")

    message_path = data["message_path"]
    if not isinstance(message_path, str) or not message_path.startswith("coordination/messages/"):
        fail("message_path must point under coordination/messages/")
    msg = (ROOT / message_path).resolve()
    try:
        msg.relative_to(ROOT / "coordination" / "messages")
    except ValueError:
        fail("message_path escapes coordination/messages/")
    if not msg.exists():
        fail(f"message_path does not exist: {message_path}")

    text = msg.read_text(encoding="utf-8")
    if "Message ID:" not in text:
        fail("message file has no Message ID")
    if data["next_actor"] == "grok" and "Recipient: Grok" not in text:
        fail("state says next_actor=grok but current message is not addressed to Grok")
    if data["next_actor"] == "chatgpt" and "Recipient: ChatGPT" not in text:
        fail("state says next_actor=chatgpt but current message is not addressed to ChatGPT")

    print(
        "AI handoff OK:",
        f"task={data['active_task']}",
        f"status={data['status']}",
        f"next_actor={data['next_actor']}",
        f"message={message_path}",
    )


if __name__ == "__main__":
    main()
