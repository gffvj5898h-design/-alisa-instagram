# Reels master registry — QA hold

Файл сохраняет историческое имя `approved-reels.md`, но текущие MP4 001–004 **не считаются финальными production-approved master**: их разрешение 512×910 ниже production gate 720×1280.

SHA-256 ниже не менялись и принимаются как сверенные Grok-аудитом.

| Reels | Тема | Длительность | Кадр | SHA-256 исходного MP4 | Статус |
|---|---|---:|---|---|---|
| 001 | Первое свидание после долгой паузы | 15.041667 с | 512×910, 30 fps | `5259ee5c812bfbf43658531392fcc8b47704531a4b804fede86a11422ad0f736` | candidate / QA hold: low-res |
| 002 | Возвращение после провального свидания | 15.041667 с | 512×910, 30 fps | `94cb5b9aa4524d729092f766588717c9a7d85791c55e04d69f1f7cf703e12b5d` | candidate / QA hold: low-res |
| 003 | Утро после, кофе и новое сообщение | 15.033333 с | 512×910, 30 fps | `a09f09486c78b2f1fd73591fffeae67a8328099bdbbd3e6789455907b41e60a3` | candidate / QA hold: low-res |
| 004 | Неизвестный знает о вчерашнем свидании | 15.041667 с | 512×910, 30 fps | `d2b7454244fd6e1ed5bc0593fe10787354985942d65669af3bdbe0c4a6b7fb55` | candidate / QA hold: low-res |

## Текущие пути candidate-master

Папка `output/approved/` сохранена как legacy-путь хранения и сама по себе не означает production approval.

- `content/reels/001-first-date/output/approved/reels-001-approved.mp4`
- `content/reels/002-bad-date-home/output/approved/reels-002-approved.mp4`
- `content/reels/003-morning-after/output/approved/reels-003-approved.mp4`
- `content/reels/004-who-knows/output/approved/reels-004-approved.mp4`

## Gate для production-approved

Ролик можно перевести в production-approved только когда одновременно выполнено:
1. пакет документации `concept.md`, `prompt-grok.md`, `storyboard.md`, `result-notes.md`;
2. 9:16 и минимум 720×1280;
3. identity QA против `character/references/alice-master-face.jpg`;
4. длительность и сюжет сверены;
5. Grok повторно проверил файлы репозитория.
