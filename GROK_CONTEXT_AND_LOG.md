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

### 2026-09-06 12:20 +03:00 — ChatGPT QA recovered master source; square-avatar crop разблокирован
- Кто/инструмент: ChatGPT + connected Gmail + GitHub mailbox
- Что сделано: принят `gk-20260906-0808-007`. ChatGPT повторно прочитал Gmail message `1a07590aac73ed98` и exact attachment `alice-master-face-original.jpeg`: MIME `image/jpeg`, 606787 bytes, subject SHA-256 `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`. Это совпадает с независимой проверкой Grok: 1237×1536, тот же SHA-256, Pillow pass. Recovery source принят для non-generative recovery-reference work; канонический `character/references/alice-master-face.jpg` не менялся. Repo mirror признан полезным, но не обязательным для следующего шага, поскольку оба агента независимо подтвердили одно и то же Gmail-вложение/checksum. Исторический source-integrity blocker для optional square avatar crop снят.
- Какие файлы изменены: `coordination/messages/20260906-1220-chatgpt-to-grok-avatar-square-crop-recovery.md` (new), `production/backlog.md`, `GROK_CONTEXT_AND_LOG.md`, далее `coordination/state.json`.
- Результат: следующий исполнимый пункт — non-generative face-safe square crop из verified recovered JPEG с binary bridge и повторным avatar QA. Reels 005 I2V blocker отдельно остаётся.
- Статус: completed / waiting_for_grok
- Следующий шаг: Grok повторно проверяет checksum recovered source, делает crop/resize без генеративного изменения лица, помещает candidate только под `content/profile/`, проверяет dimensions/SHA/QA и возвращает `qa_pending` ChatGPT.

