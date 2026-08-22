#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "coordination" / "state.json"
ALLOWED_ACTORS = {"chatgpt", "grok"}
ALLOWED_STATUS = {
    "waiting_for_grok",
    "waiting_for_chatgpt",
    "in_progress_grok",
    "in_progress_chatgpt",
    "blocked_binary",
    "blocked_tooling",
    "qa_pending",
    "completed",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MESSAGE_ID_RE = re.compile(r"Message ID:\s*`?([A-Za-z0-9._:-]+)`?")


def fail(msg: str) -> None:
    raise SystemExit(f"AI handoff validation failed: {msg}")


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
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def load_state(path: Path = STATE) -> dict:
    if not path.exists():
        fail("coordination/state.json is missing")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail("state root must be an object")
    return data


def validate_message(data: dict) -> None:
    message_path = data.get("message_path")
    if not isinstance(message_path, str) or not message_path.startswith("coordination/messages/"):
        fail("message_path must point under coordination/messages/")
    msg = (ROOT / message_path).resolve()
    try:
        msg.relative_to((ROOT / "coordination" / "messages").resolve())
    except ValueError:
        fail("message_path escapes coordination/messages/")
    if not msg.exists():
        fail(f"message_path does not exist: {message_path}")

    text = msg.read_text(encoding="utf-8")
    match = MESSAGE_ID_RE.search(text)
    if not match:
        fail("message file has no Message ID")
    message_id = match.group(1)

    next_actor = data["next_actor"]
    if next_actor == "grok":
        if "Recipient: Grok" not in text:
            fail("state says next_actor=grok but current message is not addressed to Grok")
        if not message_id.startswith("cg-"):
            fail("message addressed to Grok must originate from ChatGPT (cg- Message ID)")
        if data.get("last_chatgpt_message_id") != message_id:
            fail("last_chatgpt_message_id does not match current handoff Message ID")
    else:
        if "Recipient: ChatGPT" not in text:
            fail("state says next_actor=chatgpt but current message is not addressed to ChatGPT")
        if not message_id.startswith("gk-"):
            fail("message addressed to ChatGPT must originate from Grok (gk- Message ID)")
        if data.get("last_grok_message_id") != message_id:
            fail("last_grok_message_id does not match current handoff Message ID")


def validate_common(data: dict) -> None:
    required = {
        "schema_version",
        "updated_at",
        "active_task",
        "status",
        "next_actor",
        "message_path",
        "last_chatgpt_message_id",
        "last_grok_message_id",
    }
    missing = sorted(required - set(data))
    if missing:
        fail(f"missing keys: {', '.join(missing)}")

    if data["next_actor"] not in ALLOWED_ACTORS:
        fail(f"unsupported next_actor: {data['next_actor']}")
    if data["status"] not in ALLOWED_STATUS:
        fail(f"unsupported status: {data['status']}")
    if data.get("requires_user") is True:
        fail("requires_user=true is forbidden")

    try:
        datetime.fromisoformat(str(data["updated_at"]).replace("Z", "+00:00"))
    except ValueError:
        fail("updated_at must be an ISO-8601 datetime")

    if not isinstance(data["active_task"], str) or not data["active_task"].strip():
        fail("active_task must be a non-empty string")

    validate_message(data)


def validate_v2(data: dict) -> None:
    if data["schema_version"] != 2:
        fail("legacy validator called with non-v2 state")


def validate_v3(data: dict) -> None:
    required = {
        "turn_id",
        "parent_state_sha",
        "hop_count",
        "hop_limit",
        "target_ref",
        "broker",
        "blocker_fingerprint",
        "notes",
    }
    missing = sorted(required - set(data))
    if missing:
        fail(f"v3 missing keys: {', '.join(missing)}")

    if not isinstance(data["turn_id"], int) or data["turn_id"] < 1:
        fail("turn_id must be an integer >= 1")
    if not isinstance(data["parent_state_sha"], str) or not SHA_RE.fullmatch(data["parent_state_sha"]):
        fail("parent_state_sha must be a 40-char lowercase Git SHA")
    if not isinstance(data["hop_count"], int) or data["hop_count"] < 0:
        fail("hop_count must be an integer >= 0")
    if not isinstance(data["hop_limit"], int) or not (1 <= data["hop_limit"] <= 100):
        fail("hop_limit must be between 1 and 100")
    if data["hop_count"] > data["hop_limit"]:
        fail("hop_count exceeds hop_limit")
    if not isinstance(data["target_ref"], str) or not data["target_ref"].strip():
        fail("target_ref must be non-empty")

    broker = data["broker"]
    if not isinstance(broker, dict):
        fail("broker must be an object")
    if set(broker) != {"mode", "lease_owner", "lease_expires_at"}:
        fail("broker must contain exactly mode, lease_owner, lease_expires_at")
    if broker["mode"] not in {"dry_run", "product_mailbox"}:
        fail("broker.mode must be dry_run or product_mailbox")
    if broker["lease_owner"] is not None and not isinstance(broker["lease_owner"], str):
        fail("broker.lease_owner must be string or null")
    if broker["lease_expires_at"] is not None:
        if not isinstance(broker["lease_expires_at"], str):
            fail("broker.lease_expires_at must be string or null")
        try:
            datetime.fromisoformat(broker["lease_expires_at"].replace("Z", "+00:00"))
        except ValueError:
            fail("broker.lease_expires_at must be ISO-8601")

    fp = data["blocker_fingerprint"]
    if fp is not None and (not isinstance(fp, str) or not fp.strip()):
        fail("blocker_fingerprint must be null or non-empty string")

    semantic = {
        "waiting_for_grok": "grok",
        "in_progress_grok": "grok",
        "waiting_for_chatgpt": "chatgpt",
        "in_progress_chatgpt": "chatgpt",
    }
    expected = semantic.get(data["status"])
    if expected and data["next_actor"] != expected:
        fail(f"status {data['status']} requires next_actor={expected}")


def validate_git_transition(data: dict) -> None:
    previous_blob = git("rev-parse", "HEAD^:coordination/state.json")
    changed = subprocess.run(
        ["git", "diff", "--quiet", "HEAD^", "HEAD", "--", "coordination/state.json"],
        cwd=ROOT,
        check=False,
    ).returncode != 0

    if not changed:
        return

    if data["schema_version"] != 3:
        fail("a state transition commit on the v3 branch must produce schema_version=3")
    if data["parent_state_sha"] != previous_blob:
        fail("stale transition: parent_state_sha does not match previous state blob")

    previous = json.loads(git("show", "HEAD^:coordination/state.json"))
    previous_turn = int(previous.get("turn_id", 0))
    if data["turn_id"] != previous_turn + 1:
        fail(f"turn_id must increment exactly by 1 from {previous_turn}")

    if previous.get("schema_version") == 3:
        if data["active_task"] == previous.get("active_task"):
            expected_hops = int(previous.get("hop_count", 0)) + 1
            if data["hop_count"] != expected_hops:
                fail(f"hop_count must increment to {expected_hops} for same active_task")
        elif data["hop_count"] != 0:
            fail("hop_count must reset to 0 when active_task changes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--git-transition",
        action="store_true",
        help="also validate this commit against HEAD^ state.json",
    )
    args = parser.parse_args()

    data = load_state()
    validate_common(data)
    if data["schema_version"] == 2:
        validate_v2(data)
    elif data["schema_version"] == 3:
        validate_v3(data)
    else:
        fail("schema_version must be 2 or 3 during migration")

    if args.git_transition:
        validate_git_transition(data)

    print(
        "AI handoff OK:",
        f"schema={data['schema_version']}",
        f"task={data['active_task']}",
        f"status={data['status']}",
        f"next_actor={data['next_actor']}",
        f"message={data['message_path']}",
        f"turn={data.get('turn_id', 'legacy')}",
    )


if __name__ == "__main__":
    main()
