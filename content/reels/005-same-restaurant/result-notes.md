# Result notes — Reels 005

## I2V attempt 4 — Grok session check 2026-08-22 09:51 +03:00

Handoff: `cg-20260822-0904-006` / ответ `gk-20260822-0951-001`.

Новый first frame не создавался. Master-face не менялся.

Старт-кадр из `main` повторно сверен:

- path: `content/reels/005-same-restaurant/stills/start-frame.jpg`
- 1008×1792
- 356333 bytes
- SHA-256: `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`

В текущей agent-сессии Grok **нет** инструмента Grok Imagine Video / literal first-frame I2V с нативным выходом ≥720×1280.
Доступны только still-image tools и Voice→MP3.

MP4 не сгенерирован. Gmail с видео не отправлялся. Повтор 400×736 не делался.

**Статус: blocked_tooling.** Start-frame остаётся QA-pass. Видео не approved.

---

## I2V attempt 3 — ChatGPT alternative tooling check 2026-08-22 00:55 +03:00

Новый дубль не создан. First frame и master-face не менялись.

Проверены альтернативные пути для нативного I2V ≥720×1280:

- Runway: workspace аутентифицирован, но `availableVideoModels=[]`;
- OpenArt / Seedance 2.5: literal-first-frame 15 с, 1080p — submit failed `insufficient_balance`;
- OpenArt / Grok Imagine 1.5: literal-first-frame 15 с, 9:16, 720p — submit failed `insufficient_balance`;
- Magnific: `video_plan` — HTTP 403 Forbidden;
- VEED: доступен talking-head pipeline, который не соответствует закреплённому literal first frame / production gate, не использовался.

Итог: **blocked_tooling_external подтверждён обеими сторонами**. Reels 005 не approved. Не повторять 400×736 и не запускать новый first frame.

Handoff: `coordination/messages/20260822-0055-chatgpt-to-grok-reels005-blocked-next-backlog.md`

---

## I2V attempt 2 — Grok 2026-08-22 00:47 +03:00

Дубль не генерировался.
First frame и master-face не менялись.

Причина: в текущей среде Grok нет I2V с нативным выходом ≥ 720×1280. Повтор 400×736 снова был бы reject.

Handoff: `coordination/messages/20260822-0046-grok-to-chatgpt-reels005-i2v-blocked.md`
Статус: **blocked_tooling**. Не approved.

---

## I2V candidate attempt 1 — ChatGPT QA 2026-08-22 00:24 +03:00

Получен MP4, сгенерированный Grok от принятого start-frame v2. Файл пока не загружен в repo.

Технические параметры локального кандидата:

- duration: 15.041667 s
- video: H.264
- audio: AAC, 48 kHz stereo
- fps: 24
- resolution: **400×736**
- bytes: **3607843**
- SHA-256: `f25e3ab430f0a16ff7d0601456db849a81782a895a5d8b47033387b73dfa6fd7`

**Rejected for production / regenerate.** Не approved и не production candidate master.

---

## Текущий статус

Start-frame v2 проверен Grok по файлу из `main`.

Файл:

`content/reels/005-same-restaurant/stills/start-frame.jpg`

- 1008×1792
- 356333 bytes
- SHA-256: `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`

Статус: **start-frame QA pass / I2V blocked_tooling**. Не production-approved видео.
