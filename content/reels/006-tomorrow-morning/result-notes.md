# Reels 006 — result notes

## Start-frame probe 2026-09-07

- Identity reference used by Grok: `character/references/alice-master-face.jpg` (SHA-256 `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`) attached as edit base.
- Candidate JPEG: 1080×1920, 496473 bytes, SHA-256 `bdad3a65fd0ab93e289e0fdd537f323e2b49012fd777f7bacda45afcf2784f3d`.
- Scene: late evening apartment window, dark work-to-home outfit, phone in hand, warm practical lamp plus cool city light, no text, no male face.
- Transport source: Gmail ALISA-BRIDGE message_id `1a07d26141fe0e1b`.
- ChatGPT independently read the attachment, verified exact SHA-256, byte count and full JPEG decode at 1080×1920.
- Binary data-plane import completed on `main`: `content/reels/006-tomorrow-morning/stills/start-frame.jpg`.
- Import receipt: `production/import-receipts/20260907-reels006-start-frame-grok-t5.md`; receipt confirms 496473 bytes, matching SHA-256 and 1080×1920 decode.
- Identity QA: compared visually against the independently recovered verified original canonical attachment (`alice-master-face-original.jpeg`, 606787 bytes, canonical SHA-256 above). Facial structure, eyes, nose, lips, jawline, blonde identity and apparent age remain consistent; no replacement-face drift detected.
- Prompt QA: strict 9:16 start-frame composition, Alice by apartment window, phone, dark outfit, mixed warm/cool lighting; no man visible and no text.
- Canonical identity files were not modified.

**Status: start-frame QA PASS.** This approves only the Reels 006 start frame / capability probe evidence, not a Reels 006 production video.
