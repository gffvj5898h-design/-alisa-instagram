# Result notes — Reels 001

## 2026-08-21 — Stable Video Diffusion attempt

### Why SVD

Correct class for identity: image-to-video from a locked still, not text-to-video.
First frame = approved Alice still (edit of `alice-master-face.jpg`).

### What was tried

1. Local SVD via diffusers: **impossible here**.
   Sandbox: 2 CPU, ~1 GB RAM, no NVIDIA GPU. SVD-XT needs several GB of VRAM.
2. Remote SVD Space `multimodalart/stable-video-diffusion`:
   - connected
   - resized the closed-neckline V2 still (`VZX5h.jpg`)
   - `/video` failed: ZeroGPU quota exceeded (`180s requested vs 0s left`)
   - no Hugging Face token in this session

No MP4 was produced. Face was not regenerated from text.

### SVD limits vs Reels 001

- Native output: ~25 frames at 6 fps ≈ 4 seconds, landscape 1024×576
- Need: 8 seconds, strict 9:16
- SVD cannot play all four story beats in one shot
- High `motion_bucket_id` warps faces; keep 30–60

### If run on a GPU later

Start frame: closed-neckline V2 still, not a text-only blonde.
Keep master-face as the identity source for any later SuperGrok pass.

```python
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
import torch

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt-1-1",
    torch_dtype=torch.float16, variant="fp16"
)
pipe.enable_model_cpu_offload()

image = load_image("v2-closed-neckline-still.jpg").resize((576, 1024))
frames = pipe(
    image,
    decode_chunk_size=4,
    motion_bucket_id=40,
    noise_aug_strength=0.02,
    num_frames=25,
    generator=torch.manual_seed(42),
).frames[0]
export_to_video(frames, "content/reels/001-first-date/output/001-svd-test.mp4", fps=6)
```

Decision: SVD is a motion test only, not the final 8s Reels.

## 2026-08-21 — V2 video attempt in this chat

Video reference slot still unavailable. Text-to-video refused.
V2 stills from master-face: same Alice, age ~40; neckline often copies the canon V-neck; skin slightly cleaned.

## 2026-08-21 — V1 generated video QA

V1 MP4: 6.04s, 400×736, identity 8/10, story incomplete, too glamorous. Not final.
