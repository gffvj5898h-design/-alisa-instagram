# Алиса Instagram — контекст для Grok и журнал операций

Этот файл — краткий рабочий контекст проекта для Grok / SuperGrok и одновременно операционный журнал.

Перед любой новой задачей по Алисе сначала прочитать:

1. `PROJECT_INSTRUCTIONS.md`
2. `GROK_CONTEXT_AND_LOG.md`
3. `character/alice-profile.md`
4. `character/visual-rules.md`
5. `prompts/identity-lock.md`
6. файл конкретного Reels / поста, над которым идёт работа

---

## 1. Что мы делаем

Создаём сериализированный Instagram-проект вокруг постоянного виртуального AI-персонажа Алисы Ветровой.

---

## 2. Единственное каноническое лицо

`character/references/alice-master-face.jpg`

---

## 4. Технический стандарт Reels

9:16, минимум 720×1280, цель 15 с. Reels 001–004 — candidate / QA hold из-за 512×910.

---

## 5. Текущая сюжетная линия

001–004: candidate / QA hold.
005: start-frame QA pass; I2V blocked_tooling (нет native ≥720p в agent-сессии).
Бинарный транспорт: `production/GROK_BINARY_UPLOAD.md`, `production/GMAIL_BRIDGE.md`.

---

# Журнал операций

### 2026-09-06 06:08 +03:00 — Identity-video-recovery audit выполнен (Reels 001–004)
- Кто/инструмент: Grok + GitHub mailbox + local ffprobe/ffmpeg frame inspection
- Что сделано: принят handoff `cg-20260906-0533-007`. Создан `production/identity-video-recovery.md`. Все четыре committed candidate-master MP4 декодируются (H.264, 512×910, ~15 с). SHA-256 совпали с `result-notes.md`. Documented provenance = identity lock к `alice-master-face.jpg`. Локально извлечены representative frames (n≈0/150/300/450) только для осмотра; **кадры не коммитились**. Визуальная непрерывность с accepted start-frame 005 подтверждена. Классификация каждой: `supporting_recovery_evidence`. Канон не изменён.
- Ключевые факты:
  - 001: `5259ee5c…f736`, 9264597 bytes, 15.041667 s
  - 002: `94cb5b9a…2b5d`, 9361410 bytes, 15.041667 s
  - 003: `a09f0948…60a3`, 9261519 bytes, 15.033333 s
  - 004: `d2b74542…fb55`, 9094878 bytes, 15.041667 s
- Какие файлы изменены: `production/identity-video-recovery.md` (new), `production/backlog.md`, `coordination/messages/20260906-0508-grok-to-chatgpt-identity-video-recovery-done.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: audit complete. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA `production/identity-video-recovery.md` и выбор следующего исполнимого backlog-пункта.

### 2026-09-06 05:33 +03:00 — Identity recovery inventory QA pass; video-source audit передан Grok
- Кто/инструмент: ChatGPT + GitHub mailbox
- Что сделано: проведён QA `production/identity-source-recovery.md`. Ключевые параметры единственного декодируемого still `content/reels/005-same-restaurant/stills/start-frame.jpg` независимо сверены с `content/reels/005-same-restaurant/result-notes.md`: 1008×1792, 356333 bytes, SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`, Grok start-frame QA pass. Классификация оставлена evidence/practical-reference only; derivative не объявлен canonical. В backlog добавлен следующий исполнимый recovery-support task: аудит уже committed MP4 Reels 001–004 как video recovery evidence без смены канона и без commit извлечённых кадров. Создан handoff `cg-20260906-0533-007` для Grok.
- Какие файлы изменены: `production/backlog.md`, `coordination/messages/20260906-0533-chatgpt-to-grok-identity-video-recovery-audit.md`, `GROK_CONTEXT_AND_LOG.md`, `coordination/state.json`
- Результат: identity-source-recovery QA pass; `alice-master-face.jpg` не изменён; следующий task — `identity-video-recovery-audit`.
- Статус: waiting_for_grok
- Следующий шаг: Grok создаёт `production/identity-video-recovery.md`, локально инспектирует representative frames Reels 001–004 только как evidence, не коммитит извлечённые кадры и возвращает `qa_pending` ChatGPT.

### 2026-09-06 05:06 +03:00 — Identity-source-recovery audit выполнен (inventory only)
- Кто/инструмент: Grok + GitHub mailbox + local decode checks
- Что сделано: принят handoff `cg-20260906-0433-006`. Выполнен inventory уже существующих image-файлов Алисы в `main` с documented canonical provenance. Создан `production/identity-source-recovery.md`. Canonical master **не** изменён. Бинарники не генерировались, Gmail-bridge не использовался, square crop не делался.
- Ключевые факты:
  - `character/references/alice-master-face.jpg` и `content/profile/avatar-candidate.jpg` — byte-identical truncated JPEG (15008 bytes, blob `e1974689…`, SHA-256 `2d5347eb…`); EOI отсутствует; Pillow decode fails → `not_suitable`.
  - Единственный декодируемый still: `content/reels/005-same-restaurant/stills/start-frame.jpg` (1008×1792, 356333 bytes, SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`, blob `33a5b529…`); EOI present; full decode OK; documented master-face identity reference + start-frame QA pass → `strong_recovery_candidate`.
  - Других JPG/PNG Alice stills под `content/` нет (001 stills = только README; 002–004 = только MP4).
- Какие файлы изменены: `production/identity-source-recovery.md` (new), `production/backlog.md`, `coordination/messages/20260906-0506-grok-to-chatgpt-identity-source-recovery-done.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: audit complete. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA inventory и выбор следующего исполнимого backlog-пункта.
