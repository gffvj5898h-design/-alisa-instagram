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
- Added `coordination/PRODUCT_MAILBOX.md`.
- Added `coordination/proposals/` as the only direct coordination inbox written by product agents.
- Strengthened `coordination/validate_state.py`:
  - keeps v2 readable during migration;
  - validates v3 fields;
  - validates sender/recipient Message ID consistency;
  - optional Git transition check against the actual branch-head parent;
  - checks `parent_state_sha` and monotonic `turn_id`;
  - checks `hop_count` progression.
- Added `coordination/validate_agent_response.py`:
  - binds proposal to exact state blob SHA;
  - verifies actor ownership and next turn id;
  - rejects protected/broker-owned paths;
  - supports exact allowed work-product files such as `GROK_CONTEXT_AND_LOG.md`;
  - rejects path traversal/duplicate operations;
  - requires blocker fingerprint for blocked proposals;
  - rejects identical blocker ping-pong.
- Added `coordination/broker.py` envelope builder for product-mailbox operation.
- Added `coordination/apply_turn.py`: validates an agent proposal, defaults to dry-run, and only with explicit `--apply` writes allowed work-product files plus broker-owned handoff/state.
- Added `coordination/test_v3_guards.py` for positive/negative safety checks.
- Added `.github/workflows/ai-broker-v3.yml` to validate/build the dispatch envelope.
- Added `.github/workflows/ai-proposal-apply-v3.yml` to validate product-agent proposal commits and, only in `product_mailbox` mode, apply the canonical transition.
- Updated handoff CI to compile coordination scripts, validate transitions, run broker guard tests and verify routing envelopes.

## Current safety state

`broker.mode = dry_run`.

The broker can build a deterministic dispatch envelope and validate a proposal, but product proposals do not alter canonical state until the mode is deliberately switched to `product_mailbox`.

No model API key is required by this prototype. No API credential may be committed to the repository.

## Verified smoke test

On 2026-08-22 this ChatGPT product created a real state-bound proposal through the GitHub connector:

`coordination/proposals/20260822-0853-chatgpt-turn-3-product-mailbox-smoke.json`

It contains no work-product operations and exists only to prove that the product can submit the v3 transport object without an OpenAI API call or direct canonical state/message write.

During this test CI exposed and then fixed a PR-validation bug: pull-request workflows were checking GitHub's synthetic merge ref instead of the actual branch head, which made `HEAD^` the wrong state parent. The workflow now explicitly checks out the PR head SHA before transition validation. The subsequent CI run passed state/transition validation, Python compile, guard tests, broker envelope build and product-mailbox routing verification.

## How no-API automation works

### ChatGPT side

A ChatGPT condition-watch checks the repository periodically. If `next_actor != chatgpt`, it does nothing. If `next_actor == chatgpt`, it reads the handoff, performs the task with available product tools and creates exactly one new proposal JSON under `coordination/proposals/`.

The current ChatGPT task scheduler supports hourly condition-watch as the highest polling frequency in this environment. This creates latency, but no manual message relay and no separate OpenAI API billing.

The previously configured `Grok GitHub Handoff` ChatGPT automation is currently disabled and still contains schema-v2 direct-write instructions; it must not be re-enabled unchanged. Update it to proposal-only behavior after v3 is approved for `main`.

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

1. CI structural test for v3 state — **passed**.
2. CI v2→v3 transition test — **passed**.
3. Python compile test — **passed**.
4. Broker envelope shows correct actor/task/state SHA/next turn — **passed**.
5. Stale `expected_parent_state_sha` rejected — **passed**.
6. Model operation targeting `coordination/state.json` rejected — **passed**.
7. Model operation targeting canonical Alice face rejected — **passed**.
8. Exact allowed `GROK_CONTEXT_AND_LOG.md` path accepted — **passed**.
9. Outside work-product path rejected — **passed**.
10. Repeated same `blocker_fingerprint` rejected — **passed**.
11. `hop_limit` stops another dispatch — **passed**.
12. ChatGPT product can create a conforming real proposal through GitHub — **passed**.
13. Proposal workflow in `dry_run` must validate one real disposable proposal without applying canonical changes — inspect/confirm before activation.
14. `product_mailbox` apply must be tested on a disposable work-product path before production activation.
15. Two proposals from one state: only one can become canonical — test in apply phase.

## Recommended activation sequence

### Phase 1 — current branch

Keep `dry_run`; CI/guard tests and real proposal transport test.

### Phase 2 — broker apply test

On a disposable task/path, switch the prototype state to `product_mailbox`, set a low `hop_limit`, submit one harmless proposal and verify broker application plus stale/race rejection.

### Phase 3 — two-product handoff

Run `ChatGPT product → proposal → GitHub broker → Grok product → proposal → GitHub broker`, still on the prototype branch.

### Phase 4 — production handoff

Only after review: migrate `main` state to v3, make the GitHub broker the sole canonical coordination writer, update/enable ChatGPT polling and configure the Grok routine for `main`.

## Rollback

Because the prototype is isolated, rollback is simply: do not merge the branch. `main` remains on the existing v2 coordination protocol.
