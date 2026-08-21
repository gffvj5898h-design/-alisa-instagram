# Project Instructions for AI Tools / SuperGrok

## Read first

Before any new task for Alice, read:

1. `GROK_CONTEXT_AND_LOG.md`
2. `character/alice-profile.md`
3. `character/visual-rules.md`
4. `prompts/identity-lock.md`
5. the files for the specific Reels / post being worked on

`GROK_CONTEXT_AND_LOG.md` contains the current creative direction, story continuity and append-only operations log. Keep it updated after meaningful project operations. New log entries are added at the top of the operations log.

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

## Production approval gate

Do not call a Reels `approved` or `production-approved` until all conditions are met:

1. The episode folder contains `concept.md`, `prompt-grok.md`, `storyboard.md`, and `result-notes.md`.
2. Final video is strict 9:16 and at least 720×1280; 1080×1920 is preferred.
3. Identity is checked against `character/references/alice-master-face.jpg`.
4. Duration, story beats, hands, skin, lipsync and continuity are checked.
5. Grok has re-checked the repository files and confirmed the production master.

Existing 512×910 files are candidate / QA reference masters only, even when stored under legacy `output/approved/` paths.
