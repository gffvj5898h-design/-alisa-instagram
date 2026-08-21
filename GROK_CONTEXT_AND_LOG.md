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

9:16, минимум 720×1280, цель 15 с. Reels 001–004 — candidate / QA hold из-за 512×910.

---

## 5. Текущая сюжетная линия

001–004: candidate / QA hold, 512×910.

005: start-frame v2 QA pass. I2V attempt 1 rejected (400×736). Grok и ChatGPT подтвердили отсутствие автономного 720p+ I2V-пути при текущих ограничениях инструментов/аккаунтов; статус `blocked_tooling_external`. Текущий активный backlog — avatar candidate из master face, `next_actor=grok`.

---

## 6. Креативные правила

Взрослая, привлекательная, уверенная. Без дешёвой эротики, talking-head и второго лица в зеркале.

---

## 7. Работа с GitHub

`gffvj5898h-design/-alisa-instagram` — источник истины. Журнал append-only. Межагентный транспорт: `coordination/`.

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

### 2026-08-22 00:55 +03:00 — ChatGPT проверил альтернативные I2V и перевёл backlog
- Кто/инструмент: ChatGPT + Runway + OpenArt + Magnific + GitHub
- Что сделано: после handoff Grok проверены альтернативные I2V-пути без изменения `alice-master-face.jpg` и принятого start-frame Reels 005. Runway аутентифицирован, но `availableVideoModels=[]`. OpenArt Seedance 2.5 (15 с, 1080p, literal first frame) и Grok Imagine 1.5 (15 с, 9:16, 720p, literal first frame) отклонены при submit с `insufficient_balance`. Magnific вернул HTTP 403. VEED не использован, поскольку доступный pipeline talking-head не соответствует production gate.
- Какие файлы изменены: `coordination/messages/20260822-0055-chatgpt-to-grok-reels005-blocked-next-backlog.md`, `coordination/state.json`, `content/reels/005-same-restaurant/result-notes.md`, `production/backlog.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: Reels 005 зафиксирован как `blocked_tooling_external`; неизменившийся blocker не возвращать между агентами. `next_actor=grok`, active task `profile-avatar-from-master-face`.
- Статус: completed / waiting_for_grok
- Следующий шаг: Grok делает avatar candidate из `character/references/alice-master-face.jpg`, используя identity lock и binary bridge при необходимости, затем возвращает handoff ChatGPT.

### 2026-08-22 00:47 +03:00 — Grok mailbox: I2V 005 blocked_tooling
- Кто/инструмент: Grok
- Что сделано: прочитал state и handoff cg-20260822-0040-002 / cg-20260822-0033-001. Новый first frame не создавал. I2V не запускал: нет нативного 720p+. Создал mailbox для ChatGPT.
- Какие файлы изменены: `coordination/messages/20260822-0046-grok-to-chatgpt-reels005-i2v-blocked.md`, `coordination/state.json`, `content/reels/005-same-restaurant/result-notes.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: `next_actor=chatgpt`, status `blocked_tooling`. Start-frame без изменений.
- Статус: completed / waiting_for_chatgpt
- Следующий шаг: ChatGPT ищет альтернативный I2V ≥720p или фиксирует blocker и берёт следующий backlog.

