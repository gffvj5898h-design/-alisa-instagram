# AI handoff automation

## Что автоматизировано

### GitHub transport

`coordination/state.json` определяет текущий ход.

`coordination/messages/` хранит неизменяемые сообщения ChatGPT ↔ Grok.

`.github/workflows/ai-handoff-validate.yml` проверяет корректность state/message handoff при изменениях coordination-файлов.

В протоколе только два actor: `chatgpt` и `grok`. Пользователь не используется как промежуточный actor и не должен вручную переносить сообщения между агентами.

Допустимые `status` в schema v2:

- `waiting_for_grok`
- `waiting_for_chatgpt`
- `in_progress_grok`
- `in_progress_chatgpt`
- `blocked_binary`
- `blocked_tooling`
- `qa_pending`
- `completed`

`ready_for_qa` невалиден; для передачи на QA использовать `qa_pending`.

### Avatar QA

`.github/workflows/avatar-qa.yml` гоняет `production/validate_avatar.py` на изменения аватаров и канона.

Скрипт считает SHA-256, разрешение, квадратность и сверку с `character/references/alice-master-face.jpg`.

Текущий `content/profile/avatar-candidate.jpg` — exact-master fallback 320×400: CI даёт `warn`, не `fail`.

### ChatGPT side

Для ChatGPT настроен condition-watch репозитория раз в час — это максимальная доступная частота для ChatGPT Tasks.

Логика:

- если `next_actor != chatgpt` — ничего не делать по текущему handoff;
- если `next_actor == chatgpt` — прочитать `message_path`, выполнить handoff в рамках repo-правил, создать новый ответ в `coordination/messages/` и передать ход Grok через `state.json`;
- если отсутствует бинарник или инструмент — самостоятельно попробовать доступные bridge / connector / GitHub пути;
- если blocker объективно неразрешим текущими инструментами, зафиксировать его в mailbox и backlog, не просить ручного переноса у пользователя и продолжить следующую доступную задачу.

Это polling, не webhook: реакция ChatGPT может занимать до часа.

### Grok side

Grok должен мониторить `coordination/state.json` максимально часто, насколько позволяет его среда.

Минимально Grok перечитывает state:

- перед каждой операцией;
- после каждой операции;
- после каждого commit;
- после генерации изображения / видео;
- после QA;
- перед ожиданием;
- при каждом доступном периодическом / фоновом цикле.

Если среда Grok поддерживает автоматический polling, используется минимальный доступный разумный интервал.

Если `next_actor=grok`, Grok немедленно читает `message_path`, выполняет задачу и возвращает новый immutable message для ChatGPT. Если `next_actor=chatgpt`, Grok не продолжает старый handoff и только мониторит state.

## Автономность

`user` не является actor.

При blocker:

1. первый агент передаёт blocker второму;
2. второй пытается альтернативный инструмент / bridge;
3. если новых путей нет, задача фиксируется как blocked;
4. агенты переходят к следующему доступному пункту `production/backlog.md`;
5. один и тот же blocker не гоняется бесконечно между агентами без нового факта или изменившегося условия.

## Bootstrap для Grok

Достаточно дать Grok один раз короткую команду:

> Работай по `PROJECT_INSTRUCTIONS.md` и `coordination/PROTOCOL.md`. Мониторь `coordination/state.json` максимально часто. Действуй только когда `next_actor=grok`; бери задачу из `message_path`, отвечай новым файлом в `coordination/messages/` и передавай ход через state. `user` не actor: не проси меня переносить сообщения или ждать моего действия. При блокере передавай его ChatGPT или фиксируй blocked и переходи к следующей доступной задаче.

Текущую задачу нужно брать из mailbox; её не нужно повторно вставлять в чат Grok.
