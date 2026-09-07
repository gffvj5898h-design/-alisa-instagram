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
  - 2026-09-07: guarded repair восстановил exact verified original: 1237×1536, 606787 bytes, SHA-256 `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`, full Pillow decode pass.
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
  - [x] Public evidence verification 2026-09-06: `alisa.vetrova` подтверждённо занят по handoff Grok; `vetrova.life` также занят.
  - Текущий регистрационный кандидат: `alisa.vetrova.spb`.
  - Статус `alisa.vetrova.spb`: публично unresolved; доступность не подтверждена. Не закрывать этот backlog-пункт до фактической успешной регистрации или надёжного availability signal.
- [x] Сделать production-usable квадратный аватар профиля из verified master source
  - `content/profile/avatar-candidate.jpg`
  - 1080×1080, 372608 bytes, SHA-256 `cd13823359565526f6f60e6e2c2e5926aded675e0fc89ecacce38bdc62f25c57`
  - non-generative center-square crop; новое лицо не генерировалось
  - binary import receipt: `production/import-receipts/20260907-avatar-firestorage-v3.md`
  - Avatar QA run `34070246195`: master integrity pass, overall pass, `likely_same_identity`, no warnings/errors
  - final cross-agent Grok visual QA pending before maintenance task closure
- [x] Квадратный crop аватара без смены лица + binary bridge
  - 2026-09-07: source-integrity и binary-transport blockers сняты. Canonical восстановлен exact verified bytes, importer получил hash-locked firestorage share transport, avatar imported and technically QA-passed.
  - `content/profile/result-notes.md` — актуальный отчёт.
- [x] Аудит восстановительных identity sources без смены канона
  - 2026-09-06 Grok: inventory complete. See `production/identity-source-recovery.md`. Sole decodable Alice still с документированной provenance на момент аудита: `content/reels/005-same-restaurant/stills/start-frame.jpg` (1008×1792, SHA-256 `1e2a30eb7e0e55145384e354fb358db850a7e7dfabd74a1444c64359b72c8a87`) — `strong_recovery_candidate`.
  - 2026-09-06 original master source independently recovered and verified by both agents: 1237×1536, 606787 bytes, SHA-256 `d3a64a201e3466eb87a197a897116161578db51aac23e28be927fd2c89109767`, Pillow pass.
  - 2026-09-07 guarded maintenance repair promoted those exact verified bytes back to canonical path; this was integrity restoration, not identity redesign.
- [x] Аудит существующих Reels 001–004 как video recovery sources без смены канона
  - 2026-09-06 Grok: audit complete. See `production/identity-video-recovery.md`. All four MP4s decode OK (512×910, ~15 s, H.264). SHA-256 match result-notes. Documented provenance = master-face identity reference. Classification: `supporting_recovery_evidence` for each.
- [ ] Сгенерировать 7 кадров Post 001 с master face
- [ ] Проверить лицо на каждом кадре
- [x] Подготовить 3 дня Stories
- [x] Оформить bio профиля
- [x] Post 002 — текстовый пакет QA pass 2026-09-05 (`caption.md` + `carousel-plan.md`); визуальные кадры отдельно зависят от identity-reference generator
- [x] Пакет из 10 фоновых Stories — text QA pass 2026-09-06 (`content/stories/background-10-pack.md`)
- [x] Подготовить визуальный пресет / референс света — text QA pass 2026-09-06 (`production/visual-light-preset.md`)
