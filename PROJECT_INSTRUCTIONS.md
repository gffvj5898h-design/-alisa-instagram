# Project Instructions for AI Tools / SuperGrok

## Source of truth

GitHub branch `main` is the production source of truth. If chat memory disagrees with `main`, `main` wins.

Before any Alice task read:

1. `coordination/PROTOCOL.md`
2. `coordination/state.json`
3. `coordination/tasks.json`
4. `coordination/capabilities.json`
5. the exact file in `state.message_path` when non-null
6. `character/alice-profile.md`
7. `character/visual-rules.md`
8. `prompts/identity-lock.md`
9. task-specific files

`GROK_CONTEXT_AND_LOG.md` and `production/backlog.md` are human summaries, not transaction state.

## Coordination v4

When `main/coordination/state.json` has `schema_version=4`:

- ChatGPT and Grok are stateless workers.
- Act only when `next_actor` equals your actor.
- Re-read canonical state immediately before any proposal submission.
- Do not directly edit `main/coordination/state.json`, `coordination/tasks.json`, `coordination/messages/**`, `coordination/proposals/**`, project instructions, protocol/broker files, canonical identity, workflow files or executable production code.
- Submit exactly one new schema-v4 proposal JSON on branch `coordination-inbox` under `coordination/inbox/`.
- A mailbox commit must add exactly that one proposal file and nothing else.
- Bind the proposal to exact `expected_state_sha` and `turn_id=current+1`.
- GitHub Actions broker is the only canonical coordination writer.
- The user is not a transport actor.
- No self-handoff and no repeated blocker fingerprint without a changed condition.

If `schema_version` is not 4, follow the protocol actually present on `main`; do not infer or activate v4 from a side branch.

## Canonical Alice identity

Canonical path remains:

`character/references/alice-master-face.jpg`

Identity metadata:

`character/identity.json`

Normal autonomous agent proposals can never modify either the canonical image or identity metadata. Repair of corrupt canonical bytes is a separate guarded maintenance operation and must preserve the independently verified identity/checksum policy.

## Mandatory rule for Alice imagery/video

1. Use the active canonical identity reference.
2. Prepend `prompts/identity-lock.md` for Alice video prompts.
3. Never substitute text-only generation for Alice when identity reference is required.
4. If the generator cannot accept the required identity reference, do not generate a replacement face.
5. Preserve age ~40 and continuity.

## Binary data plane

Binary transport is independent of coordination.

Preferred order:

1. verified native connector/Git Data binary path when exact bytes can be supplied safely;
2. `production/import-queue/` via base64 chunks for manageable files;
3. unsigned public direct HTTPS URL;
4. Gmail only as product-to-product byte transport, never as coordination state.

A queue manifest is immutable and independent. One failed manifest must not poison other imports. Do not claim upload success until the target and receipt exist on `main` with matching SHA-256.

Never commit signed/private URLs, cookies, bearer tokens or API keys.

## Production gate

Reels are production-approved only after required package files exist, strict 9:16, at least 720×1280, identity QA, duration/continuity checks and repository confirmation. Legacy 512×910 files remain candidate/QA references.

## Language

Working prompts for Grok are Russian unless the user requests otherwise. Alice speaks Russian unless explicitly changed.
