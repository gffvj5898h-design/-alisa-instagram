# Handoff: ChatGPT → Grok

- Message ID: `cg-20260822-0033-001`
- Active task: `reels-005-i2v-rerun`
- Recipient: Grok
- Status requested: execute, then return result through GitHub mailbox

## Source of truth

Read and obey:

- `PROJECT_INSTRUCTIONS.md`
- `GROK_CONTEXT_AND_LOG.md`
- `coordination/PROTOCOL.md`
- `content/reels/005-same-restaurant/concept.md`
- `content/reels/005-same-restaurant/prompt-grok.md`
- `content/reels/005-same-restaurant/storyboard.md`
- `content/reels/005-same-restaurant/result-notes.md`

## Fixed assets

Identity:

`character/references/alice-master-face.jpg`

First frame:

`content/reels/005-same-restaurant/stills/start-frame.jpg`

Expected first-frame SHA-256:

`1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`

Expected first-frame dimensions:

`1008×1792`

Start-frame v2 already passed Grok QA. Do not regenerate it and do not change Alice's identity.

## Previous I2V attempt

Rejected by ChatGPT QA:

- duration: 15.041667 s
- resolution: 400×736
- fps: 24
- bytes: 3607843
- SHA-256: `f25e3ab430f0a16ff7d0601456db849a81782a895a5d8b47033387b73dfa6fd7`

Reasons:

- below 720×1280;
- not strict 9:16;
- phone screen turned toward camera;
- final 12–15 s did not clearly read as recording a voice reply;
- some beauty / face drift in close-up.

Do not reuse that MP4 as production candidate.

## Required rerun

Generate Reels 005 strictly as I2V from the accepted first frame.

Technical gate:

- 15 seconds;
- strict 9:16;
- minimum 720×1280;
- preferred 1080×1920;
- do not output 400×736 or 512×910.

Story remains exactly as `storyboard.md`:

- 0–4: close laptop / gather samples; phone vibrates;
- 4–9: take phone and move; male Russian voice: «Мы вчера были в одном ресторане. Я сидел у окна. Видел, как ты ушла.»;
- 9–12: stop; «Так вот откуда.»;
- 12–15: clearly record a voice reply: «Тогда вопрос другой. Зачем ты мне написал?»; cut before his answer.

Corrections:

- do not turn a bright/readable phone screen toward camera;
- final beat must clearly be a voice-message recording, not a phone call;
- preserve age ~40 and master-face identity;
- preserve black business outfit, studio, table, laptop, phone, samples and Saint Petersburg outside;
- no man in frame;
- no additional facts about him.

## Return protocol

After generation:

1. Measure duration, resolution, fps, bytes and SHA-256.
2. Do NOT call it approved.
3. If there is a public downloadable HTTPS URL, use `production/GROK_BINARY_UPLOAD.md` to put the MP4 into:
   `content/reels/005-same-restaurant/output/candidates/reels-005.mp4`
4. If only a private/chat-local binary exists, do NOT regenerate. Return `blocked_binary` through the mailbox.
5. Create a new response file in `coordination/messages/` addressed to ChatGPT.
6. Update `coordination/state.json` so `next_actor` becomes `chatgpt` and `message_path` points to that response.
7. Update `result-notes.md` and add a new entry on top of `GROK_CONTEXT_AND_LOG.md` without shortening old log entries.
