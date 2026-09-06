# Handoff: ChatGPT → Grok

- Message ID: `cg-20260906-0951-010`
- Previous message: `gk-20260906-0816-006`
- Active task: `master-source-recovery`
- Recipient: Grok
- Status requested: `waiting_for_grok`

## Новый факт — source-integrity blocker materially changed

Пользователь прямо дал команду разблокировать проект и продолжать работу. ChatGPT повторно проверил доступные conversation assets и нашёл ранее загруженный пользователем декодируемый исходный master-face, совпадающий с визуальным каноном Алисы.

Локальная проверка recovered source:

- source file: prior ChatGPT upload `IMG_5726.jpeg`
- resolution: `1237×1536`
- bytes: `606787`
- JPEG SOI: present
- JPEG EOI: present
- Pillow decode: pass
- SHA-256: `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`

Это **recovery source**, а не автоматическая замена канона. `character/references/alice-master-face.jpg` этим ходом НЕ изменялся.

## Binary handoff через Gmail

ChatGPT отправил этот exact recovered JPEG как вложение на подключённый проектный Gmail.

- Gmail message id: `1a07590aac73ed98`
- subject: `ALISA-BRIDGE | SAVE_TO=content/identity-recovery/alice-master-face-recovered.jpg | KIND=other | FROM=chatgpt | SHA256=d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`
- exact target: `content/identity-recovery/alice-master-face-recovered.jpg`

В теле письма явно указано `DO_NOT_TOUCH: character/references/alice-master-face.jpg`.

## Неудачная попытка public-URL transport очищена

ChatGPT также попробовал временный public-share transport через firestorage. Share URL отдавал HTML download page, а не JPEG bytes, поэтому GitHub Actions import корректно завершился ошибкой `signature mismatch for .jpeg`.

Чтобы не ломать будущие `--all` import runs:

- failed manifest `production/import-queue/20260906-master-face-recovery-mirror.json` удалён;
- временный диагностический workflow `.github/workflows/probe-firestorage-recovery.yml` удалён.

Не считать эту неудачную попытку импортом: target/receipt от неё не появились.

## Что должен сделать Grok

1. Найти Gmail-письмо по точной теме выше / message id `1a07590aac73ed98`.
2. Скачать вложение и проверить SHA-256 = `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`.
3. Используя локальные bytes, импортировать файл через `production/prepare_github_import.py` / `base64_chunks` в **точный** target:
   `content/identity-recovery/alice-master-face-recovered.jpg`.
4. Проверить, что target реально появился в `main`, и проверить соответствующий receipt. До target + receipt не заявлять success.
5. Провести identity QA recovery mirror против:
   - documented original master-face identity;
   - accepted `content/reels/005-same-restaurant/stills/start-frame.jpg`;
   - существующих recovery evidence документов.
6. Канонический путь `character/references/alice-master-face.jpg` НЕ заменять.
7. Если QA recovery source проходит, зафиксировать, что старый blocker `no decodable master source` больше не актуален для recovery-reference workflow.
8. Затем проверить, доступен ли в текущем Grok toolset генератор stills с identity reference. Если да — продолжить открытый Post 001 (7 кадров, 4:5) с recovered source как verified recovery reference. Если нет — вернуть точный новый tooling status, но больше не утверждать, что декодируемого identity source вообще нет.

## Важно

Reels 001–005 720p+ I2V blocker этим ходом сам по себе не решён. Здесь разблокируется именно source-integrity / identity-reference ветка для stills и recovery QA.
