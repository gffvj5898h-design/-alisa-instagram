# Протокол бинарной выгрузки Grok → GitHub

Цель: дать Grok возможность складывать JPG / PNG / WEBP / MP4 / MOV в repo, даже если его GitHub-инструмент умеет писать только текст.

## Как это работает

Grok НЕ пытается записать бинарник через GitHub API напрямую.

Вместо этого он создаёт один UTF-8 JSON-манифест в:

`production/import-queue/`

GitHub Actions видит новый `*.json`, скачивает бинарный файл по публичной HTTPS-ссылке, проверяет базовую сигнатуру файла, считает SHA-256, кладёт бинарник в `content/...` и создаёт receipt в:

`production/import-receipts/`

Workflow:

`.github/workflows/import-generated-assets.yml`

Importer:

`production/import_generated_asset.py`

---

## Основной режим: public HTTPS URL

Grok должен иметь прямую ссылку, по которой GitHub Actions может скачать сам бинарный файл без cookie, логина и браузерной сессии.

Пример для start-frame Reels 005:

```json
{
  "source_url": "https://PUBLIC-CDN.example/path/generated-image.jpg",
  "target_path": "content/reels/005-same-restaurant/stills/start-frame.jpg",
  "replace": false,
  "max_bytes": 52428800,
  "note": "Reels 005 start-frame candidate v2"
}
```

Сохранить как, например:

`production/import-queue/20260821-reels-005-start-frame-v2.json`

После commit/push workflow запускается автоматически.

## Режим base64

Для небольшого изображения, если Grok реально может получить бинарные bytes и представить их base64, можно использовать:

```json
{
  "base64": "BASE64_DATA_HERE",
  "target_path": "content/reels/005-same-restaurant/stills/start-frame.jpg",
  "replace": false
}
```

Для MP4 этот режим обычно непрактичен из-за размера. Для видео предпочтителен `source_url`.

---

## Что importer проверяет

- только `https://` для URL;
- URL не должен резолвиться в private / loopback / link-local адрес;
- target должен находиться только под `content/`;
- запрещён импорт бинарников напрямую в `character/references/`;
- разрешённые расширения: `.jpg`, `.jpeg`, `.png`, `.webp`, `.mp4`, `.mov`;
- максимум 95 MiB, чтобы не пересечь GitHub hard limit;
- сигнатура файла должна соответствовать расширению;
- если указан `expected_sha256`, он обязан совпасть;
- существующий target не заменяется, пока явно не указано `"replace": true`.

После успешного импорта создаётся receipt с размером и SHA-256.

---

## Важно для публичного репозитория

`production/import-queue/*.json` попадает в публичную Git-историю.

Не помещать туда:
- приватные URL;
- bearer-токены;
- cookie;
- API keys;
- ссылки, доступ к которым даёт секретный query parameter, если его раскрытие нежелательно.

Использовать только URL, который безопасно сделать публичным. Если у Grok есть только локальный attachment/chat-id или приватный URL, он должен остановиться и передать бинарник пользователю / ChatGPT для ручного bridge-upload.

---

## Инструкция Grok после генерации файла

1. Получить прямой downloadable HTTPS URL генерации.
2. Не менять канон Алисы и не перегенерировать файл ради выгрузки.
3. Создать JSON в `production/import-queue/`.
4. Указать точный `target_path`.
5. Не выставлять `replace: true`, если пользователь явно не просил заменить существующий файл.
6. Подождать GitHub Actions.
7. Проверить наличие target и receipt.
8. Сверить размер и SHA-256 из receipt.
9. Только после этого обновлять `result-notes.md` и `GROK_CONTEXT_AND_LOG.md`.

## Пример проверки результата

Ожидаемые файлы:

- `content/reels/005-same-restaurant/stills/start-frame.jpg`
- `production/import-receipts/20260821-reels-005-start-frame-v2.md`

Если receipt не появился, смотреть GitHub Actions run `Import generated assets` и не утверждать, что файл загружен.
