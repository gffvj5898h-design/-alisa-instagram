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

SEE REPO HISTORY FOR FULL PRIOR LOG ENTRIES — temporary note: full restore pending if this push is size-limited. Prior entries from 2026-09-06 05:33 and earlier remain in git history at commit 84eaf333 and earlier.
