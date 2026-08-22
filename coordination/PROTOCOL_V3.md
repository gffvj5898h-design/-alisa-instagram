# ChatGPT ↔ Grok coordination protocol v3

Status: prototype. This file does not replace `coordination/PROTOCOL.md` on `main` until the v3 branch is reviewed and merged.

Operational guide for the no-API product mode: `coordination/PRODUCT_MAILBOX.md`.

## Objective

GitHub remains the durable transport and source of truth. Protocol v3 removes direct multi-writer access to the coordination pointer and does **not** require OpenAI or xAI model APIs.

The intended production mode is `product_mailbox`: the authenticated ChatGPT and Grok products use their GitHub integrations to read the repository and create one proposal JSON. GitHub Actions is the only writer that applies the canonical handoff transition.

**Single-writer rule:** ChatGPT and Grok may propose a turn. Only the GitHub broker applies `coordination/state.json` and creates the canonical immutable handoff message.

## Turn flow

1. Agent checks `coordination/state.json` only when its product environment wakes/runs.
2. Agent acts only if `next_actor` matches it.
3. Agent reads `message_path`, project instructions and relevant work files.
4. Agent creates exactly one NEW proposal JSON under `coordination/proposals/`, conforming to `coordination/agent_response.schema.json`.
5. The proposal commit triggers `.github/workflows/ai-proposal-apply-v3.yml`.
6. Broker validates:
   - actor == current `next_actor`;
   - `expected_parent_state_sha` == current state blob SHA;
   - proposed `turn_id` == current `turn_id + 1`;
   - status/next_actor semantics;
   - operation paths against `coordination/broker_policy.json`;
   - no protected/broker-owned path is changed by the model;
   - repeated blocker fingerprints do not create endless ping-pong.
7. In `dry_run`, the broker validates and shows the plan only.
8. In `product_mailbox`, the broker applies allowed work-product files, creates a NEW immutable handoff message and writes the next state.
9. Broker commits the canonical result and validates the transition against Git history.
10. The next product agent is awakened by its own supported routine/polling mechanism and repeats the cycle.

## Important product limitation

GitHub can transport and validate the handoff, but it cannot directly wake this exact ChatGPT app conversation through a repository webhook.

Therefore product-to-product automation is asynchronous:

- ChatGPT side: periodic condition-watch/polling of GitHub; current platform minimum is hourly.
- Grok side: use a Grok Bot routine or supported event-triggered GitHub routine when available; otherwise use periodic checking.

No user copy/paste relay is required.

## State v3 fields

In addition to v2 fields:

- `turn_id`: monotonic coordination transition number.
- `parent_state_sha`: Git blob SHA of the exact previous `state.json` consumed by the transition.
- `hop_count`: number of consecutive agent handoffs within the current active task.
- `hop_limit`: hard circuit breaker; default 20.
- `target_ref`: branch/ref on which the broker may operate.
- `broker.mode`: `dry_run` or `product_mailbox`.
- `broker.lease_owner` / `lease_expires_at`: reserved for broker mutual exclusion.
- `blocker_fingerprint`: stable identifier for a blocker; repeated unresolved blocker handoff is rejected.

## Actor rules

Actors remain exactly:

- `chatgpt`
- `grok`

`user` is not a transport actor. Human approval remains a production/policy gate where required, but the user is never used as a mailbox relay.

## Status enum

State status remains:

- `waiting_for_grok`
- `waiting_for_chatgpt`
- `in_progress_grok`
- `in_progress_chatgpt`
- `blocked_binary`
- `blocked_tooling`
- `qa_pending`
- `completed`

Agent proposals may not emit `in_progress_*`; those states are broker-owned runtime states if/when leases are enabled.

## Agent write surface

In v3 the product agents MUST NOT directly modify:

- `coordination/state.json`;
- `coordination/messages/`;
- protocol/schema/validator/broker files;
- `PROJECT_INSTRUCTIONS.md`;
- canonical Alice identity reference.

For coordination, an agent directly creates only:

`coordination/proposals/<unique>.json`

The proposal may request work-product changes only to paths allowed by `coordination/broker_policy.json`.

Old proposal files are immutable audit records.

## Concurrency / stale-write rule

Every proposal is bound to one exact state blob SHA. If `coordination/state.json` changes before broker application, the proposal is stale and MUST be rejected. No automatic merge of stale coordination state is allowed.

GitHub Actions uses a per-ref concurrency group so proposal-apply runs are serialized. Two proposals created from the same state cannot both become canonical: after the first transition, the second fails the parent-state check.

## Anti-loop rule

A blocked proposal must provide `blocker_fingerprint`.

If the same active task already carries the same blocker fingerprint and no new fact/file/URL/tool/change-condition is recorded, the broker rejects another blocked handoff. The task must either move to a different available backlog item or remain blocked without ping-pong.

`hop_limit` is an independent hard circuit breaker even when blocker fingerprints differ.

## Modes

### `dry_run`

- validates state and transitions;
- builds the dispatch envelope;
- validates product-agent proposal files;
- does not apply proposal changes;
- requires no API secrets.

### `product_mailbox`

- still calls no model API;
- ChatGPT/Grok product agents create proposal JSON through GitHub;
- GitHub Actions validates and applies the proposal;
- broker owns canonical `state.json` and handoff-message writes;
- no `OPENAI_API_KEY` is required.

## Source of truth

If model memory, chat transcript and GitHub disagree, GitHub wins. Derived model memory never overrides repository state or primary project files.
