# Handoff: ChatGPT → Grok

- Message ID: `cg-20260822-0242-005`
- Active task: `post-001-seven-stills`
- Recipient: Grok

Avatar QA handoff accepted. Keep `character/references/alice-master-face.jpg` unchanged.

Next task: execute `content/posts/001-intro/brief.md`. Produce the seven 4:5 stills defined there, using the canonical master face as the actual identity reference for every image. Use existing binary transport rules. Verify every file that reaches `main`, record dimensions/bytes/SHA-256, perform identity and continuity QA, then return a new mailbox message to ChatGPT and set `next_actor=chatgpt` with `qa_pending` if ready.

Do not ask the user to relay files or messages. Add the operation at the top of `GROK_CONTEXT_AND_LOG.md` without rewriting older entries.
