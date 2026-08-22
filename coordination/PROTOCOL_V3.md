# ChatGPT ↔ Grok coordination protocol v3

Status: prototype. This file does not replace `coordination/PROTOCOL.md` on `main` until the v3 branch is reviewed and merged.

## Objective

GitHub remains the durable transport and source of truth, but v3 removes direct multi-writer access to the coordination pointer.

**Single-writer rule:** ChatGPT/OpenAI and Grok/xAI may propose a turn. Only the broker applies `coordination/state.json` and creates the canonical immutable handoff message.

## Turn flow

1. Broker reads and validates `coordination/state.json`.
2. Broker refuses work if `hop_count >= hop_limit`, state is stale, or a lease is active for another run.
3. Broker reads `message_path` and builds a dispatch envelope for `next_actor`.
4. Recipient agent returns a JSON proposal conforming to `coordination/agent_response.schema.json`.
5. Broker validates:
   - actor == current `next_actor`;
   - `expected_parent_state_sha` == current state blob SHA;
   - proposed `turn_id` == current `turn_id + 1`;
   - status/next_actor semantics;
   - operation paths against `coordination/broker_policy.json`;
   - no protected/broker-owned path is changed by the model;
   - repeated blocker fingerprints do not create endless ping-pong.
6. Broker applies allowed work-product files.
7. Broker creates a NEW immutable `coordination/messages/*.md` handoff.
8. Broker atomically writes the next state with:
   - incremented `turn_id`;
   - `parent_state_sha` set to the state blob that was actually consumed;
   - incremented/reset `hop_count`;
   - new `message_path`;
   - updated last-message id;
   - blocker fingerprint if applicable.
9. CI validates the transition against Git history.
10. In live mode, a broker event dispatches the next actor. In prototype mode, this last step is dry-run only.

## State v3 fields

In addition to v2 fields:

- `turn_id`: monotonic coordination transition number.
- `parent_state_sha`: Git blob SHA of the exact previous `state.json` consumed by the transition.
- `hop_count`: number of consecutive agent handoffs within the current active task.
- `hop_limit`: hard circuit breaker; default 20.
- `target_ref`: branch/ref on which the broker may operate.
- `broker.mode`: `dry_run` or `live`.
- `broker.lease_owner` / `lease_expires_at`: reserved for live-run mutual exclusion.
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

Agent proposals may not emit `in_progress_*`; those states are broker-owned runtime states when live execution is implemented.

## Concurrency / stale-write rule

Every agent proposal is bound to one exact state blob SHA. If `coordination/state.json` changes before application, the proposal is stale and MUST be discarded/re-run. No automatic merge of stale coordination state is allowed.

## Path policy

Agents can propose changes only to work-product paths allowed by `coordination/broker_policy.json`.

The following are broker/protected surfaces and cannot be changed by an autonomous agent proposal:

- `coordination/state.json`
- canonical handoff creation under `coordination/messages/`
- protocol/schema/validator/broker files
- `PROJECT_INSTRUCTIONS.md`
- canonical Alice identity reference

A change to these requires an explicit repository maintenance operation outside an autonomous turn.

## Anti-loop rule

A blocked proposal must provide `blocker_fingerprint`.

If the same active task already carries the same blocker fingerprint and no new fact/file/URL/tool/change-condition is recorded, the broker rejects another blocked handoff. The task must either move to a different available backlog item or remain blocked without ping-pong.

`hop_limit` is an independent hard circuit breaker even when blocker fingerprints differ.

## Prototype vs live

### Prototype (`dry_run`)

- validates state and transitions;
- builds the dispatch envelope;
- does not call OpenAI/xAI;
- does not autonomously commit an agent response;
- requires no API secrets.

### Live

Live mode must not be enabled until:

1. OpenAI and xAI adapters are implemented/tested;
2. API credentials exist only in GitHub Actions secrets;
3. branch protection and allowed-path policy are reviewed;
4. the broker has write permission only to the intended ref;
5. model output is validated before every write;
6. spend/rate limits and a hop limit are configured.

## Source of truth

If model memory, chat transcript and GitHub disagree, GitHub wins. Derived model memory never overrides repository state or primary project files.
