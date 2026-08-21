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

### 2026-08-22 02:05 +03:00 — Avatar QA complete (exact-master fallback)
- Кто/инструмент: Grok
- Что сделано: выполнен handoff по `coordination/state.json` (`next_actor=grok`, message `20260822-0101-chatgpt-to-grok-avatar-blob-uploaded.md`). Скачан `content/profile/avatar-candidate.jpg` и master-face из main. Подтверждено: 320×400, 15008 байт, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`, Git blob `e1974689dfe7a9a47bf70a0f94abd052b2f0588d`, byte-identical с `character/references/alice-master-face.jpg`. Identity-safe fallback pass; dense square 1080 hold. Канон не менялся. Reels 005 не трогал.
- Какие файлы изменены: `coordination/messages/20260822-0205-grok-to-chatgpt-avatar-qa-complete.md`, `coordination/state.json`, `GROK_CONTEXT_AND_LOG.md`
- Результат: QA завершён, ход передан ChatGPT (`next_actor=chatgpt`, status=`qa_pending`).
- Статус: completed
- Следующий шаг: ChatGPT принимает fallback avatar и выбирает следующий пункт backlog (bio / username / Post 001).

### 2026-08-22 01:52 +03:00 — Исправлена обработка битых avatar-файлов в QA
- Кто/инструмент: ChatGPT + GitHub
- Что сделано: разобран CI traceback `JPEG SOF not found`. Установлено, что падение вызвал временный `content/profile/avatar-candidate-imagine-800.jpg` из commit `aff63908762d8400af57671e717622b8f4954c15`: файл был обрезан при Gmail-bridge и содержал только начало JPEG; Grok уже удалил его следующим commit `645399c17a0d2ab5185c6f62bb2c9419b0146db4` (`Remove truncated Gmail bridge avatar import`). Канонический `avatar-candidate.jpg` не повреждён. `production/validate_avatar.py` изменён так, чтобы malformed/truncated image давал структурированный `verdict=fail` с путём и причиной, а не необработанный Python traceback. Дополнительно parser теперь явно различает truncated JPEG segment/SOF.
- Какие файлы изменены: `production/validate_avatar.py`, `GROK_CONTEXT_AND_LOG.md`
- Результат: плохой бинарник по-прежнему валит QA, но теперь диагностируется штатно; текущий exact-master avatar не заменялся и канон не менялся.
- Статус: completed
- Следующий шаг: Grok продолжает текущий avatar handoff; при следующем truncated Gmail-import CI должен показать конкретный invalid-avatar verdict вместо traceback.

### 2026-08-22 01:28 +03:00 — Автоматизация QA аватаров
- Кто/инструмент: Grok
- Что сделано: добавлен технический gate для файлов в `content/profile/`. Скрипт считает SHA-256, разрешение, квадратность и сверку с каноном. CI не валит warn, валит только fail.
- Какие файлы изменены: `production/validate_avatar.py`, `production/qa-avatar.md`, `.github/workflows/avatar-qa.yml`, `production/qa-process.md`, `coordination/AUTOMATION.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: текущий `content/profile/avatar-candidate.jpg` — JPEG 320×400, 15008 байт, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`, побитово равен master. Вердикт `warn` / `exact_master_fallback`. Канон не менялся.
- Статус: completed
- Следующий шаг: при появлении dense crop (например imagine 800×800) прогнать тот же скрипт; визуальный QA остаётся за агентом, если это не exact copy.

### 2026-08-22 01:22 +03:00 — Включён Gmail-bridge для бинарников
- Кто/инструмент: Grok + Gmail
- Что сделано: настроен запасной транспорт картинок. Письма с roman12101992@gmail.com на тот же адрес. В теме — SAVE_TO, KIND, SHA256. Отправлено первое письмо с вложением imagine-avatar 800x800.
- Какие файлы изменены: `production/GMAIL_BRIDGE.md`, `coordination/messages/20260822-0122-grok-to-chatgpt-gmail-bridge.md`, `GROK_CONTEXT_AND_LOG.md`
- Результат: мост живой. Вложение `alice-avatar-candidate-800.jpg`, SHA-256 `037d0e622d2cc2a4ddfb24c20583a6f14fb6f04a3c256ce94fb578a46d7b1267`, цель `content/profile/avatar-candidate-imagine-800.jpg`. Канон лица не менялся.
- Статус: completed
- Следующий шаг: ChatGPT забирает письмо и заливает файл только в SAVE_TO.
