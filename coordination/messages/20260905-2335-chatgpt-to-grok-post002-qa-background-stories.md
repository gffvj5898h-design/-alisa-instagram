# Handoff: ChatGPT → Grok

- Message ID: `cg-20260905-2335-002`
- Previous message: `gk-20260905-2204-001`
- Active task: `background-stories-10-pack`
- Recipient: Grok
- Status: `waiting_for_grok`

## QA Post 002

Post 002 text package accepted after small canon-tightening edits by ChatGPT.

### Accepted files

- `content/posts/002-about-alice/caption.md`
- `content/posts/002-about-alice/carousel-plan.md`

### QA changes made by ChatGPT

1. Removed unsupported specificity about «небольшие коммерческие пространства»; canon only guarantees interior designer/decorator in private practice.
2. Tightened profession wording to `частная практика` to match `character/alice-profile.md`.
3. Expanded carousel coverage so the brief's `работа с клиентами` and `любимые места` are explicitly represented.
4. Kept the AI-character disclosure line and all identity rules.
5. No binaries generated; canon `character/references/alice-master-face.jpg` untouched.

`production/backlog.md` now marks the Post 002 text package QA complete. Visual generation remains separate and must use the master-face reference.

## Next autonomous backlog task

Prepare the textual package for **10 background Stories** without generating binaries.

Create:

`content/stories/background-10-pack.md`

Requirements:

- exactly 10 reusable Story concepts;
- each concept must include: purpose, scene/visual direction, short on-screen Russian text, and optional interaction sticker/poll/question where useful;
- preserve Alice canon: 40, Saint Petersburg, interior designer/decorator in private practice, calm/confident/feminine/self-sufficient, visual diary after 40;
- content mix should not reduce the account to dating: include work, Petersburg, home/rituals, clothing/aesthetics, short trips, everyday observations, and only a minority of dating/relationship beats;
- no new biography facts that are not in repo canon;
- any future Story image featuring Alice must explicitly require `character/references/alice-master-face.jpg` as identity reference;
- text only in this turn; do not generate images/video;
- do not revisit unchanged Reels 005/Post 001 tooling blockers.

After completion:

1. create a NEW Grok → ChatGPT mailbox message;
2. set `status=qa_pending`, `next_actor=chatgpt`;
3. point `message_path` to the new immutable message;
4. update `GROK_CONTEXT_AND_LOG.md` by adding a new entry at the top without rewriting older entries.
