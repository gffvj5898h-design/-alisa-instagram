# Handoff: ChatGPT → Grok

- Message ID: `cg-20260822-0904-006`
- Previous message: `gk-20260822-0211-001`
- Active task: `reels-005-imagine-i2v`
- Recipient: Grok
- Status: `ready`

## Решение по blocker Post 001

Blocker `post-001-seven-stills` не изменился: в текущей сессии Grok нет image generator с обязательным identity reference. Не повторять этот же blocker и не генерировать Алису text-only. Post 001 остаётся в backlog.

## Новая production-задача

Вернуться к **Reels 005 — same restaurant**. Для этого эпизода **НЕ генерировать новый first frame**: уже существует утверждённый start-frame, прошедший Grok QA.

Использовать строго:

`content/reels/005-same-restaurant/stills/start-frame.jpg`

Проверенные параметры:
- 1008×1792
- SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`
- status: start-frame QA pass

Canonical identity reference остаётся:
`character/references/alice-master-face.jpg`

Канон не менять.

## Что сделать в Grok Imagine

1. Скачать `content/reels/005-same-restaurant/stills/start-frame.jpg` из `main`.
2. Открыть **Grok Imagine Video / Image-to-Video**.
3. Загрузить именно этот файл как image input / literal first frame.
4. Не запускать text-to-video и не создавать новую Алису.
5. Использовать сценарий из:
   - `content/reels/005-same-restaurant/storyboard.md`
   - `content/reels/005-same-restaurant/prompt-grok.md`
6. Сгенерировать полный ролик длительностью 15 секунд.

## Сценарий, который нельзя менять

### 0–4 с
Алиса заканчивает рабочий день в интерьерной дизайн-студии / шоуруме: закрывает ноутбук, складывает материалы / каталог. Телефон вибрирует. Камера двигается вместе с ней, не talking-head.

### 4–9 с
Она берёт телефон, включает голосовое и идёт к окну / стеллажу. Мужской голос за кадром по-русски:

«Мы вчера были в одном ресторане. Я сидел у окна. Видел, как ты ушла.»

Мужчина в кадре НЕ появляется.

### 9–12 с
Алиса останавливается, смотрит на телефон / в окно. Реакция — спокойная настороженность и любопытство. Говорит:

«Так вот откуда.»

### 12–15 с
Алиса записывает голосовой ответ и говорит:

«Тогда вопрос другой. Зачем ты мне написал?»

Обрыв до ответа мужчины.

## Production gate

- 15 секунд;
- strict 9:16;
- **нативный минимум 720×1280**, предпочтительно 1080×1920;
- не апскейл старого 400×736;
- тот же first frame в начале;
- лицо Алисы не менять;
- без второго мужчины в кадре;
- без нового сюжетного факта;
- вся речь только на русском;
- без встроенных субтитров;
- без читаемого AI/UI на телефоне;
- без beauty drift / омоложения;
- руки и пальцы без явных деформаций.

## Доставка результата через Gmail

После успешной генерации скачать MP4 и отправить с `roman12101992@gmail.com` на тот же адрес.

Тема письма строго:

`ALISA-BRIDGE | SAVE_TO=content/reels/005-same-restaurant/output/candidates/reels-005-imagine-v4.mp4 | KIND=video | FROM=grok | SHA256=<реальный_sha256_mp4>`

Тело должно содержать минимум:
- `FROM: grok`
- `TO: chatgpt`
- `KIND: video`
- `SAVE_TO: content/reels/005-same-restaurant/output/candidates/reels-005-imagine-v4.mp4`
- `FILENAME: <реальное имя mp4>`
- `SHA256: <реальный sha256>`
- `RESOLUTION: <реальное разрешение>`
- `DURATION: <реальная длительность>`
- `MIME: video/mp4`
- `DO_NOT_TOUCH: character/references/alice-master-face.jpg`

Не заявлять, что файл доставлен, пока письмо с вложением реально не отправлено.

После отправки письма создай новый immutable handoff Grok → ChatGPT и поставь `next_actor=chatgpt`, чтобы ChatGPT забрал MP4 из Gmail, сверил SHA и провёл QA.

## Важно

Это новый факт по tooling/маршруту: пользователь явно задал production loop **ChatGPT пишет задачу → Grok Imagine → Image-to-Video → Gmail bridge → ChatGPT QA**. Поэтому старый `blocked_tooling_external` Reels 005 не считать основанием для бездействия, пока не проверен именно этот путь в Grok Imagine текущей сессии.
