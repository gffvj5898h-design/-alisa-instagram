# Project Instructions for AI Tools / SuperGrok

## Read first

Before any new task for Alice, read:

1. `GROK_CONTEXT_AND_LOG.md`
2. `coordination/PROTOCOL.md`
3. `coordination/state.json`
4. `character/alice-profile.md`
5. `character/visual-rules.md`
6. `prompts/identity-lock.md`
7. the files for the specific Reels / post being worked on

`GROK_CONTEXT_AND_LOG.md` contains the current creative direction, story continuity and append-only operations log. Keep it updated after meaningful project operations. New log entries are added at the top of the operations log.

## ChatGPT ↔ Grok mailbox

Coordination between ChatGPT and Grok goes through GitHub, not through manual copy/paste of long prompts.

Protocol:

`coordination/PROTOCOL.md`

Current handoff state:

`coordination/state.json`

Mandatory behavior:

1. Read `coordination/state.json` before acting and re-check it as often as the environment allows.
2. Act only when `next_actor` matches your agent (`chatgpt` or `grok`).
3. `user` is not an actor in the coordination protocol. Do not route work to `waiting_for_user` and do not ask the user to manually relay agent-to-agent messages.
4. Read the exact message file referenced by `message_path`.
5. Reply by creating a NEW immutable message file under `coordination/messages/`.
6. Update `coordination/state.json` to point the next actor to that new message.
7. Do not edit or delete old coordination message files.
8. If GitHub and conversational memory disagree, GitHub wins.
9. Binary transfer still follows `production/GROK_BINARY_UPLOAD.md`.
10. If one agent is blocked, pass the blocker to the other agent. If both confirm no autonomous path exists, mark the task blocked and continue the next available backlog item rather than waiting for the user.
11. Do not create endless blocker ping-pong without a new fact, file, URL, tool or changed condition.

## Canonical character

Alice is a persistent fictional AI character. Her only canonical face is stored at:

`character/references/alice-master-face.jpg`

Do not change the canonical face unless the user explicitly instructs you to do so.

## Mandatory rule for any Alice video

1. Load `character/references/alice-master-face.jpg` as a visual / identity reference.
2. Prepend `prompts/identity-lock.md` to the generation prompt.
3. Do not use text-only generation for Alice.
4. If the generator cannot accept the reference image, stop generation rather than substitute a new face.
5. Keep Alice approximately 40 years old and recognizably identical to the master reference.

## Language

All working prompts for Grok / SuperGrok should be written in Russian. If Alice speaks in a video, her speech must be in Russian unless the user explicitly requests another language.

## Content principle

The account is a serialized lifestyle story with a strong visual-flirt direction, not a gallery of unrelated attractive portraits.

Every output should preserve continuity in character, biography, age, personality, visual identity and the current story arc.

## Binary upload bridge for Grok

If Grok's GitHub tool can write only UTF-8 text, do not claim that a JPG / PNG / MP4 has been uploaded directly.

Use the repository bridge described in:

`production/GROK_BINARY_UPLOAD.md`

Protocol:

1. Grok obtains a direct downloadable public HTTPS URL for the generated binary asset.
2. Grok creates one JSON manifest under `production/import-queue/` with `source_url` and exact `target_path`.
3. `.github/workflows/import-generated-assets.yml` downloads and validates the asset.
4. The workflow commits the binary under `content/...` and creates a SHA-256 receipt under `production/import-receipts/`.
5. Grok must verify both the target file and the receipt before writing that the upload succeeded.
6. Never put API keys, cookies, bearer tokens or private URLs into a queue manifest because the repository is public.
7. If Grok has only a chat-local attachment ID or a private/non-downloadable URL, do not regenerate the asset for upload. Return `blocked_binary` to ChatGPT through the mailbox. ChatGPT attempts its own bridge path; if neither agent can access the bytes autonomously, record the blocker and continue another backlog task without asking the user to relay the file.

The importer cannot write into `character/references/`, so this bridge cannot silently replace the canonical Alice face.

## Production approval gate

Do not call a Reels `approved` or `production-approved` until all conditions are met:

1. The episode folder contains `concept.md`, `prompt-grok.md`, `storyboard.md`, and `result-notes.md`.
2. Final video is strict 9:16 and at least 720×1280; 1080×1920 is preferred.
3. Identity is checked against `character/references/alice-master-face.jpg`.
4. Duration, story beats, hands, skin, lipsync and continuity are checked.
5. Grok has re-checked the repository files and confirmed the production master.

Existing 512×910 files are candidate / QA reference masters only, even when stored under legacy `output/approved/` paths.
