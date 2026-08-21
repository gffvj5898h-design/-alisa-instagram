# AI handoff automation

## Что автоматизировано

### GitHub transport

`coordination/state.json` определяет текущий ход.

`coordination/messages/` хранит неизменяемые сообщения ChatGPT ↔ Grok.

`.github/workflows/ai-handoff-validate.yml` проверяет корректность state/message handoff при изменениях coordination-файлов.

### ChatGPT side

Для ChatGPT настроен condition-watch репозитория раз в час.

Логика:

- если `next_actor != chatgpt` — ничего не делать и не уведомлять пользователя;
- если `next_actor == chatgpt` — прочитать `message_path`, выполнить handoff в рамках repo-правил, создать новый ответ в `coordination/messages/` и передать ход следующему actor через `state.json`;
- если нужен отсутствующий бинарник — перевести state в `waiting_for_user` и указать точный требуемый файл.

Это polling, а не webhook: реакция ChatGPT может занимать до часа.

### Grok side

Этот репозиторий не может сам запустить внешнюю сессию Grok.

Grok должен либо:

- иметь собственный механизм периодической проверки GitHub, если такой механизм доступен пользователю;
- либо при запуске/продолжении сессии Grok сначала читать `PROJECT_INSTRUCTIONS.md` и `coordination/state.json`.

После этого длинные handoff-промпты вручную между ChatGPT и Grok не нужны.

## Одноразовый bootstrap для Grok

Достаточно дать Grok один раз короткую команду:

> Работай по `PROJECT_INSTRUCTIONS.md` и `coordination/PROTOCOL.md`. Перед каждым действием читай `coordination/state.json`. Если `next_actor=grok`, обрабатывай `message_path` и отвечай через новый файл в `coordination/messages/`, затем передавай ход через `state.json`. Не проси меня переносить длинные сообщения между тобой и ChatGPT.

Текущая задача уже находится в mailbox; её не нужно повторно вставлять в чат Grok.
