# Result notes — Reels 001

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

### Method

Image edit of `alice-master-face.jpg`. No text-only face. No video yet.

### What worked

- Recognizable as the same woman across four beats
- Age holds around 40
- Blonde identity and black dress continue from the canon still
- Story beats are usable: hair / bag / look / door

### What broke

- Beauty retouch is stronger than the master: smoother skin, heavier makeup, more glamour
- Neckline is more revealing than the launch tone needs
- Frame 1 is a bit too posed for «slightly nervous»
- Frame 2 mirror reflection is a 3/4 profile, not a true identity check
- Hands are acceptable, not perfect
- This session still cannot write binary JPEGs into GitHub; stills live in chat until uploaded to `stills/`

### Face consistency

Same person as master-face: yes, at still level.
Same skin/finish as master-face: no, too polished.
Motion: not tested.

### Next prompt changes

- Lower beauty: natural skin, visible texture, less makeup
- Less cleavage / more closed neckline while keeping the black dress
- More everyday apartment, less hotel-glamour furniture
- Smaller hair gesture, less model hand
- Then I2V from `03-look-to-camera.jpg` + master-face as identity reference

## 2026-08-21 — generation blocked in chat

Video reference slot was not available. Text-to-video was refused.
