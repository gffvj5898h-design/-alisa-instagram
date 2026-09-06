# Coordination v4 operator summary

- Canonical production state lives on `main`.
- Product agents are workers, not canonical state writers.
- Agent output is one proposal JSON on branch `coordination-inbox` under `coordination/inbox/`.
- GitHub Actions broker is the single canonical writer.
- Proposals are bound to exact state blob SHA and next turn id.
- Scheduler selects the next runnable task from structured `coordination/tasks.json` using dependencies and verified capabilities.
- Idle means `next_actor=null`; there are no self-handoffs.
- Binary assets use the separate import data plane and independent per-manifest processing.
- Normal proposals cannot mutate coordination internals, workflows, executable production code or canonical identity.
