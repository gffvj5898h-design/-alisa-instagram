# Profile avatar — result notes

## Candidate

`content/profile/avatar-candidate.jpg`

Источник: exact Git-blob copy of `character/references/alice-master-face.jpg`.
Не Imagine-crop.

## Технические параметры (Grok, 2026-08-22)

- Git blob SHA: `e1974689dfe7a9a47bf70a0f94abd052b2f0588d`
- bytes: 15008
- resolution: 320×400
- SHA-256: `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`
- cmp vs master-face: IDENTICAL

## QA

- identity: pass
- age ~40: pass
- canon unchanged: pass
- Instagram identity-safe fallback: pass
- dense 1:1 / 1080 production avatar: hold

Статус: candidate / identity-safe fallback. Не production-approved square avatar.

## 2026-09-06 Grok diagnostic — binary integrity

Both `character/references/alice-master-face.jpg` and `content/profile/avatar-candidate.jpg` are byte-identical (15008 bytes, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`).

Integrity check:
- SOI present (`FF D8`)
- EOI **absent** (file does not end with `FF D9`)
- Pillow / libjpeg: `OSError: broken data stream when reading image file`

Consequence: any deterministic center/face-aware square crop (or other pixel-level processing) fails because the JPEG cannot be decoded. Optional backlog item «квадратный crop аватара без смены лица» therefore remains blocked by source-byte integrity, not by missing bridge.

Rule respected: `character/references/alice-master-face.jpg` was **not** modified. No new binary was generated or mailed.
