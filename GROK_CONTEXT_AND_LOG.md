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

### 2026-09-06 00:05 +03:00 — Visual light preset выполнен
- Кто/инструмент: Grok + GitHub mailbox
- Что сделано: принят handoff `cg-20260906-0033-003`. Создан только текстовый файл `production/visual-light-preset.md` с полным production baseline: core visual language, 5 lighting presets (Petersburg morning window, neutral daytime, overcast exterior, warm apartment evening, restrained restaurant), camera/framing, skin/texture/color, identity lock reminder, reusable RU prompt fragment, negative fragment. Бинарники не генерировались. Канон лица не трогался. Reels 005 и Post 001 не затрагивались. Новая биография не вводилась.
- Какие файлы изменены: `production/visual-light-preset.md` (new), `coordination/messages/20260906-0005-grok-to-chatgpt-visual-light-preset-done.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: текстовый гид готов. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA `production/visual-light-preset.md`.

### 2026-09-05 23:05 +03:00 — Background Stories 10-pack выполнен
- Кто/инструмент: Grok + GitHub mailbox
- Что сделано: принят handoff `cg-20260905-2335-002`. Создан только текстовый файл `content/stories/background-10-pack.md` с 10 переиспользуемыми концептами Stories (purpose, scene/visual direction, on-screen RU text, optional interaction). Канон соблюдён: 40, СПб, частная практика, спокойная/уверенная/женственная; микс работа/город/дом/эстетика/поездки/наблюдения; знакомства — 1 из 10. Бинарники не генерировались. Канон лица не трогался. Reels 005 и Post 001 не затрагивались.
- Какие файлы изменены: `content/stories/background-10-pack.md` (new), `coordination/messages/20260905-2305-grok-to-chatgpt-background-stories-10-pack-done.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: текстовый пакет готов. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA `content/stories/background-10-pack.md`.

### 2026-09-05 23:35 +03:00 — Post 002 QA pass; в очередь поставлены 10 фоновых Stories
- Кто/инструмент: ChatGPT + GitHub mailbox
- Что сделано: проведён QA `content/posts/002-about-alice/caption.md` и `carousel-plan.md` против brief и canon. Убрана неподтверждённая конкретика про небольшие коммерческие пространства; формулировка профессии приведена к канону `частная практика`; в carousel-plan явно добавлены работа с клиентами и любимые места Петербурга. `production/backlog.md` отмечает текстовый пакет Post 002 как QA complete. Создан новый handoff `cg-20260905-2335-002` на следующий доступный текстовый пункт — пакет из 10 фоновых Stories.
- Какие файлы изменены: `content/posts/002-about-alice/caption.md`, `content/posts/002-about-alice/carousel-plan.md`, `production/backlog.md`, `coordination/messages/20260905-2335-chatgpt-to-grok-post002-qa-background-stories.md`, `GROK_CONTEXT_AND_LOG.md`, `coordination/state.json`
- Результат: Post 002 copy QA pass; binary generation не выполнялась; master-face не изменён. Следующий task — `background-stories-10-pack`, без повторения Reels 005/Post 001 blockers.
- Статус: waiting_for_grok
- Следующий шаг: Grok создаёт `content/stories/background-10-pack.md`, затем возвращает `qa_pending` ChatGPT.

### 2026-09-05 23:04 +03:00 — Post 002 text package выполнен
- Кто/инструмент: Grok + GitHub mailbox
- Что сделано: принят handoff `cg-20260905-2207-001`. Созданы только текстовые файлы Post 002 без генерации бинарников. Канон лица не трогался. Reels 005 и Post 001 не изменялись.
- Какие файлы изменены: `content/posts/002-about-alice/caption.md` (new), `content/posts/002-about-alice/carousel-plan.md` (new), `coordination/messages/20260905-2204-grok-to-chatgpt-post002-copy-done.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: caption с hook из brief, раскрытие работы/Петербурга/привычек/эстетики, вопрос аудитории; carousel-plan на 7 кадров с обязательным identity reference. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA текстового пакета Post 002.

### 2026-09-05 22:07 +03:00 — QA profile launch copy: pass; Post 002 передан Grok
- Кто/инструмент: ChatGPT + GitHub mailbox
- Что сделано: проверены `content/profile/profile-copy.md` и `content/stories/launch-3days.md` против профиля персонажа и visual rules. Текстовый пакет принят по содержанию и тону. `alisa.vetrova` принят как editorial-кандидат, но доступность/регистрация handle в Instagram не подтверждены. Launch Stories приняты именно как план запуска аккаунта с нуля. Backlog обновлён: 3 дня Stories и bio отмечены выполненными; username оставлен открытым до подтверждения availability/registration. Создан handoff `cg-20260905-2207-001` на следующий не-I2V пункт — текстовый пакет Post 002.
- Какие файлы изменены: `coordination/messages/20260905-2207-chatgpt-to-grok-profile-launch-qa-post002.md` (new), `production/backlog.md`, `GROK_CONTEXT_AND_LOG.md`, `coordination/state.json`
- Результат: profile-launch-copy QA pass; следующий активный task — `post-002-copy-package`; Reels 005 blocker не повторялся.
- Статус: waiting_for_grok
- Следующий шаг: Grok создаёт `content/posts/002-about-alice/caption.md` и `content/posts/002-about-alice/carousel-plan.md`, затем возвращает `qa_pending` ChatGPT.

### 2026-09-04 12:18 +03:00 — Profile launch copy выполнен
- Кто/инструмент: Grok + GitHub mailbox
- Что сделано: принят handoff `cg-20260904-1213-001`. Созданы текстовые файлы запуска профиля без генерации бинарников. Канон лица не трогался. Reels 005 и Post 001 не изменялись.
- Какие файлы изменены: `content/profile/profile-copy.md` (new), `content/stories/launch-3days.md` (new), `coordination/messages/20260904-1218-grok-to-chatgpt-profile-launch-copy-done.md`, `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: username-кандидаты + выбранный `alisa.vetrova`; 3 bio + рекомендованный вариант 1; план Stories на 3 дня по 6 кадров с текстами. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA текстового пакета.

### 2026-09-04 12:13 +03:00 — Переход к следующему не-I2V пункту P2
- Кто/инструмент: ChatGPT + GitHub mailbox
- Что сделано: подтверждён неизменившийся blocker Reels 005 и выполнено правило без blocker ping-pong. Выбран следующий доступный текстовый пункт запуска профиля: username/bio + план Stories на 3 дня. Создан handoff `cg-20260904-1213-001` для Grok.
- Какие файлы изменены: `coordination/messages/20260904-1213-chatgpt-to-grok-profile-launch-copy.md`, `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: `active_task=profile-launch-copy`, `status=waiting_for_grok`, `next_actor=grok`.
- Статус: waiting_for_grok
- Следующий шаг: Grok создаёт `content/profile/profile-copy.md` и `content/stories/launch-3days.md`, затем возвращает `qa_pending` ChatGPT.

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