### 2026-09-06 11:08 +03:00 — Grok: recovered master source verified, identity QA pass, handoff ChatGPT
- Кто/инструмент: Grok + Gmail attachment download + Pillow + GitHub mailbox
- Что сделано: принят `cg-20260906-0951-010`. Найдено Gmail `1a07590aac73ed98`. Вложение скачано, SHA-256 `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767` подтверждён, 1237×1536, Pillow pass. Канон `character/references/alice-master-face.jpg` не тронут. Identity QA recovery source vs accepted start-frame 005: continuity pass. `prepare_github_import.py` выполнен локально (slug 20260906-master-face-recovered); full chunks push ограничен объёмом text tool — существующее Gmail-письмо от ChatGPT оставлено без дубля. Post 001 still-generation: автономный identity-ref still generator в текущем toolset не подтверждён, генерация не запускалась. Reels 005 I2V не трогался.
- Какие файлы изменены: `coordination/messages/20260906-0808-grok-to-chatgpt-master-source-ingested.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: blocker `no decodable master source` снят для recovery workflow. `status=qa_pending`, `next_actor=chatgpt`, `last_grok_message_id=gk-20260906-0808-007`
- Статус: qa_pending
- Следующий шаг: ChatGPT подтверждает QA / при необходимости завершает repo-mirror из Gmail / выбирает следующий executable backlog item.

### 2026-09-06 09:51 +03:00 — Найден декодируемый original master source; recovery handoff Grok
- Кто/инструмент: ChatGPT + conversation Files + Pillow + Gmail + GitHub mailbox
- Что сделано: по прямой команде пользователя разблокировать проект ChatGPT повторно проверил ранее загруженные conversation assets и нашёл `IMG_5726.jpeg`, совпадающий с каноническим образом Алисы. Файл материализован и независимо декодирован: 1237×1536, 606787 bytes, JPEG SOI+EOI present, Pillow pass, SHA-256 `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`. Канонический repo-файл `character/references/alice-master-face.jpg` НЕ заменялся.
- Binary transport: exact recovered JPEG отправлен вложением через Gmail, message id `1a07590aac73ed98`, target для recovery mirror `content/identity-recovery/alice-master-face-recovered.jpg`. Grok должен скачать bytes, сверить SHA, импортировать через base64_chunks и подтвердить target + receipt.
- Неудачный public-share эксперимент: firestorage share page отдавал HTML, importer получил `signature mismatch for .jpeg`; failed manifest и временный probe workflow удалены, чтобы не ломать будущие import runs.
- Какие файлы изменены: удалены `production/import-queue/20260906-master-face-recovery-mirror.json` и `.github/workflows/probe-firestorage-recovery.yml`; создан `coordination/messages/20260906-0951-chatgpt-to-grok-master-source-recovered.md`; далее обновляются `GROK_CONTEXT_AND_LOG.md` и `coordination/state.json`.
- Результат: blocker `no decodable master source` materially changed. Recovery source теперь реально существует и передан Grok; canonical replacement не выполнялся. I2V 720p+ blocker отдельно остаётся.
- Статус: waiting_for_grok
- Следующий шаг: Grok ingest + receipt + identity QA recovered source, затем проверка возможности Post 001 still generation с identity reference.

### 2026-09-06 08:21 +03:00 — ChatGPT park: Gmail пуст, открытый backlog классифицирован
- Кто/инструмент: ChatGPT + GitHub mailbox + connected Gmail
- Что сделано: принят `gk-20260906-0816-006`. Выполнен Gmail-поиск `subject:ALISA-BRIDGE has:attachment newer_than:7d` — совпадений нет, ingest не выполнялся. Перечитан `production/backlog.md`; все оставшиеся открытые checkbox'ы классифицированы. Текстовых автономно исполнимых пунктов не осталось. Канон не менялся; изображения/видео не генерировались.
- Какие файлы изменены: `coordination/messages/20260906-0821-chatgpt-to-chatgpt-backlog-park.md` (new), `GROK_CONTEXT_AND_LOG.md`, далее `coordination/state.json`.
- Результат: Reels 001–005 / их QA / registry, avatar crop и Post 001 остаются `blocked_same_as_before`; username остаётся `needs_user_registration_signal`. Очередь паркуется на ChatGPT без повторной передачи тех же blocker'ов Grok.
- Статус: blocked_tooling
- Следующий шаг: следующий hourly poll сначала проверяет state/Gmail/новые условия; если изменений нет — не создаёт дублирующий blocker-handoff и не меняет repo.

### 2026-09-06 08:16 +03:00 — Grok recheck; ход вернут ChatGPT с явным next_actor
- Кто/инструмент: Grok + GitHub mailbox
- Что сделано: принят `cg-20260906-0708-008`. Повторная проверка условий: нет native 720p+ I2V; канонический JPEG по-прежнему truncated (15008 bytes, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`, EOI нет, Pillow fail); нового username signal нет. Канон не трогал. Reels 005 не генерировал. Ход закрыт mailbox-сообщением с инструкциями ChatGPT (скан Gmail ALISA-BRIDGE, разметка backlog на executable vs blocked, park с явным next_actor).
- Какие файлы изменены: `coordination/messages/20260906-0816-grok-to-chatgpt-recheck-no-new-condition.md` (new), `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: `status=blocked_tooling`, `next_actor=chatgpt`, `last_grok_message_id=gk-20260906-0816-006`
- Статус: blocked_tooling
- Следующий шаг: ChatGPT выполняет инструкции из message_path; не возвращает те же blocker'ы Grok без нового факта.

### 2026-09-06 07:08 +03:00 — ChatGPT QA identity-video-recovery; открытый backlog полностью заблокирован
- Кто/инструмент: ChatGPT + GitHub mailbox
- Что сделано: проведён QA `production/identity-video-recovery.md` по доступным в `main` данным. Пути, длительности, разрешение/FPS и SHA-256 Reels 001–004 сверены с соответствующими `result-notes.md` и совпадают. Классификация `supporting_recovery_evidence` принята как evidence-only; sampled-frame continuity в документе корректно отделена как визуальная интерпретация Grok. `Decode OK` и визуальные observations не переобъявлены независимой проверкой ChatGPT, потому что отдельный decode receipt/извлечённые кадры в repo не коммитились. Канон не менялся.
- Какие файлы изменены: `coordination/messages/20260906-0708-chatgpt-to-grok-backlog-blocked.md` (new), `GROK_CONTEXT_AND_LOG.md`, далее `coordination/state.json`.
- Результат: QA pass по repository-verifiable фактам. После проверки `production/backlog.md` не найдено открытых автономно исполнимых пунктов без повторения уже известных blocker'ов: 720p+ I2V, Post 001 identity-reference при повреждённом canonical JPEG, optional avatar crop по той же причине, username без надёжного availability/registration signal.
- Статус: blocked_tooling
- Следующий шаг: Grok не повторяет blocker ping-pong; повторная работа только при новом факте, восстановленном валидном каноническом source, новом совместимом инструменте или надёжном username signal.

### 2026-09-06 06:08 +03:00 — Identity-video-recovery audit выполнен (Reels 001–004)
- Кто/инструмент: Grok + GitHub mailbox + local ffprobe/ffmpeg frame inspection
- Что сделано: принят handoff `cg-20260906-0533-007`. Создан `production/identity-video-recovery.md`. Все четыре committed candidate-master MP4 декодируются (H.264, 512×910, ~15 с). SHA-256 совпали с `result-notes.md`. Documented provenance = master-face identity reference. Локально извлечены representative frames (n≈0/150/300/450) только для осмотра; **кадры не коммитились**. Визуальная непрерывность с accepted start-frame 005 подтверждена. Классификация каждой: `supporting_recovery_evidence`. Канон не изменён.
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
