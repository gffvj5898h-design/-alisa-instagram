# Production Backlog

## P0 — технический долг Reels 001–004

- [x] Reels 001 candidate-master лежит в repo
- [x] Reels 002 candidate-master лежит в repo
- [x] Reels 003 candidate-master лежит в repo
- [x] Reels 004 candidate-master лежит в repo
- [x] SHA-256 001–004 зафиксированы и сверены Grok-аудитом
- [x] Восстановить пакет `concept.md`, `prompt-grok.md`, `storyboard.md`, `result-notes.md` для Reels 003
- [x] Восстановить пакет `concept.md`, `prompt-grok.md`, `storyboard.md`, `result-notes.md` для Reels 004
- [x] Синхронизировать канон лица на `character/references/alice-master-face.jpg`
- [x] Обновить `result-notes.md` Reels 001–004 после Grok-аудита
- [x] Перевести реестр 001–004 в QA hold до выполнения production gate
- [ ] Пересобрать / перегенерировать Reels 001 в нативном 9:16 минимум 720×1280
- [ ] Пересобрать / перегенерировать Reels 002 в нативном 9:16 минимум 720×1280
- [ ] Пересобрать / перегенерировать Reels 003 в нативном 9:16 минимум 720×1280
- [ ] Пересобрать / перегенерировать Reels 004 в нативном 9:16 минимум 720×1280
- [ ] Повторный Grok QA по новым 720p+ masters
- [ ] Только после QA перевести соответствующие ролики в production-approved

Примечание 2026-08-22: задачи регенерации 001–004 временно зависят от того же внешнего 720p+ I2V blocker, что и Reels 005. Пока blocker не изменился, не тратить циклы на повтор одной и той же технической ошибки.

## P1 — Reels 005

- [x] Подготовить `content/reels/005-same-restaurant/concept.md`
- [x] Подготовить `content/reels/005-same-restaurant/prompt-grok.md`
- [x] Подготовить `content/reels/005-same-restaurant/storyboard.md`
- [x] Подготовить `content/reels/005-same-restaurant/result-notes.md`
- [x] Создать и залить стартовый кадр Reels 005 только с `alice-master-face.jpg` как identity reference
- [x] Провести Grok QA стартового кадра Reels 005 из repo
- [x] I2V attempt 1 получен и проверен: 15.041667 с, 400×736 — rejected, ниже production gate
- [ ] Перегенерировать Reels 005 от того же принятого start-frame: 15 с, strict 9:16, минимум 720×1280, предпочтительно 1080×1920
  - blocked_tooling_external 2026-08-22: Grok не имеет 720p+ I2V; ChatGPT проверил Runway (`availableVideoModels=[]`), OpenArt Seedance 2.5 и Grok Imagine 1.5 (`insufficient_balance`), Magnific (`403 Forbidden`); новый first frame не создавался.
- [ ] Провести Grok QA нового Reels 005
- [ ] После успешного QA обновить production registry

## P2 — запуск аккаунта

- [ ] Утвердить username Instagram
  - editorial-кандидат после QA 2026-09-05: `alisa.vetrova`; запасной `alisa.vetrova.spb`; доступность/регистрация в Instagram пока не подтверждены.
- [x] Сделать аватар профиля из master face — identity-safe fallback
  - `content/profile/avatar-candidate.jpg` = exact copy of `alice-master-face.jpg`
  - 320×400, 15008 bytes, SHA-256 `2d5347eb3831fcf5f01804fa6c4f5fd261f72473bfede75beed29255801b5ef2`
  - Grok QA 2026-08-22: identity pass; dense 1:1 / 1080 crop hold
  - notes: `content/profile/result-notes.md`
- [ ] Опционально: квадратный crop аватара без смены лица, когда есть binary bridge
- [ ] Сгенерировать 7 кадров Post 001 с master face
- [ ] Проверить лицо на каждом кадре
- [x] Подготовить 3 дня Stories
- [x] Оформить bio профиля
- [x] Post 002 — текстовый пакет QA pass 2026-09-05 (`caption.md` + `carousel-plan.md`); визуальные кадры отдельно зависят от identity-reference generator
- [x] Пакет из 10 фоновых Stories — text QA pass 2026-09-06 (`content/stories/background-10-pack.md`)
- [ ] Подготовить визуальный пресет / референс света
