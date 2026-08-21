# Result notes — Reels 005

## Текущий статус

Стартовый кадр v2: тот же кадр, исправлен только вид за окном под Санкт-Петербург.
Identity reference: `character/references/alice-master-face.jpg`.
Видео не генерировалось.

Файл залит в repo:

`content/reels/005-same-restaurant/stills/start-frame.jpg`

- размер изображения: 1008×1792
- размер файла: 356333 bytes
- Git blob SHA: `33a5b529b122517fa7d2685ac267cf5ad279d1cc`
- SHA-256: `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`

Статус: **start-frame candidate v2 in repo / pending Grok QA**. Не approved.

## QA v2

- identity: лицо сохранено относительно принятого кадра и master-face; Grok должен повторно сверить файл из repo
- возраст: ~40
- одежда / поза / стол / ноутбук / телефон / образцы: не менять
- руки: проверить по repo-файлу
- фон: исторический Санкт-Петербург, без московских высоток
- формат: 1008×1792, строго 9:16, выше минимального production gate 720×1280
- бинарная целостность: SHA-256 зафиксирован выше

## QA decision

Не approved до повторного Grok QA файла из repo. 15-секундное видео не генерировалось и до QA start-frame не генерировать.
