# ChatGPT ↔ Grok coordination protocol

GitHub — единственный транспорт и источник истины для handoff между ChatGPT и Grok по этому проекту.

## Обязательное чтение перед работой

Каждый агент перед действием читает:

1. `PROJECT_INSTRUCTIONS.md`
2. `GROK_CONTEXT_AND_LOG.md`
3. `coordination/PROTOCOL.md`
4. `coordination/state.json`
5. файл из поля `message_path` в `coordination/state.json`
6. пакет конкретного Reels / поста, если он указан в сообщении

## Модель очереди

Все сообщения неизменяемые и создаются как новые файлы в:

`coordination/messages/`

Формат имени:

`YYYYMMDD-HHMM-<sender>-to-<recipient>-<slug>.md`

Примеры:

- `20260822-0033-chatgpt-to-grok-reels005-rerun.md`
- `20260822-0045-grok-to-chatgpt-reels005-result.md`

Старые message-файлы не редактировать и не удалять.

## `coordination/state.json`

Это единственный изменяемый указатель очереди.

Ключевые поля:

- `active_task` — текущая задача;
- `status` — состояние handoff;
- `next_actor` — кто должен действовать следующим: `chatgpt`, `grok` или `user`;
- `message_path` — конкретный message-файл, который должен прочитать `next_actor`;
- `last_chatgpt_message_id`;
- `last_grok_message_id`;
- `requires_user` — нужен ли ручной шаг пользователя.

## Правило хода

Агент действует только если `next_actor` совпадает с ним.

Если `next_actor` не совпадает:

- ничего не генерировать;
- не менять рабочие файлы;
- не перехватывать задачу другого агента.

## Как ответить

После выполнения своего шага агент обязан:

1. Создать НОВЫЙ `.md` в `coordination/messages/`.
2. В ответе указать факты, изменённые файлы, SHA / параметры бинарника при наличии и следующий требуемый шаг.
3. Обновить `coordination/state.json`:
   - `updated_at`;
   - `status`;
   - `next_actor`;
   - `message_path` на новый ответ;
   - свой `last_*_message_id`.
4. Добавить содержательную операцию СВЕРХУ в `GROK_CONTEXT_AND_LOG.md`, не сокращая старые записи.

## Статусы

Рекомендуемые значения:

- `waiting_for_grok`
- `waiting_for_chatgpt`
- `waiting_for_user`
- `in_progress_grok`
- `in_progress_chatgpt`
- `blocked_binary`
- `blocked_tooling`
- `qa_pending`
- `completed`

## Бинарники

Для JPG / PNG / WEBP / MP4 / MOV действует `production/GROK_BINARY_UPLOAD.md`.

Если Grok имеет прямой публичный downloadable HTTPS URL:

- ставит manifest в `production/import-queue/`;
- ждёт import receipt;
- только после receipt сообщает, что файл в repo.

Если Grok имеет только chat-local attachment / private URL:

- НЕ перегенерирует результат ради выгрузки;
- создаёт сообщение ChatGPT со статусом `blocked_binary`;
- ставит `next_actor: "chatgpt"` или `next_actor: "user"` в зависимости от того, доступен ли бинарник ChatGPT в текущем чате.

ChatGPT не должен утверждать, что бинарник загружен, пока файл реально не появился в `main`.

## Production gate

Mailbox не отменяет проектные требования. Нельзя автоматически переводить результат в `approved` только потому, что оба агента обменялись сообщениями.

Для Reels по-прежнему действуют `PROJECT_INSTRUCTIONS.md`, `production/backlog.md`, пакет эпизода и повторный QA.

## Конфликты

Если GitHub и память агента расходятся — побеждает GitHub.

Если `state.json` ссылается на отсутствующий message-файл — остановиться со статусом `blocked_tooling`; не угадывать содержание сообщения.

Если два агента одновременно изменили state — сначала перечитать актуальный `main`, затем отвечать новым message-файлом; старый handoff не переписывать.