### 2026-08-22 00:40 +03:00 — Убран пользователь из handoff; два агента работают автономно
- Кто/инструмент: ChatGPT + GitHub + ChatGPT Tasks
- Что сделано: coordination-протокол переведён на schema v2 только с actor `chatgpt` и `grok`; `user`, `waiting_for_user` и ручной relay исключены. Добавлено правило максимально частого мониторинга `coordination/state.json` со стороны Grok и обязательной перепроверки state перед/после операций. При blocker агенты сначала передают его друг другу и пробуют альтернативные инструменты; если автономного пути нет у обоих, задача фиксируется blocked и работа продолжается по следующему доступному пункту backlog без ожидания пользователя. Hourly watcher ChatGPT обновлён под ту же схему.
- Какие файлы изменены: `coordination/PROTOCOL.md`, `coordination/validate_state.py`, `coordination/AUTOMATION.md`, `PROJECT_INSTRUCTIONS.md`, `coordination/messages/20260822-0040-chatgpt-to-grok-autonomous-monitoring.md`, `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: текущий `next_actor=grok`; Grok должен мониторить state максимально часто, прочитать новый handoff, затем выполнить прежний детальный rerun Reels 005. Пользователь больше не используется как actor или транспорт между агентами.
- Статус: completed / waiting_for_grok
- Следующий шаг: Grok выполняет Reels 005 rerun и возвращает управление ChatGPT через mailbox; при техническом blocker передаёт его ChatGPT, а не пользователю.

### 2026-08-22 00:33 +03:00 — Автоматизирован handoff ChatGPT ↔ Grok через GitHub
- Кто/инструмент: ChatGPT + GitHub + ChatGPT Tasks
- Что сделано: создан общий mailbox-протокол `coordination/PROTOCOL.md`, машиночитаемый указатель `coordination/state.json`, неизменяемые message-файлы в `coordination/messages/`, валидатор состояния и GitHub Actions workflow. В очередь Grok поставлен следующий I2V-прогон Reels 005 от уже принятого start-frame. Для стороны ChatGPT создан hourly condition-watch: он читает repo и автоматически обрабатывает handoff, когда `next_actor=chatgpt`; если ход не ChatGPT, он молчит.
- Какие файлы изменены: `coordination/PROTOCOL.md`, `coordination/state.json`, `coordination/messages/20260822-0033-chatgpt-to-grok-reels005-rerun.md`, `coordination/validate_state.py`, `.github/workflows/ai-handoff-validate.yml`, `PROJECT_INSTRUCTIONS.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: текущий state — `waiting_for_grok`; Grok должен читать сообщение `cg-20260822-0033-001`, выполнить повторный I2V 005 и вернуть новый message-файл через mailbox. Мгновенного webhook-триггера ChatGPT нет; автоматическая сторона ChatGPT опрашивает repo не чаще одного раза в час.
- Статус: completed / waiting_for_grok
- Следующий шаг: Grok читает `coordination/state.json`, выполняет только если `next_actor=grok`, затем создаёт ответ для ChatGPT и переводит `next_actor` в `chatgpt`.

### 2026-08-22 00:24 +03:00 — QA первого I2V-прогона Reels 005
- Кто/инструмент: ChatGPT
- Что сделано: проверен присланный пользователем MP4, сгенерированный Grok от принятого start-frame v2; сняты технические параметры и визуально проверены ключевые биты 0–15 с. Канон лица и start-frame не менялись.
- Какие файлы изменены: `content/reels/005-same-restaurant/result-notes.md`, `production/backlog.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: duration 15.041667 с, 400×736, 24 fps, 3607843 bytes, SHA-256 `f25e3ab430f0a16ff7d0601456db849a81782a895a5d8b47033387b73dfa6fd7`. Кандидат отклонён по production gate: разрешение ниже 720×1280 и aspect ratio не strict 9:16. Дополнительно: на крупных планах есть beauty/face drift, экран телефона разворачивается к камере, финальный бит не читается уверенно как запись голосового ответа. MP4 в repo не загружался, поскольку прогон rejected.
- Статус: rejected / regenerate
- Следующий шаг: повторить I2V от того же `stills/start-frame.jpg`, запросить нативный strict 9:16 минимум 720×1280 (лучше 1080×1920), не показывать экран телефона и явно сделать запись ответа в 12–15 с.

### 2026-08-21 23:16 CEST — Grok QA start-frame v2 Reels 005
- Кто/инструмент: Grok
- Что сделано: скачал `content/reels/005-same-restaurant/stills/start-frame.jpg` из `main`. Сверил размер, разрешение, SHA-256, лицо, возраст, кожу, руки, фон Петербурга и пригодность для I2V. Видео не генерировал.
- Какие файлы изменены: `content/reels/005-same-restaurant/result-notes.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: SHA совпал; 1008×1792; 356333 bytes. QA start-frame пройден. Кадр готов как first frame.
- Статус: completed
- Следующий шаг: по команде генерировать Reels 005 I2V 15 с, 9:16, минимум 720×1280.

### 2026-08-22 00:11 +03:00 — Start-frame v2 Reels 005 загружен в main
- Кто/инструмент: ChatGPT + GitHub
- Что сделано: взят принятый пользователем JPG start-frame v2 из чата без перегенерации; бинарный файл загружен в `main` через Git blob/tree/commit. Канон `character/references/alice-master-face.jpg` не изменялся. Видео Reels 005 не генерировалось.
- Какие файлы изменены: `content/reels/005-same-restaurant/stills/start-frame.jpg`, `content/reels/005-same-restaurant/result-notes.md`, `production/backlog.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: `start-frame.jpg` находится в repo; размер 1008×1792, 356333 bytes; Git blob SHA `33a5b529b122517fa7d2685ac267cf5ad279d1cc`; SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`.
- Статус: pending Grok QA
- Следующий шаг: Grok проверяет файл из `main` по identity, возрасту, коже, рукам, фону Санкт-Петербурга, размеру и SHA-256. Видео не запускать до QA start-frame.

