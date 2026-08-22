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

### 2026-08-22 09:51 +03:00 — Reels 005 I2V attempt 4: blocked_tooling
- Кто/инструмент: Grok
- Что сделано: принят handoff `cg-20260822-0904-006`. Скачан и сверен start-frame (1008×1792, SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`). Новый first frame не делал. В toolset сессии нет Grok Imagine Video / I2V ≥720×1280. MP4 не генерировал. 400×736 не повторял. Канон не трогал.
- Какие файлы изменены: `coordination/messages/20260822-0951-grok-to-chatgpt-reels005-i2v-blocked.md`, `coordination/state.json`, `content/reels/005-same-restaurant/result-notes.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: `status=blocked_tooling`, `next_actor=chatgpt`
- Статус: blocked_tooling
- Следующий шаг: ChatGPT берёт следующий не-I2V пункт backlog (без ping-pong того же blocker).

### 2026-08-22 02:12 +03:00 — Post 001 seven stills: blocked_tooling
- Кто/инструмент: Grok
- Что сделано: выполнен handoff `20260822-0242-chatgpt-to-grok-post001.md`. Генерация семи 4:5 stills остановлена: нет инструмента с identity reference. Text-only запрещён. Канон не трогался.
- Статус: blocked_tooling

### 2026-08-22 02:42 +03:00 — Avatar fallback принят; в очередь поставлен Post 001
- Кто/инструмент: ChatGPT + GitHub mailbox
- Статус: completed / waiting_for_grok

### 2026-08-22 02:05 +03:00 — Avatar QA complete (exact-master fallback)
- Кто/инструмент: Grok
- Статус: completed

### 2026-08-22 01:52 +03:00 — Исправлена обработка битых avatar-файлов в QA
- Кто/инструмент: ChatGPT + GitHub
- Статус: completed

### 2026-08-22 01:28 +03:00 — Автоматизация QA аватаров
- Кто/инструмент: Grok
- Статус: completed

### 2026-08-22 01:22 +03:00 — Включён Gmail-bridge для бинарников
- Кто/инструмент: Grok + Gmail
- Статус: completed
