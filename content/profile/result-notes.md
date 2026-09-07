# Profile avatar — result notes

## Current candidate — 2026-09-07

`content/profile/avatar-candidate.jpg`

Источник: non-generative center-square crop из verified recovered original Alice master source. Новое лицо не генерировалось.

### Технические параметры

- bytes: 372608
- resolution: 1080×1080
- mode: RGB
- SHA-256: `cd13823359565526f6f60e6e2c2e5926aded675e0fc89ecacce38bdc62f25c57`
- JPEG full decode: pass
- EOI: present
- binary import receipt: `production/import-receipts/20260907-avatar-firestorage-v3.md`
- import workflow run: `34070153104` — success

### Canonical source after guarded repair

`character/references/alice-master-face.jpg`

- bytes: 606787
- resolution: 1237×1536
- mode: RGB
- SHA-256: `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`
- JPEG full decode: pass
- EOI: present
- guarded repair workflow run: `34069880776` — success
- repair commit produced by GitHub Actions: `848d332`
- metadata: `character/identity.json`

This was a byte-integrity restoration from the verified original user upload, not a character redesign.

## Automated Avatar QA — 2026-09-07

Workflow: `Avatar QA`, run `34070246195` — **success**.

- canonical integrity: **pass**
- overall: **pass**
- avatar dimensions: 1080×1080
- preferred square 1080: true
- circular crop safe: true
- identity kind: `likely_same_identity`
- aHash Hamming: 24
- MAE64: 0.073
- errors: none
- warnings: none

Technical status: **production-usable square avatar**. Final independent Grok visual identity QA remains the cross-agent gate before closing the maintenance task.

---

## Historical state — 2026-08-22 / 2026-09-06

The old `content/profile/avatar-candidate.jpg` was an exact copy of the then-corrupted canonical file:

- 15008 bytes
- 320×400
- SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`
- JPEG SOI present, EOI absent
- Pillow/libjpeg decode failed

That historical fallback is no longer the active candidate. The corrupt bytes remain recoverable through Git history for audit only.