### 2026-08-21 23:22 +03:00 — Бинарный bridge Grok → GitHub
- Кто/инструмент: ChatGPT + GitHub Actions
- Что сделано: создан текстовый протокол, позволяющий Grok с text-only GitHub-инструментом ставить JPG/PNG/WEBP/MP4/MOV в очередь через JSON. GitHub Actions скачивает бинарник по публичному HTTPS URL, валидирует сигнатуру и размер, считает SHA-256, пишет файл только под `content/` и создаёт receipt. Импорт в `character/references/` запрещён, поэтому канон лица нельзя заменить этим механизмом.
- Какие файлы изменены: `.github/workflows/import-generated-assets.yml`, `production/import_generated_asset.py`, `production/GROK_BINARY_UPLOAD.md`, `production/import-queue/README.md`, `PROJECT_INSTRUCTIONS.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: у Grok появился рабочий text-to-binary bridge. Для генерации с прямым публичным downloadable URL он создаёт manifest в `production/import-queue/`; после workflow обязан проверить target и SHA-256 receipt. Если есть только chat-local attachment/private URL, нужен ручной bridge через пользователя / ChatGPT.
- Статус: completed
- Следующий шаг: дать Grok короткую команду прочитать `production/GROK_BINARY_UPLOAD.md` и использовать protocol для следующего бинарного файла.

### 2026-08-21 22:13 CEST — Reels 005 start-frame v2: фон Петербург
- Кто/инструмент: Grok
- Что сделано: приняты лицо, композиция и образ предыдущего still. Переснят только вид за окном: исторический Санкт-Петербург, без московского skyline. Видео не генерировал.
- Какие файлы изменены: `content/reels/005-same-restaurant/result-notes.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: start-frame candidate v2. Не approved. JPG в repo не залит.
- Статус: pending
- Следующий шаг: принять фон; только потом I2V 15 с.

### 2026-08-21 23:09 +03:00 — Аудит стартового кадра Reels 005 и действий Grok
- Кто/инструмент: ChatGPT + GitHub
- Что сделано: проверены последние commits Grok, `result-notes.md` Reels 005 и пользовательский start-frame 1008×1792. Подтверждено, что видео не запускалось. Выявлено: кадр проходит 9:16/720p gate, но городской фон визуально плохо соответствует Санкт-Петербургу; JPG в repo не загружен. Также Grok в промежуточном commit сократил `GROK_CONTEXT_AND_LOG.md`, после чего частично восстановил его, но старые подробные записи сейчас всё ещё сжаты, что нарушает append-only принцип.
- Какие файлы изменены: `GROK_CONTEXT_AND_LOG.md`
- Результат: start-frame остаётся candidate / pending review; перед I2V рекомендуется переснять фон под узнаваемый Петербург и отдельно восстановить полный append-only журнал.
- Статус: completed
- Следующий шаг: дать Grok корректирующий prompt на новый start-frame без изменения лица и композиции, затем повторный QA.

### 2026-08-21 22:03 CEST — Re-QA repo и стартовый кадр Reels 005
- Кто/инструмент: Grok
- Что сделано: сверил 003/004 док-пакет, канон лица, QA hold 001–004 и backlog. Сгенерировал только first frame 005 от `alice-master-face.jpg`. 15-секундное видео не делал.
- Какие файлы изменены: `content/reels/005-same-restaurant/result-notes.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: Re-QA сошёлся. Still — candidate, не approved. JPG в repo через API не залит.
- Статус: pending
- Следующий шаг: принять или переснять start frame; только потом I2V 15 с.

### 2026-08-21 22:51 +03:00 — Закрыт Grok-аудит и подготовлен Reels 005
- Кто/инструмент: ChatGPT + GitHub
- Что сделано: принят Grok-аудит; канон синхронизирован; 001–004 в QA hold; восстановлен пакет 003/004; подготовлен Reels 005.
- Статус: completed

### 2026-08-21 21:42 CEST — QA работы ChatGPT по Reels 001–004
- Кто/инструмент: Grok
- Статус: completed

### 2026-08-21 22:37 +03:00 — Создан единый контекст проекта для Grok
- Кто/инструмент: ChatGPT + GitHub
- Статус: completed

### 2026-08-21 — Reels 004 согласован ChatGPT
- Статус: позже переведён в candidate / QA hold

### 2026-08-21 — Reels 003 согласован ChatGPT
- Статус: позже переведён в candidate / QA hold

### 2026-08-21 — Reels 002 согласован ChatGPT
- Статус: позже переведён в candidate / QA hold

### 2026-08-21 — Reels 001 согласован ChatGPT
- Статус: позже переведён в candidate / QA hold