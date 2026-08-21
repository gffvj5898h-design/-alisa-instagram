# Binary import queue

Grok кладёт сюда один `*.json` манифест на каждый бинарный импорт.

Три режима (ровно один ключ в JSON):

1. `source_url` — публичный HTTPS.
2. `base64` — маленький файл целиком.
3. `base64_chunks` — список текстовых кусков в `chunks/<slug>/`.

Подготовка локального файла:

`python3 production/prepare_github_import.py SRC content/... --slug SLUG`

Полный протокол: `production/GROK_BINARY_UPLOAD.md`.

Не класть credentials, cookie, API keys и private signed URL в этот публичный репозиторий.
