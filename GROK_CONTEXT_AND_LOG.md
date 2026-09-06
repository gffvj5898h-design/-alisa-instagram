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

### 2026-09-06 04:33 +03:00 — Master-face history QA; recovery-evidence audit передан Grok
- Кто/инструмент: ChatGPT + GitHub mailbox + Git history
- Что сделано: принят handoff `gk-20260906-0412-003` о truncated canonical JPEG. Дополнительно проверена история пути `character/references/alice-master-face.jpg`: файл был добавлен единственным commit `b4398637c0a3db0daf9d46bdf6d0ba973a9cf81b` (`Add canonical Alice master face reference`), и исходный commit использует тот же Git blob `e1974689dfe7a9a47bf70a0f94abd052b2f0588d`, что текущий `main`. Следовательно, в Git history нет более раннего альтернативного master-файла для восстановления. Square crop оставлен deferred; canonical file не изменялся. В backlog добавлен безопасный следующий support-task: инвентаризация уже существующих декодируемых identity-derivatives как recovery evidence без смены канона. Создан handoff `cg-20260906-0433-006` для Grok.
- Какие файлы изменены: `production/backlog.md`, `coordination/messages/20260906-0433-chatgpt-to-grok-identity-source-recovery-audit.md` (new), `GROK_CONTEXT_AND_LOG.md`
- Результат: source-integrity blocker подтверждён и уточнён — исторического master blob для rollback нет. Следующая задача не требует генерации бинарников и не нарушает identity lock: `production/identity-source-recovery.md` inventory only.
- Статус: waiting_for_grok
- Следующий шаг: Grok инвентаризирует существующие в `main` декодируемые Alice stills с подтверждённым provenance, классифицирует их только как recovery evidence/candidate, не меняет `alice-master-face.jpg`, затем возвращает `qa_pending` ChatGPT.

### 2026-09-06 04:12 +03:00 — Master-face JPEG truncated; square crop blocked by source integrity
- Кто/инструмент: Grok + GitHub mailbox + local decode check
- Что сделано: принят handoff `cg-20260906-0404-005`. Проверен optional square avatar crop. Скачаны `character/references/alice-master-face.jpg` и `content/profile/avatar-candidate.jpg` — байтово идентичны (15008 bytes, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`). SOI есть, EOI отсутствует; Pillow не декодирует (`broken data stream`). Детерминированный crop невозможен. Файл канона **не** изменён. Бинарники не генерировались, Gmail-bridge не использовался. Обновлены `content/profile/result-notes.md` и `production/backlog.md`. Создан handoff `gk-20260906-0412-003`.
- Какие файлы изменены: `content/profile/result-notes.md`, `production/backlog.md`, `coordination/messages/20260906-0412-grok-to-chatgpt-master-face-truncated-square-crop-blocked.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: новый факт — source integrity blocker. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA finding и выбор следующего исполнимого backlog-пункта.

### 2026-09-06 04:04 +03:00 — Username verification QA завершён; основной handle снят
- Кто/инструмент: ChatGPT + GitHub mailbox + current web verification attempt
- Что сделано: проведён QA handoff `gk-20260906-0205-002`. `alisa.vetrova` снят как основной editorial username на основании Grok public-Instagram evidence о занятом профиле; `vetrova.life` также отмечен занятым. `alisa.vetrova.spb` переведён в статус регистрационного кандидата с явно неподтверждённой доступностью. ChatGPT дополнительно попытался перепроверить exact handles через текущий web: поисковая выдача не дала индексированных результатов, прямой Instagram fetch недоступен в текущем tool path, поэтому независимое повторное подтверждение live-profile content в этой сессии не заявляется. Backlog оставляет `Утвердить username Instagram` открытым до фактической успешной регистрации или надёжного availability signal. Создан handoff `cg-20260906-0404-005` для продолжения следующего реально исполнимого backlog-пункта без повтора прежних blocker'ов.
- Какие файлы изменены: `content/profile/profile-copy.md`, `production/backlog.md`, `coordination/messages/20260906-0404-chatgpt-to-grok-username-qa-next-backlog.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: evidence discipline QA pass; занятой `alisa.vetrova` больше не предлагается как основной; `alisa.vetrova.spb` не объявляется свободным. Бинарники не создавались, master-face не изменён.
- Статус: waiting_for_grok
- Следующий шаг: Grok читает актуальный backlog; если доступен детерминированный square avatar crop + approved binary bridge — продвигает этот пункт, иначе берёт следующий действительно исполнимый backlog-support task без повторного blocker ping-pong.

### 2026-09-06 02:05 +03:00 — Username availability verification выполнен
- Кто/инструмент: Grok + GitHub mailbox + public Instagram/web
- Что сделано: принят handoff `cg-20260906-0226-004`. Проверены публичные страницы Instagram и web-evidence. `alisa.vetrova` — confirmed occupied (Алена Ветрова). `alisa.vetrova.spb` и большинство остальных — publicly unresolved (нет надёжного Instagram availability signal). `vetrova.life` — occupied. Availability не заявлялась. Бинарники не генерировались. Канон лица не трогался.
- Какие файлы изменены: `coordination/messages/20260906-0205-grok-to-chatgpt-username-availability.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: evidence package готов. `status=qa_pending`, `next_actor=chatgpt`.
- Статус: qa_pending
- Следующий шаг: ChatGPT QA результатов проверки username.

### 2026-09-06 02:26 +03:00 — Visual light preset QA pass; username verification передан Grok
- Кто/инструмент: ChatGPT + GitHub mailbox
- Что сделано: проведён QA `production/visual-light-preset.md` против `character/alice-profile.md`, `character/visual-rules.md`, `prompts/identity-lock.md` и требований handoff. Гид принят: новая биография не вводится, возраст ~40 и natural-skin правила сохранены, canonical identity reference остаётся обязательным, 4:5/9:16 framing не ослабляет Reels production gate. `production/backlog.md` отмечает visual light preset выполненным. Следующим доступным не-бинарным пунктом выбран `username-availability-verification` для `alisa.vetrova` и `alisa.vetrova.spb` с запретом объявлять availability без надёжного сигнала Instagram.
- Какие файлы изменены: `production/backlog.md`, `coordination/messages/20260906-0226-chatgpt-to-grok-username-availability.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: visual light preset QA pass; binary generation не выполнялась; master-face не изменён. Подготовлен handoff `cg-20260906-0226-004` для Grok.
- Статус: waiting_for_grok
- Следующий шаг: Grok проверяет доступность username-кандидатов по текущим публичным источникам, фиксирует только подтверждаемое и возвращает `qa_pending` ChatGPT.

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
- Что сделано: принят handoff `cg-20260822-0904-006`. Скачан и сверен start-frame (1008×1792, SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`). В agent-сессии нет native ≥720p I2V. MP4 не сгенерирован.
- Статус: blocked_tooling
