# Протокол бинарной выгрузки Grok → GitHub

Цель: складывать JPG / PNG / WEBP / MP4 / MOV в `content/`, даже если GitHub-инструмент Grok пишет только UTF-8 текст.

Grok **не** записывает бинарник через Contents API напрямую.

Импорт делает GitHub Actions:

- workflow: `.github/workflows/import-generated-assets.yml`
- importer: `production/import_generated_asset.py`

Очередь: один UTF-8 JSON в `production/import-queue/*.json`.

---

## Автоматический режим для локального файла (рекомендуется Grok)

Если файл уже есть на диске (Imagine render, скачанный still, сжатый JPEG):

```bash
python3 production/prepare_github_import.py /path/to/file.jpg \
  content/profile/avatar-candidate.jpg \
  --slug 20260822-avatar-imagine-1080 \
  --note "short public note" \
  --replace   # только если target уже существует и его нужно заменить
```

Скрипт создаёт:

- `production/import-queue/chunks/<slug>/part-NN.txt` — куски base64 по 50k символов;
- `production/import-queue/<slug>.json` — манифест с `base64_chunks` и `expected_sha256`.

Дальше Grok коммитит **только эти текстовые файлы** одним `push_files` / несколькими `create_or_update_file`.

После push:

1. Дождаться run `Import generated assets`.
2. Проверить `content/...` в `main`.
3. Проверить receipt `production/import-receipts/<slug>.md`.
4. Сверить bytes и SHA-256.
5. Только после receipt писать в mailbox, что файл загружен.

Не коммитить `*.files.json` и не класть сырой base64 целиком в один огромный JSON, если файл больше ~30 KiB.

Алиас: `production/queue_local_image.py` делает то же самое внутри clone.

---

## Режим public HTTPS URL

Если есть прямая публичная ссылка без cookie / логина / секретного query:

```json
{
  "source_url": "https://PUBLIC-CDN.example/path/generated-image.jpg",
  "target_path": "content/reels/005-same-restaurant/stills/start-frame.jpg",
  "replace": false,
  "max_bytes": 52428800,
  "note": "Reels 005 start-frame candidate"
}
```

Сохранить как `production/import-queue/<slug>.json` и push.

Для MP4 / больших файлов это предпочтительный режим.

---

## Режим embedded base64

Только для очень маленького файла, который целиком влезает в один текстовый commit:

```json
{
  "base64": "BASE64_DATA_HERE",
  "target_path": "content/profile/avatar-candidate.jpg",
  "replace": false,
  "expected_sha256": "..."
}
```

---

## Что importer проверяет

- ровно один источник: `source_url` **или** `base64` **или** `base64_chunks`;
- `source_url` только `https://`, без private / loopback адресов;
- chunks только под `production/import-queue/chunks/`;
- target только под `content/`;
- импорт в `character/references/` запрещён;
- расширения: `.jpg`, `.jpeg`, `.png`, `.webp`, `.mp4`, `.mov`;
- максимум 95 MiB;
- сигнатура файла должна соответствовать расширению;
- `expected_sha256` обязан совпасть, если указан;
- существующий target не заменяется без `"replace": true`.

---

## Публичный репозиторий

`production/import-queue/` попадает в историю Git. Не класть:

- приватные URL;
- bearer-токены, cookie, API keys;
- signed URL с секретом в query.

---

## После генерации

1. Не менять канон Алисы и не перегенерировать файл только ради выгрузки.
2. Если есть локальные bytes — `prepare_github_import.py` + commit chunks.
3. Если есть публичный HTTPS — манифест с `source_url`.
4. Если bytes недоступны ни Grok, ни ChatGPT — `blocked_binary`, переход к следующей задаче backlog. Пользователь не actor.
5. Не утверждать загрузку до target + receipt в `main`.
