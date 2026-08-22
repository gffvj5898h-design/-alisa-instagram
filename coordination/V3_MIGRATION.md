# Coordination v3 migration

Branch: `coordination-v3-prototype`

Purpose: test broker-owned ChatGPT ↔ Grok coordination without changing the working `main` handoff and without requiring model API billing.

## Product decision — 2026-08-22

OpenAI API is explicitly out of scope. The intended automation uses the existing ChatGPT product plus the Grok product, their authenticated GitHub access, GitHub Actions and product-side routines/polling.

No `OPENAI_API_KEY` is required. The design also does not require an xAI model API call for normal handoff.

## What changed in the prototype

- `coordination/state.json` migrated from schema v2 to v3.
- Added `coordination/state.schema.json`.
- Added `coordination/agent_response.schema.json`.
- Added `coordination/broker_policy.json`.
- Added `coordination/PROTOCOL_V3.md`.
- Added `coordination/proposals/` as the only direct coordination inbox written by product agents.
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
- Added `coordination/broker.py` envelope builder for product-mailbox operation.
- Added `coordination/apply_turn.py`: validates an agent proposal, defaults to dry-run, and only with explicit `--apply` writes allowed work-product files plus broker-owned handoff/state.
- Added `coordination/test_v3_guards.py` for positive/negative safety checks.
- Added `.github/workflows/ai-broker-v3.yml` to validate/build the dispatch envelope.
- Added `.github/workflows/ai-proposal-apply-v3.yml` to validate product-agent proposal commits and, only in `product_mailbox` mode, apply the canonical transition.
- Updated handoff CI to compile coordination scripts, validate transitions, run broker guard tests and verify routing envelopes.
- Path policy permits the required `GROK_CONTEXT_AND_LOG.md` project-log update while keeping coordination internals and canonical identity protected.

## Current safety state

`broker.mode = dry_run`.

The broker can build a deterministic dispatch envelope and validate a proposal, but product proposals do not alter canonical state until the mode is deliberately switched to `product_mailbox`.

No model API key is required by this prototype. No API credential may be committed to the repository.

## How no-API automation works

### ChatGPT side

A ChatGPT condition-watch checks the repository periodically. If `next_actor != chatgpt`, it does nothing. If `next_actor == chatgpt`, it reads the handoff, performs the task with available product tools and creates exactly one new proposal JSON under `coordination/proposals/`.

The current ChatGPT task scheduler supports hourly condition-watch as the highest polling frequency in this environment. This creates latency, but no manual message relay and no separate OpenAI API billing.

### Grok side

Use Grok's authenticated GitHub connector plus a Grok Bot routine where available. xAI documentation states that routines may run on schedules and, for supported account integrations, after events such as a GitHub notification. Configure a narrow repository/coordination event rule rather than a broad listener. If event trigger is unavailable for the account, use a periodic routine.

The Grok product agent follows the same rule: it writes a proposal JSON only and never edits canonical state/messages directly.

### GitHub side

`ai-proposal-apply-v3.yml` is the single-writer bridge:

1. detect exactly one newly created proposal;
2. serialize proposal-apply runs with GitHub Actions concurrency;
3. validate current state;
4. validate proposal against exact current state SHA;
5. in `dry_run`, show plan only;
6. in `product_mailbox`, apply work files + canonical message + state;
7. commit as `github-actions[bot]`;
8. validate the committed state transition.

A second proposal created from an old state fails as stale after the first accepted transition.

## Why `main` is not migrated yet

`main` has a live schema-v2 handoff. Replacing it before validating v3 would risk breaking the existing ChatGPT ↔ Grok mailbox.

The prototype preserves the current active task/message but isolates schema/workflow changes on its own branch.

## Tests before activation

1. CI structural test for v3 state.
2. CI v2→v3 transition test.
3. Python compile test.
4. Broker envelope shows the correct `next_actor`, `active_task`, state SHA and next `turn_id`.
5. Stale `expected_parent_state_sha` rejected.
6. Model operation targeting `coordination/state.json` rejected.
7. Model operation targeting canonical Alice face rejected.
8. Repeated same `blocker_fingerprint` rejected.
9. `hop_limit` stops another dispatch.
10. Two proposals from one state: only one can become canonical.
11. Proposal workflow in `dry_run` validates one real disposable proposal without applying it.
12. `product_mailbox` apply tested on a disposable work-product path before production activation.

## Recommended activation sequence

### Phase 1 — current branch

Keep `dry_run`; CI/guard tests only.

### Phase 2 — real product-agent proposal

Have ChatGPT or Grok create one harmless disposable proposal under `coordination/proposals/`. Confirm GitHub Actions validates it and makes no canonical changes.

### Phase 3 — broker apply test

On a disposable task/path, switch the prototype state to `product_mailbox`, set a low `hop_limit`, submit one proposal and verify broker application plus stale/race rejection.

### Phase 4 — two-product handoff

Run `ChatGPT product → proposal → GitHub broker → Grok product → proposal → GitHub broker`, still on the prototype branch.

### Phase 5 — production handoff

Only after review: migrate `main` state to v3, make the GitHub broker the sole canonical coordination writer, update/enable ChatGPT polling and configure the Grok routine for `main`.

## Rollback

Because the prototype is isolated, rollback is simply: do not merge the branch. `main` remains on the existing v2 coordination protocol.
