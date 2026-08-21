# Result notes — Reels 001

## 2026-08-21 — ответ на Grok-аудит

Аудит принят без спора по SHA.

- текущий candidate-master в repo: `output/approved/reels-001-approved.mp4`;
- длительность: 15.041667 с;
- разрешение: 512×910, 30 fps;
- SHA-256: `5259ee5c812bfbf43658531392fcc8b47704531a4b804fede86a11422ad0f736`;
- прежняя запись ниже «No MP4 was produced» относится только к ранней SVD-попытке и не описывает текущий master;
- разрешение ниже production gate 720×1280, поэтому ролик **не production-approved**;
- текущий статус: candidate / QA hold: low-res.

Следующий шаг: пересобрать / перегенерировать нативный 9:16 минимум 720×1280 с `character/references/alice-master-face.jpg`, затем повторный Grok QA.

---

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

No MP4 was produced in that SVD attempt. Face was not regenerated from text.

### SVD limits vs Reels 001

- Native output: ~25 frames at 6 fps ≈ 4 seconds, landscape 1024×576
- Need: 8 seconds, strict 9:16
- SVD cannot play all four story beats in one shot
- High `motion_bucket_id` warps faces; keep 30–60

### If run on a GPU later

Historical note only. Current canonical identity source remains `character/references/alice-master-face.jpg`.

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

Decision: SVD was a motion test only, not the current Reels master.

## 2026-08-21 — V2 video attempt in this chat

Historical attempt. Video reference slot was unavailable. Text-to-video refused.

## 2026-08-21 — V1 generated video QA

V1 MP4: 6.04s, 400×736, identity 8/10, story incomplete, too glamorous. Not final.
