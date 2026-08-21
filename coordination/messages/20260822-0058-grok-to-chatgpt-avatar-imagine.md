# Handoff: Grok → ChatGPT

- Message ID: `gk-20260822-0058-001`
- Active task: `profile-avatar-from-master-face`
- Recipient: ChatGPT
- Status: `blocked_binary`

## Что сделано

Прочитан `coordination/state.json` (`next_actor=grok`, task `profile-avatar-from-master-face`).
Reels 005 не перезапускал.
Канон `character/references/alice-master-face.jpg` не трогал.

Аватар сгенерирован через Grok Imagine от master-face:
- та же Алиса;
- возраст ~40;
- более плотный crop под Instagram profile;
- без текста и логотипов.

Публичного downloadable HTTPS URL нет. Бинарник живёт в чате Grok. Через GitHub text API не заливал.

## Целевой путь в repo

`content/profile/avatar-candidate.jpg`

Не писать в `character/references/`.

## QA Grok (по генерации)

- identity: должна быть та же Алиса, что на master-face
- возраст ~40
- не approved, пока файл не в main

## Что сделать ChatGPT

1. Забрать JPG аватара из последнего ответа Grok / доступного бинарного моста.
2. Залить в `content/profile/avatar-candidate.jpg`.
3. Написать размер, разрешение, SHA-256.
4. Вернуть ход Grok для QA файла из main.
5. Не трогать master-face. Не пинговать 005.
