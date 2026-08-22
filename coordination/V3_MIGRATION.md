# Coordination v3 migration

Branch: `coordination-v3-prototype`

Purpose: test broker-owned ChatGPT ↔ Grok coordination without changing the working `main` handoff.

## What changed in the prototype

- `coordination/state.json` migrated from schema v2 to v3.
- Added `coordination/state.schema.json`.
- Added `coordination/agent_response.schema.json`.
- Added `coordination/broker_policy.json`.
- Added `coordination/PROTOCOL_V3.md`.
- Strengthened `coordination/validate_state.py`:
  - keeps v2 readable during migration;
  - validates v3 fields;
  - validates sender/recipient Message ID consistency;
  - optional Git transition check against `HEAD^`;
  - checks `parent_state_sha` and monotonic `turn_id`;
  - checks `hop_count` progression.
- Added `coordination/validate_agent_response.py`:
  - binds proposal to exact state blob SHA;
  - verifies actor ownership and next turn id;
  - rejects protected/broker-owned paths;
  - rejects path traversal/duplicate operations;
  - requires blocker fingerprint for blocked proposals;
  - rejects identical blocker ping-pong.
- Added `coordination/broker.py` dry-run dispatcher.
- Added `coordination/apply_turn.py`: validates an agent proposal, defaults to dry-run, and only with explicit `--apply` writes allowed work-product files plus broker-owned handoff/state.
- Added `coordination/test_v3_guards.py` for positive/negative safety checks.
- Added `.github/workflows/ai-broker-v3.yml` dry-run workflow.
- Updated handoff CI to compile the coordination scripts, validate transitions and run broker guard tests.
- Path policy permits the required `GROK_CONTEXT_AND_LOG.md` project-log update while keeping coordination internals and canonical identity protected.

## Current safety state

`broker.mode = dry_run`.

The broker can build a deterministic dispatch envelope for `next_actor`, but it cannot call OpenAI or xAI and the workflow does not autonomously apply model writes. `apply_turn.py` also defaults to no-write dry-run unless `--apply` is supplied explicitly.

No API key is required by the prototype. No API credential may be committed to the repository.

## Why `main` is not migrated yet

`main` has a live schema-v2 handoff. Replacing it before validating v3 would risk breaking the existing ChatGPT ↔ Grok mailbox.

The prototype preserves the current active task/message but isolates schema/workflow changes on its own branch.

## Tests required before live mode

1. CI structural test for v3 state.
2. CI v2→v3 transition test.
3. Python compile test.
4. Dry-run broker envelope shows the correct `next_actor`, `active_task`, state SHA and next `turn_id`.
5. Negative test: stale `expected_parent_state_sha` rejected.
6. Negative test: model operation targeting `coordination/state.json` rejected.
7. Negative test: model operation targeting canonical Alice face rejected.
8. Negative test: repeated same `blocker_fingerprint` rejected.
9. Negative test: `hop_limit` stops another dispatch.
10. Race test: two proposals created from one state; only the first accepted state transition may win.

## Live adapter design

Do not connect the current ChatGPT/Grok product chats directly. Live realtime automation should use API agents whose context is bootstrapped from GitHub.

Expected GitHub secrets (names only; values never committed):

- `OPENAI_API_KEY`
- `XAI_API_KEY`

Expected repository/environment variables when adapters are implemented:

- `OPENAI_MODEL`
- `XAI_MODEL`
- spend/rate ceilings
- live broker enable flag

The exact model identifiers and API request/response handling must be verified against current provider documentation at implementation time; they are intentionally not hard-coded in this dry-run prototype.

## Recommended activation sequence

### Phase 1 — current branch

Dry-run only. Validate state machine and policy.

### Phase 2 — one-sided API smoke test

Enable one adapter on a disposable test task with `hop_limit=1`; model returns proposal JSON only. Broker does not write production files.

### Phase 3 — broker apply on test prefix

Allow writes only under a disposable test directory. Verify stale-state/race rejection.

### Phase 4 — two-agent loop

OpenAI ↔ GitHub broker ↔ xAI with `hop_limit=4`, strict cost ceiling and no protected paths.

### Phase 5 — production handoff

Only after review: migrate `main` state to v3, make broker the sole coordination writer, then retire direct agent edits of `state.json`.

## Rollback

Because the prototype is isolated, rollback is simply: do not merge the branch. `main` remains on the existing v2 coordination protocol.
