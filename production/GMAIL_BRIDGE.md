# Gmail-мост для бинарников Grok → ChatGPT

GitHub API у Grok пишет только текст. Если нет публичного HTTPS URL и chunk-import через `production/GROK_BINARY_UPLOAD.md` недоступен, Grok отправляет JPG/PNG/MP4 письмом.

Аккаунт: `roman12101992@gmail.com`
Письма: от этого адреса самому себе.
ChatGPT подключён к тому же Gmail и забирает вложения.

Канон `character/references/alice-master-face.jpg` этим мостом **не** заменяется.

---

## Тема письма (обязательный формат)

```
ALISA-BRIDGE | SAVE_TO=<repo-path> | KIND=<kind> | FROM=grok | SHA256=<hex>
```

Примеры:

```
ALISA-BRIDGE | SAVE_TO=content/reels/005-same-restaurant/stills/start-frame.jpg | KIND=start-frame | FROM=grok | SHA256=...
ALISA-BRIDGE | SAVE_TO=content/profile/avatar-candidate-imagine-800.jpg | KIND=avatar | FROM=grok | SHA256=...
ALISA-BRIDGE | SAVE_TO=content/reels/005-same-restaurant/exports/attempt-02.mp4 | KIND=video | FROM=grok | SHA256=...
```

`SAVE_TO` — единственное место, куда ChatGPT кладёт файл.
`KIND`: `start-frame` | `still` | `avatar` | `video` | `other`

---

## Тело письма

```
ALISA-BRIDGE
FROM: grok
TO: chatgpt
KIND: ...
SAVE_TO: content/...
FILENAME: ...
SHA256: ...
RESOLUTION: WxH
MIME: image/jpeg | video/mp4
DO_NOT_TOUCH: character/references/alice-master-face.jpg
```

Дальше 3–6 строк: что это, что сделать, чего не делать.

---

## Поиск для ChatGPT

```
subject:ALISA-BRIDGE has:attachment newer_than:7d
```

---

## Что делает ChatGPT

1. Находит непрочитанные / новые письма с `subject:ALISA-BRIDGE`.
2. Читает тему: берёт `SAVE_TO` и `SHA256`.
3. Скачивает вложение.
4. Сверяет SHA-256.
5. Заливает **только** в `SAVE_TO` под `content/`.
6. Не трогает `character/references/`.
7. Пишет receipt в журнал и `result-notes` эпизода.
8. Возвращает handoff Grok через `coordination/`.

Если SHA не совпал — не заливать, статус `rejected`.

---

## Что делает Grok

1. Сначала пробует `production/GROK_BINARY_UPLOAD.md`.
2. Если бинарник нельзя положить в GitHub — письмо себе.
3. Тема строго по шаблону.
4. Одно вложение = один target path.
5. После отправки пишет запись в `GROK_CONTEXT_AND_LOG.md`.
