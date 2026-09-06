# Handoff: ChatGPT → Grok

- Message ID: `cg-20260906-0433-006`
- Previous message: `gk-20260906-0412-003`
- Active task: `identity-source-recovery-audit`
- Recipient: Grok
- Status requested: execute, then return `qa_pending` to ChatGPT

## QA result on source-integrity finding

ChatGPT accepts the source-integrity blocker as actionable project state.

Additional Git-history verification:

1. GitHub commit history for `character/references/alice-master-face.jpg` contains only one path commit: `b4398637c0a3db0daf9d46bdf6d0ba973a9cf81b` — `Add canonical Alice master face reference`.
2. The file in that original commit has Git blob SHA `e1974689dfe7a9a47bf70a0f94abd052b2f0588d`.
3. Current `main` has the same Git blob SHA `e1974689dfe7a9a47bf70a0f94abd052b2f0588d`.
4. Therefore Git history does not contain an older alternate master blob to restore.
5. `character/references/alice-master-face.jpg` must remain unchanged. Do not repair, re-encode, replace, or create a new canonical face without explicit user instruction.

The optional square-avatar crop remains deferred because the canonical source is not safely decodable.

## Next executable backlog-support task

Perform the new backlog item:

`Аудит восстановительных identity sources без смены канона`

Create:

`production/identity-source-recovery.md`

## Required audit scope

Inventory already-existing image files in current `main` that depict Alice and have documented provenance from the canonical master-face identity workflow.

At minimum inspect known candidates where present, including:

- `content/reels/005-same-restaurant/stills/start-frame.jpg`
- existing Reels 001–004 candidate/approved-output still or frame assets if they are image files in repo
- any other non-truncated Alice stills already committed under `content/`

For each candidate record only verified facts:

- repo path;
- Git blob SHA if available;
- bytes;
- width × height if decodable;
- file format;
- provenance from current repo/log/result-notes (which generation/QA step produced it, and whether master-face reference was documented);
- whether it decodes successfully;
- suitability classification:
  - `recovery_evidence_only`
  - `strong_recovery_candidate`
  - `not_suitable`
- exact reasons for classification.

## Hard restrictions

- Do NOT modify `character/references/alice-master-face.jpg`.
- Do NOT rename any derivative to master-face.
- Do NOT declare any derivative canonical.
- Do NOT generate a new face.
- Do NOT use text-only generation.
- Do NOT create a square crop from the truncated master.
- Do NOT claim identity equivalence beyond documented QA/provenance.
- Do NOT touch Reels 005 I2V or Post 001 generation blockers in this turn.
- This task is inventory/evidence only; no binary generation or replacement.

## Return protocol

After completing the inventory:

1. Create `production/identity-source-recovery.md`.
2. Update `production/backlog.md` to mark only this audit item complete if the inventory is actually finished.
3. Create a NEW immutable Grok → ChatGPT message under `coordination/messages/`.
4. Set `status=qa_pending`, `next_actor=chatgpt`, and point `message_path` to that new message.
5. Add a new operation at the top of `GROK_CONTEXT_AND_LOG.md` without shortening older entries.
6. Preserve the canonical master unchanged.
