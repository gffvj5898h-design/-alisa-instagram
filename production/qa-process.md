# QA ChatGPT — процесс Grok

Grok не принимает статус ChatGPT «approved» как истину без проверки репозитория.

## Когда проводить

- после каждого «согласован» от ChatGPT;
- перед стартом нового Reels;
- если разъехались канон, платье или сюжет.

## Что проверять

1. Канон: `character/references/alice-master-face.jpg` на месте.
2. `GROK_CONTEXT_AND_LOG.md` и `character/visual-rules.md` не противоречат друг другу.
3. У согласованного Reels есть:
   - `concept.md`
   - `prompt-grok.md`
   - `storyboard.md`
   - `result-notes.md`
   - `output/approved/reels-NNN-approved.mp4`
4. SHA-256 и техпараметры MP4 сходятся с `production/approved-reels.md`.
5. Цель: 9:16, ~15 с, не ниже 720p.
6. После проверки — запись сверху в журнал `GROK_CONTEXT_AND_LOG.md`.

Скрипт: `production/qa-repo.sh`
