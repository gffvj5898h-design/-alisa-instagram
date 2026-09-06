# Identity source recovery audit — evidence only

**Date:** 2026-09-06  
**Task:** `identity-source-recovery-audit`  
**Actor:** Grok  
**Scope:** Inventory of already-existing image files in current `main` that depict Alice and have documented provenance from the canonical master-face identity workflow.  
**Hard restrictions observed:**  
- `character/references/alice-master-face.jpg` was **not** modified, renamed, replaced, re-encoded or repaired.  
- No derivative was declared canonical.  
- No new face was generated.  
- No text-only generation.  
- No square crop from the truncated master.  
- No Reels 005 I2V or Post 001 generation work.  
- Classification is evidence-only; identity equivalence is limited to documented QA/provenance.

---

## Canonical reference (for context only — not a recovery candidate)

| Field | Value |
|-------|-------|
| Path | `character/references/alice-master-face.jpg` |
| Git blob SHA | `e1974689dfe7a9a47bf70a0f94abd052b2f0588d` |
| Bytes | 15008 |
| SHA-256 | `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2` |
| Format | JPEG (SOI present, EOI **absent**) |
| Decode | **Fails** (Pillow / libjpeg: `broken data stream when reading image file`) |
| Provenance | Single path commit `b4398637c0a3db0daf9d46bdf6d0ba973a9cf81b` («Add canonical Alice master face reference»). Same blob in current `main`. No older recoverable alternate blob in Git history (ChatGPT history QA 2026-09-06). |
| Classification | Source of record, but **not decodable**. Not suitable for pixel-level recovery operations. |

---

## Inventory of existing image files under `content/`

### 1. `content/profile/avatar-candidate.jpg`

| Field | Value |
|-------|-------|
| Path | `content/profile/avatar-candidate.jpg` |
| Git blob SHA | `e1974689dfe7a9a47bf70a0f94abd052b2f0588d` (identical to master) |
| Bytes | 15008 |
| SHA-256 | `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2` |
| Width × Height | Reported historically as 320×400; full decode fails |
| Format | JPEG (SOI present, EOI **absent**) |
| Decode | **Fails** (same broken data stream as master) |
| Provenance | Exact Git-blob copy of `character/references/alice-master-face.jpg` (documented in `content/profile/result-notes.md`). Created as identity-safe fallback, not an Imagine crop or independent generation. |
| Suitability | `not_suitable` |
| Reasons | Byte-identical to the truncated canonical master; cannot be decoded for any recovery, crop or re-encode operation. |

### 2. `content/reels/005-same-restaurant/stills/start-frame.jpg`

| Field | Value |
|-------|-------|
| Path | `content/reels/005-same-restaurant/stills/start-frame.jpg` |
| Git blob SHA | `33a5b529b122517fa7d2685ac267cf5ad279d1cc` |
| Bytes | 356333 |
| SHA-256 | `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87` |
| Width × Height | 1008 × 1792 |
| Format | JPEG, RGB, EOI present |
| Decode | **Successful** (Pillow full load) |
| Provenance | Documented in `content/reels/005-same-restaurant/result-notes.md` and generation workflow: created with `character/references/alice-master-face.jpg` as mandatory visual/identity reference (see `prompt-grok.md` identity-lock requirement). Grok QA of the file from `main` recorded as start-frame QA pass. Used as accepted first-frame for subsequent (blocked) I2V attempts. |
| Suitability | `strong_recovery_candidate` |
| Reasons | Fully decodable; higher resolution than the truncated master; explicit documented use of the canonical master-face as identity reference during generation; already passed Grok start-frame QA; only non-truncated Alice still currently present under `content/`. Suitable as recovery evidence and as a practical identity-preserving still for future non-canonical work (e.g. temporary reference while master remains truncated). **Not** to be promoted to canonical master without explicit user instruction. |

---

## Other locations inspected

- `content/reels/001-first-date/stills/` — contains only `README.md` (no JPEG/PNG assets). README describes intended storyboard stills that were never committed as image files.
- `content/reels/002-bad-date-home/`, `003-morning-after/`, `004-who-knows/` — no `stills/` directories with image files; only MP4 candidate masters under `output/approved/`.
- `content/posts/`, `content/stories/`, `content/profile/` (except avatar-candidate) — text files only.
- `production/import-receipts/` — empty / no receipts present.
- No additional `.jpg` / `.jpeg` / `.png` / `.webp` image files depicting Alice were found under `content/` in the current `main` tree.

MP4 candidate masters (Reels 001–004) exist and contain Alice, but they are video files, not still images, and fall outside the required image-file inventory scope. Extraction of frames from them was not performed in this audit (would constitute new generation of derivative stills).

---

## Summary classification

| Path | Decode | Suitability |
|------|--------|-------------|
| `character/references/alice-master-face.jpg` | Fail | Source of record (truncated) |
| `content/profile/avatar-candidate.jpg` | Fail | `not_suitable` |
| `content/reels/005-same-restaurant/stills/start-frame.jpg` | OK (1008×1792) | `strong_recovery_candidate` |

**Conclusion (evidence only):**  
The sole currently decodable Alice still with documented canonical-reference provenance is `content/reels/005-same-restaurant/stills/start-frame.jpg`. It is classified `strong_recovery_candidate` for recovery-evidence and practical reference use. No action was taken to alter the canonical master or to promote any derivative.

---

## Files changed by this audit

- `production/identity-source-recovery.md` (this file, new)
- `production/backlog.md` (mark audit item complete)
- coordination message + state + log (handoff)
