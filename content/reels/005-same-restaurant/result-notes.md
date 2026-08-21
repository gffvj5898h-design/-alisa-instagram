# Result notes — Reels 005

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

QA:

- длительность около 15 секунд — да;
- identity в целом удерживается, но на крупных планах появляется заметный beauty / face drift относительно master-face;
- Петербург и рабочая студия сохраняются;
- ноутбук / образцы / телефон участвуют в действии;
- телефон на одном из крупных планов развёрнут ярким синим экраном к камере — нежелательный AI-маркер;
- финальный бит визуально не читается уверенно как запись голосового ответа: телефон остаётся у лица;
- **production gate по формату провален**: 400×736 не является строгим 9:16 и существенно ниже минимальных 720×1280.

### QA decision

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

## Grok QA 2026-08-21 23:16 CEST

1. файл в `main` — да
2. SHA-256 — совпал
3. лицо vs `alice-master-face.jpg` — та же Алиса, не новая блондинка
4. возраст ~40 — да
5. кожа — без сильного beauty-дрейфа; чуть чище master, не пластик
6. руки — 5 пальцев, держат образцы, без явной деформации
7. фон — Нева, исторические фасады, шпили Петербурга; без Москвы-Сити
8. I2V — годится как first frame
