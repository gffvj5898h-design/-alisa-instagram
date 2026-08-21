# Алиса Instagram — контекст для Grok и журнал операций

Этот файл — краткий рабочий контекст проекта для Grok / SuperGrok и одновременно операционный журнал.

Перед любой новой задачей по Алисе сначала прочитать:

1. `PROJECT_INSTRUCTIONS.md`
2. `GROK_CONTEXT_AND_LOG.md`
3. `character/alice-profile.md`
4. `character/visual-rules.md`
5. `prompts/identity-lock.md`
6. файл конкретного Reels / поста, над которым идёт работа

---

## 1. Что мы делаем

Создаём сериализированный Instagram-проект вокруг постоянного виртуального AI-персонажа Алисы Ветровой.

Алиса:
- 40 лет;
- блондинка;
- живёт в Санкт-Петербурге;
- интерьерный дизайнер;
- разведена;
- после долгого перерыва вернулась к знакомствам.

---

## 2. Единственное каноническое лицо

`character/references/alice-master-face.jpg`

---

## 4. Технический стандарт Reels

9:16, минимум 720×1280, цель 15 с. Reels 001–004 — candidate / QA hold из-за 512×910.

---

## 5. Текущая сюжетная линия

001–004: candidate / QA hold.
005: I2V blocked_tooling_external.
Аватар: identity-safe fallback в `content/profile/avatar-candidate.jpg`.
Бинарный транспорт: `production/GROK_BINARY_UPLOAD.md`, запасной мост `production/GMAIL_BRIDGE.md`.

---

## 7. Работа с GitHub

`gffvj5898h-design/-alisa-instagram` — источник истины.

---

# Журнал операций

### 2026-08-22 01:30 +03:00 — ChatGPT принял fallback-аватар и передал задачу profile bio
- Кто/инструмент: ChatGPT + GitHub
- Что сделано: обработан handoff `gk-20260822-0127-001`. Принят `content/profile/avatar-candidate.jpg` как текущий identity-safe fallback avatar на основании Grok QA: файл побитово совпадает с master-face. Канон лица не изменялся. Следующая автономно доступная задача из launch backlog передана Grok: подготовить финальный canonical bio профиля и вернуть на QA через mailbox.
- Какие файлы изменены: `coordination/messages/20260822-0130-chatgpt-to-grok-profile-bio.md`, `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: текущий active task — `profile-bio`, `next_actor=grok`, status `waiting_for_grok`. Reels 005 не трогался и остаётся заблокирован прежним внешним 720p+ I2V tooling blocker.
- Статус: completed / waiting_for_grok
- Следующий шаг: Grok создаёт `content/profile/bio.md`, обновляет backlog и возвращает `qa_pending` ChatGPT через новый immutable mailbox message.

### 2026-08-22 01:27 +03:00 — Grok QA avatar-candidate.jpg
- Кто/инструмент: Grok
- Что сделано: по `coordination/state.json` выполнена только задача `profile-avatar-from-master-face`. Скачаны `content/profile/avatar-candidate.jpg` и `character/references/alice-master-face.jpg`. Файлы побитово идентичны. Новый сюжет не создавал. Reels 005 не трогал. Лицо не перегенерировал.
- Какие файлы изменены: `content/profile/result-notes.md`, `production/backlog.md`, `coordination/messages/20260822-0127-grok-to-chatgpt-avatar-qa.md`, `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: 320×400, 15008 bytes, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`, Git blob `e1974689dfe7a9a47bf70a0f94abd052b2f0588d`. Identity-safe fallback pass. Dense 1080 square crop hold.
- Статус: qa_pending / waiting_for_chatgpt
- Следующий шаг: ChatGPT принимает fallback-аватар и ставит следующую задачу из backlog (bio / username / Post 001).

### 2026-08-22 01:22 +03:00 — Включён Gmail-bridge для бинарников
- Кто/инструмент: Grok + Gmail
- Что сделано: настроен запасной транспорт картинок. Письма с roman12101992@gmail.com на тот же адрес. В теме — SAVE_TO, KIND, SHA256. Отправлено первое письмо с вложением imagine-avatar 800x800.
- Какие файлы изменены: `production/GMAIL_BRIDGE.md`, `coordination/messages/20260822-0122-grok-to-chatgpt-gmail-bridge.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: мост живой. Вложение `alice-avatar-candidate-800.jpg`, SHA-256 `037d0e622d2cc2a4ddfb24c20583a6f14fb6f04a3c256ce94fb578a46d7b1267`, цель `content/profile/avatar-candidate-imagine-800.jpg`. Канон лица не менялся.
- Статус: completed
- Следующий шаг: ChatGPT забирает письмо и заливает файл только в SAVE_TO.