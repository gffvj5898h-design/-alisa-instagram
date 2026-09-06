# ChatGPT ↔ Grok automation — protocol v4

## Runtime model

Both product agents are workers, not transaction managers.

- `main/coordination/state.json` is the canonical scheduler snapshot.
- Each product wakes on its own supported schedule/routine.
- If `next_actor` does not match, it performs no repo write.
- If it matches, it performs the assigned task and submits exactly one proposal to branch `coordination-inbox` under `coordination/inbox/*.json`.
- GitHub Actions broker is the sole writer of canonical coordination state/tasks/messages and allowed text work products on `main`.

No OpenAI API or xAI model API is required.

## ChatGPT routine

On each run:

1. read `main/PROJECT_INSTRUCTIONS.md`, `coordination/PROTOCOL.md`, `coordination/state.json`, `coordination/tasks.json`, `coordination/capabilities.json`, and the current message;
2. act only for `next_actor=chatgpt`;
3. re-read state immediately before submitting;
4. create one schema-v4 proposal on `coordination-inbox` bound to the exact current state blob SHA and `turn_id+1`;
5. never directly update canonical coordination files;
6. notify the user only for a completed substantive turn, material blocker, or decision.

## Grok routine

Use the same algorithm for `next_actor=grok`. Hourly polling is acceptable. Do not hardcode v2/v3 behavior; read the active protocol from `main` every run.

## Health

`state.agent_last_seen` is updated by the broker when a valid proposal is accepted. It is not a product wake heartbeat. A future watchdog may alert on stale workers, but absence of a proposal is not itself a state transition.

## Idle

When no task is runnable, broker sets:

- `active_task=null`
- `task_status=idle`
- `next_actor=null`

There are no self-handoffs and no blocker ping-pong.
