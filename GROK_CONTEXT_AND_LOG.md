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

Контент — последовательный сериал с узнаваемой героиней и сильным визуальным флиртом.

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
Бинарный транспорт: `production/GROK_BINARY_UPLOAD.md`, запасной мост `production/GMAIL_BRIDGE.md`.

---

## 7. Работа с GitHub

`gffvj5898h-design/-alisa-instagram` — источник истины.
Бинарники: GitHub import-queue или Gmail-bridge.

---

# Журнал операций

### 2026-08-22 01:22 +03:00 — Включён Gmail-bridge для бинарников
- Кто/инструмент: Grok + Gmail
- Что сделано: настроен запасной транспорт картинок. Письма с roman12101992@gmail.com на тот же адрес. В теме — SAVE_TO, KIND, SHA256. Отправлено первое письмо с вложением imagine-avatar 800x800.
- Какие файлы изменены: `production/GMAIL_BRIDGE.md`, `coordination/messages/20260822-0122-grok-to-chatgpt-gmail-bridge.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: мост живой. Вложение `alice-avatar-candidate-800.jpg`, SHA-256 `037d0e622d2cc2a4ddfb24c20583a6f14fb6f04a3c256ce94fb578a46d7b1267`, цель `content/profile/avatar-candidate-imagine-800.jpg`. Канон лица не менялся.
- Статус: completed
- Следующий шаг: ChatGPT забирает письмо и заливает файл только в SAVE_TO.
