# Identity video recovery audit — evidence only

**Date:** 2026-09-06  
**Task:** `identity-video-recovery-audit`  
**Actor:** Grok  
**Scope:** Audit already-committed Reels 001–004 MP4 candidate masters as possible **video recovery evidence** for Alice identity continuity. Local temporary frame extraction for inspection only.  
**Hard restrictions observed:**  
- `character/references/alice-master-face.jpg` was **not** modified, repaired, re-encoded or replaced.  
- No MP4 or extracted frame was declared canonical.  
- No extracted frames were committed.  
- No new face or Alice image was generated.  
- No text-only generation.  
- No regeneration of Reels 001–005.  
- No repeat of the known 720p+ I2V blocker.  
- Evidence statements distinguish documented provenance from visual interpretation.

Reference still used for visual comparison (evidence only, not canonical):  
`content/reels/005-same-restaurant/stills/start-frame.jpg`  
(1008×1792, SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`, Grok start-frame QA pass, documented master-face identity reference).

---

## Reels 001 — first-date

| Field | Value |
|-------|-------|
| Committed MP4 path | `content/reels/001-first-date/output/approved/reels-001-approved.mp4` |
| Git blob SHA | `ea9ec4e286e6f3b5e1beec2d9191ef72433e5468` |
| Bytes | 9264597 |
| SHA-256 (verified) | `5259ee5c812bfbf43658531392fcc8b47704531a4b804fede86a11422ad0f736` |
| Duration | 15.041667 s |
| Resolution | 512×910 |
| FPS | 30 |
| Video codec | H.264 (High), yuv420p |
| Audio codec | AAC LC, 48 kHz stereo |
| Decode status | **OK** (ffprobe + ffmpeg full decode) |
| Documented identity provenance | Episode package + historical QA: generated with identity reference to `character/references/alice-master-face.jpg` (see `result-notes.md`, `prompt-grok.md`). Status: candidate / QA hold: low-res (below production gate 720×1280). |
| Representative frames inspected (local only) | n=0, ~150, ~300, ~450 (start / mid / late / near-end) |
| Visual observations (interpretation) | Consistent blonde woman ~40; facial structure, eye colour/shape, lip shape, hair colour/style and overall proportions align with the accepted Reels 005 start-frame and documented Alice identity. Lighting and wardrobe vary by scene (black satin dress, bedroom evening). No obvious identity break across sampled frames. |
| Suitability | `supporting_recovery_evidence` |
| Notes | Low native resolution limits pixel-level recovery value. Useful as motion/continuity evidence and as secondary visual confirmation of the same identity line used for 005 start-frame. Not suitable as a high-resolution still source. |

---

## Reels 002 — bad-date-home

| Field | Value |
|-------|-------|
| Committed MP4 path | `content/reels/002-bad-date-home/output/approved/reels-002-approved.mp4` |
| Git blob SHA | `335e4a830bd89211eb60ced5cad8e729d8bb6984` |
| Bytes | 9361410 |
| SHA-256 (verified) | `94cb5b9aa4524d729092f766588717c9a7d85791c55e04d69f1f7cf703e12b5d` |
| Duration | 15.041667 s |
| Resolution | 512×910 |
| FPS | 30 |
| Video codec | H.264 (High), yuv420p |
| Audio codec | AAC LC, 48 kHz stereo |
| Decode status | **OK** |
| Documented identity provenance | Episode package + historical QA: identity source documented as `alice-master-face.jpg` (see `result-notes.md`). Status: candidate / QA hold: low-res. |
| Representative frames inspected (local only) | n=0, ~150, ~300, ~450 |
| Visual observations (interpretation) | Same identity continuum as 001 and 005 start-frame: blonde, ~40, matching facial landmarks. Emotional range (tears, distress) does not break face consistency. Wardrobe: black long-sleeve dress. |
| Suitability | `supporting_recovery_evidence` |
| Notes | Same resolution constraint as 001. Supports continuity evidence across the early story arc. |

---

## Reels 003 — morning-after

| Field | Value |
|-------|-------|
| Committed MP4 path | `content/reels/003-morning-after/output/approved/reels-003-approved.mp4` |
| Git blob SHA | `41c1bd2bd8c5cb9324f3818e2d35d3a556322512` |
| Bytes | 9261519 |
| SHA-256 (verified) | `a09f09486c78b2f1fd73591fffeae67a8328099bdbbd3e6789455907b41e60a3` |
| Duration | 15.033333 s |
| Resolution | 512×910 |
| FPS | 30 |
| Video codec | H.264 (High), yuv420p |
| Audio codec | AAC LC, 48 kHz stereo |
| Decode status | **OK** |
| Documented identity provenance | Episode package restored + historical QA: generated under identity lock to master face (see `result-notes.md`, `prompt-grok.md`). Status: candidate / QA hold: low-res. |
| Representative frames inspected (local only) | n=0, ~150, ~300, ~450 |
| Visual observations (interpretation) | Same woman as 001/002/005 start-frame. Morning light, white shirt, kitchen/Petersburg window. Face remains recognisably continuous; no identity drift observed in sampled frames. |
| Suitability | `supporting_recovery_evidence` |
| Notes | Continues the visual identity line into the morning arc that leads to 004 and later 005. |

---

## Reels 004 — who-knows

| Field | Value |
|-------|-------|
| Committed MP4 path | `content/reels/004-who-knows/output/approved/reels-004-approved.mp4` |
| Git blob SHA | `b3d5c50d2d4e3e65a124cc34b77f85b232de5ef2` |
| Bytes | 9094878 |
| SHA-256 (verified) | `d2b7454244fd6e1ed5bc0593fe10787354985942d65669af3bdbe0c4a6b7fb55` |
| Duration | 15.041667 s |
| Resolution | 512×910 |
| FPS | 30 |
| Video codec | H.264 (High), yuv420p |
| Audio codec | AAC LC, 48 kHz stereo |
| Decode status | **OK** |
| Documented identity provenance | Episode package restored + historical QA: identity lock to master face documented (see `result-notes.md`). Status: candidate / QA hold: low-res. |
| Representative frames inspected (local only) | n=0, ~150, ~300, ~450 |
| Visual observations (interpretation) | Same continuous identity as preceding reels and 005 start-frame. White shirt, phone interaction, overcast Petersburg light. Facial features remain stable across sampled frames. |
| Suitability | `supporting_recovery_evidence` |
| Notes | Closes the pre-005 arc with consistent identity evidence. |

---

## Summary classification

| Reels | Decode | Resolution | Documented provenance | Suitability |
|-------|--------|------------|-----------------------|-------------|
| 001 | OK | 512×910 | master-face identity reference | `supporting_recovery_evidence` |
| 002 | OK | 512×910 | master-face identity reference | `supporting_recovery_evidence` |
| 003 | OK | 512×910 | master-face identity reference | `supporting_recovery_evidence` |
| 004 | OK | 512×910 | master-face identity reference | `supporting_recovery_evidence` |

**Overall conclusion (evidence only):**  
All four committed candidate masters decode cleanly. SHA-256 values match the values previously recorded in each episode `result-notes.md`. Documented provenance for each points to the same canonical identity reference (`character/references/alice-master-face.jpg`). Visual inspection of representative frames shows a consistent ~40-year-old blonde woman whose facial structure, hair and overall appearance align with the accepted (and only currently decodable) still `content/reels/005-same-restaurant/stills/start-frame.jpg`.  

Because native resolution is 512×910 (below production gate), none of the MP4s rise to `strong_recovery_evidence` for high-resolution still recovery. They remain valuable as **supporting_recovery_evidence** for identity continuity, motion behaviour and story-arc consistency.  

No frames were committed. Canonical master was not touched. No file was promoted to canonical status.

---

## Files changed by this audit

- `production/identity-video-recovery.md` (this file, new)
- `production/backlog.md` (mark audit item complete)
- coordination message + state + log (handoff)
