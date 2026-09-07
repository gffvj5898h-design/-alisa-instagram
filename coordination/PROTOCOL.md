# ChatGPT ↔ Grok coordination protocol v4

Status: production control-plane design.

## Core rule

GitHub is the durable source of truth, but **product agents are not canonical state writers**.

- ChatGPT and Grok read canonical state from `main` and create exactly one proposal JSON on the dedicated `coordination-inbox` branch.
- Product agents do not write normal work commits to `main`.
- Only the GitHub Actions broker may update `main/coordination/state.json`, `main/coordination/tasks.json`, canonical work products, or create canonical handoff messages.
- The user is not a transport actor.
- No OpenAI API or xAI model API is required.

This removes the schema-v2 multi-writer race and separates control plane from worker execution.

## Control plane

Authoritative machine-readable files:

- `coordination/state.json` — current scheduler snapshot.
- `coordination/tasks.json` — structured task database.
- `coordination/capabilities.json` — verified autonomous agent capabilities.
- `coordination/proposals/*.json` — broker-archived immutable accepted proposals on `main`.
- `coordination/messages/*.md` — immutable broker-generated handoff/audit events.

Transport mailbox:

- branch `coordination-inbox`
- path `coordination/inbox/*.json`

`GROK_CONTEXT_AND_LOG.md` and `production/backlog.md` are human-readable context only. They do not own transaction state.

## Agent turn

1. Read `main/coordination/state.json`.
2. Act only if `next_actor` equals your actor.
3. Read `message_path`, task DB, capabilities, project instructions and task files.
4. Perform the task with available product tools.
5. On branch `coordination-inbox`, create exactly one NEW proposal JSON under `coordination/inbox/`.
6. The mailbox commit must contain only that one new proposal file.
7. Do not commit task/work/control-plane changes directly to `main`.
8. GitHub Actions captures the proposal, checks out latest `main`, validates exact state ownership and stale-state guards, applies allowed work-product changes, updates tasks/state and creates one immutable canonical event.
9. Re-read `main/coordination/state.json` after the broker commit.

Piggyback paths in a mailbox commit are rejected.

## Proposal contract

Required fields:

- `schema_version`: `4`
- `actor`: `chatgpt` or `grok`
- `message_id`: `cg-*` or `gk-*`
- `task_id`: current `active_task`
- `expected_state_sha`: exact Git blob SHA of current `coordination/state.json`
- `turn_id`: current `turn_id + 1`
- `outcome`: `completed`, `qa_pass`, `qa_fail`, or `blocked`
- `summary`
- `handoff_body`
- `operations`: optional safe text work-product create/update operations
- `blocker_fingerprint`: required only for `blocked`, otherwise `null`

The broker chooses the next task and actor. Agents do not schedule themselves.

## Task scheduler

A task is runnable only when dependencies are complete, attempts are below the limit, and at least one actor satisfies every required capability. `preferred_actor` wins when capable.

If a worker reports `completed` and a different `qa_actor` is configured, the broker changes the task to `qa_pending` and assigns that QA actor. `qa_pass` completes it. `qa_fail` returns it to `ready`, increments attempts and re-schedules.

A `blocked` result stores a stable blocker fingerprint and schedules another runnable task. If nothing is runnable, state becomes `idle` with `next_actor=null`. There are no ChatGPT→ChatGPT parking handoffs.

Capability-blocked tasks are reconsidered only when `coordination/capabilities.json` materially changes. External blockers remain blocked until an explicit condition-change event updates the task.

## Concurrency and stale writes

Every proposal is bound to exact current state SHA and next turn number. Broker runs are serialized. Two proposals derived from the same state cannot both become canonical.

## Broker write policy

Agent-requested operations are UTF-8 text only and limited to explicit work-product prefixes. Proposals cannot mutate `coordination/**`, `.github/**`, project instructions, canonical identity files, or executable production code.

## Binary data plane

Binary media is separate from coordination:

1. Use Git Data binary blob/tree/commit when the active product connector has a verified path for the exact bytes.
2. Otherwise use `production/import-queue/` with `base64_chunks` or an unsigned public HTTPS URL.
3. Gmail may transport bytes between products but is never coordination state.

Each manifest is processed independently. A bad manifest produces a rejection receipt and cannot poison later imports.

## Canonical identity

`character/identity.json` records integrity state for the canonical path. A corrupted byte copy may be repaired only from an independently verified original of the same identity under an explicit maintenance path. Normal agent proposals can never modify canonical identity.

## Repository protection

`main` should ultimately be protected by a GitHub ruleset requiring coordination/QA checks and disallowing force pushes/direct agent writes. The connected GitHub App does not expose repository-admin writes, so the ruleset itself cannot be enabled from chat; CI guards provide detection until that setting is enabled.

## Source of truth

Order of authority:

1. valid broker-owned `coordination/state.json`;
2. `coordination/tasks.json`;
3. immutable broker message;
4. task work products;
5. human summaries.
