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

Алиса:
- 40 лет;
- блондинка;
- живёт в Санкт-Петербурге;
- интерьерный дизайнер;
- разведена;
- после долгого перерыва вернулась к знакомствам.

Контент — последовательный сериал с узнаваемой героиней и сильным визуальным флиртом.

Текущий креативный вектор:
- визуальный флирт, уверенность и взрослая привлекательность;
- каждый сюжетный Reels должен двигать историю;
- не скатываться в дешёвую эротическую эстетику;
- лицо и continuity важнее эффектности отдельного кадра;
- не делать серию из однотипных talking-head роликов.

---

## 2. Единственное каноническое лицо

Канонический файл:

`character/references/alice-master-face.jpg`

Обязательные правила:
- всегда использовать его как visual / identity reference;
- никогда не генерировать Алису только по тексту;
- не создавать «похожую блондинку»;
- не менять форму лица, глаза, нос, губы, подбородок и пропорции;
- не омолаживать;
- не превращать кожу в пластиковую beauty-ретушь;
- при I2V можно использовать утверждённый стартовый кадр, но master-face остаётся identity reference;
- если модель не принимает референс, генерацию не запускать;
- не вводить `alice-master-face-v2.jpg` без прямой команды пользователя.

---

## 3. Язык проекта

Рабочие промпты для Grok — на русском. Речь Алисы только на русском.

---

## 4. Технический стандарт Reels

9:16, минимум 720×1280, цель 15 с. Reels 001–044 — candidate / QA hold из-за 512×910.

---

## 5. Текущая сюжетная линия

001–04: candidate / QA hold, 512×910.

005: start-frame v2 QA pass. I2V attempt 1 rejected (400×736). Grok и ChatGPT подтвердили отсутствие автономного 720p+ I2V-пути при текущих ограничениях инструментов/аккаунтов; статус `blocked_tooling_external`. Текущий активный backlog — avatar candidate из master face, `next_actor=grok`.

Бинарный транспорт: сначала `production/GROK_BINARY_UPLOAD.md`, запасной мост — `production/GMAIL_BRIDGE.md`.

---

## 6. Креативные правила

Взрослая, привлекательная, уверенная. Без дешёвой эротики, talking-head и второго лица в зеркале.

---

## 7. Работа с GitHub

`gffvj5898h-design/-alisa-instagram` — источник истины. Журнал append-only. Межагентный транспорт: `coordination/`.
Бинарники: `production/GROK_BINARY_UPLOAD.md` или Gmail-bridge `production/GMAIL_BRIDGE.md`.

---

## 8. Формат записи в журнал

### YYYY-MM-DD HH:MM — название
- Кто/инструмент
- Что сделано
- Какие файлы изменены
- Результат
- Статус
- Следующий шаг

---

# Журнал операций

### 2026-08-22 01:22 +03:00 — Включён Gmail-bridge для бинарников
- Кто/инструмент: Grok + Gmail
- Что сделано: по команде пользователя настроен запасной транспорт картинок. Письма идут с roman12101992@gmail.com на тот же адрес. В теме — SAVE_TO, KIND, SHA256. Отправлено первое письмо с вложением imagine-avatar 800x800.
- Какие файлы изменены: `production/GMAIL_BRIDGE.md`, `coordination/messages/20260822-0122-grok-to-chatgpt-gmail-bridge.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: мост живой. Вложение `alice-avatar-candidate-800.jpg`, SHA-256 `037d0e622d2cc2a4ddfb24c20583a6f14fb6f04a3c256ce94fb578a46d7b1267`, цель `content/profile/avatar-candidate-imagine-800.jpg`. Канон лица не менялся.
- Статус: completed
- Следующий шаг: ChatGPT забирает письмо по промпту Gmail-bridge и либо заливает файл в SAVE_TO, либо продолжает текущий avatar QA по `content/profile/avatar-candidate.jpg`.

### 2026-08-22 00:55 +03:00 — ChatGPT проверил альтернативные I2V и перевёл backlog
- Кто/инструмент: ChatGPT + Runway + OpenArt + Magnific + GitHub
- Что сделано: после handoff Grok проверены альтернативные I2V-пути без изменения `alice-master-face.jpg` и принятого start-frame Reels 005. Runway аутентифицирован, но `availableVideoModels=[]`. OpenArt Seedance 2.5 и Grok Imagine 1.5 отклонены при submit с `insufficient_balance`. Magnific вернул HTTP 403.
- Какие файлы изменены: `coordination/messages/20260822-0055-chatgpt-to-grok-reels005-blocked-next-backlog.md`, `coordination/state.json`, `content/reels/005-same-restaurant/result-notes.md`, `production/backlog.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: Reels 005 зафиксирован как `blocked_tooling_external`. `next_actor=grok`, active task `profile-avatar-from-master-face`.
- Статус: completed / waiting_for_grok
- Следующий шаг: Grok делает avatar candidate из `character/references/alice-master-face.jpg`.

### 2026-08-22 00:47 +03:00 — Grok mailbox: I2V 005 blocked_tooling
- Статус: completed / waiting_for_chatgpt

### 2026-08-22 00:40 +03:00 — Убран пользователь из handoff; два агента работают автономно
- Статус: completed / waiting_for_grok

### 2026-08-22 00:33 +03:00 — Автоматизирован handoff ChatGPT ↔ Grok через GitHub
- Статус: completed / waiting_for_grok

### 2026-08-22 00:24 +03:00 — QA первого I2V-прогона Reels 005
- Статус: rejected / regenerate

### 2026-08-21 23:16 CEST — Grok QA start-frame v2 Reels 005
- Статус: completed

### 2026-08-22 00:11 +03:00 — Start-frame v2 Reels 005 загружен в main
- Статус: pending Grok QA

### 2026-08-21 22:22 +03:00 — Бинарный bridge Grok → GitHub
- Статус: completed
