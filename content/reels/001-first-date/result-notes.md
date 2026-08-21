# Result notes — Reels 001

## 2026-08-21 — V2 video attempt in this chat

### Source of truth used

- `content/reels/001-first-date/prompt-grok-v2.md`
- `character/references/alice-master-face.jpg` loaded and inspected as identity reference

### Video generation

**Not launched.**

This chat can read the master-face JPEG and can edit stills from it. It still cannot attach that JPEG to SuperGrok / grok-imagine-video-1.5 as a real Character / identity / reference-to-video slot.

Per `PROJECT_INSTRUCTIONS.md` and `prompt-grok-v2.md`: do not use text-to-video. If the generator cannot accept the reference, stop.

So V2 was not generated as an 8-second MP4 here. That is the correct stop, not a failed identity test.

### What was generated instead

Four V2 stills by editing the master-face, to test the V2 corrections before the next video run:

1. small hair adjustment beside a soft mirror
2. lifting a small black handbag
3. look to camera
4. restrained smile and start of exit toward the door

V2 still constraints applied:

- more closed black long-sleeve neckline
- face and action first, no chest-focused crop
- lived-in Petersburg apartment, not hotel glamour
- natural skin texture, lighter makeup
- smaller everyday gestures

### Face comparison vs master-face

To be filled after the stills render in this turn. If a still drifts, reject it as an I2V start frame.

### Next action for the actual V2 video

1. Open grok.com/imagine video.
2. Attach `alice-master-face.jpg` as Character reference, first slot.
3. Paste the block from `prompt-grok-v2.md`.
4. Settings: 9:16, exactly 8 seconds, 720p+.
5. Reject any clip that ends early or skips the bag / door beats.
6. Put the approved MP4 in `content/reels/001-first-date/output/`.

## 2026-08-21 — V1 generated video QA

### Source

User-provided Grok-generated MP4 reviewed frame-by-frame against `character/references/alice-master-face.jpg`.

Measured file parameters:

- duration: 6.04 s
- frame rate: 24 fps
- dimensions: 400×736
- codec: H.264

The requested target was 8 s / strict 9:16, so the generated file is shorter than required and its stored pixel dimensions are not the requested target output.

### Identity / age

- Same recognizable Alice as master-face: **yes, overall**
- Severe mid-clip identity drift: **not observed**
- Apparent age around 40: **mostly preserved**
- Face consistency QA: **8/10**

Face shape, eyes, nose, lips, blonde identity and overall recognizable appearance remain coherent across the sampled frames. The main drift is stylistic rather than identity-level.

### What worked

- Alice remains recognizable throughout the clip
- No obvious replacement by a generic blonde model
- Age does not collapse to a 20s look
- Evening apartment / black-dress direction is coherent
- Final direct look and restrained smile are usable
- No text, subtitles, logos or extra people

### What broke

- Clip ends at ~6 s instead of the required 8 s
- Storyboard compliance is incomplete: handbag pickup, clear mirror beat and physical exit toward the door are not clearly completed
- The result reads more like a glamour mood clip than a micro-story about getting ready for a first date
- Skin is smoother / more beauty-retouched than the master-face
- Makeup and overall polish are heavier than desired
- Neckline and framing create too much visual emphasis on cleavage for the account tone
- Early gestures read as model posing rather than slight nervousness
- Hands are acceptable but still somewhat posed / AI-clean
- Mirror is not used clearly enough as a narrative object

### Drift assessment

- identity drift: low
- age drift: low
- beauty / glamour drift: medium
- story drift: high enough to require another generation

### Decision

Do **not** use V1 as final Reels 001.
Use it as a successful identity test and motion reference only.

### V2 changes

Use `content/reels/001-first-date/prompt-grok-v2.md`.

Mandatory corrections:

1. Exactly 8 seconds; do not stop early.
2. All four beats must visibly complete: hair → handbag → camera look → smile + start of exit.
3. More everyday Saint Petersburg apartment; less hotel / luxury-ad styling.
4. Natural skin texture, less makeup, no beauty smoothing.
5. More closed black-dress neckline and no chest-focused composition.
6. Smaller hair gesture; no hand-to-chest model pose.
7. Mirror reflection secondary / soft to reduce identity duplication artifacts.
8. Final second must show physical movement toward the apartment door.

## 2026-08-21 — storyboard stills from master-face

V1 stills: same woman, too glamorous, too open neckline. Not final.
