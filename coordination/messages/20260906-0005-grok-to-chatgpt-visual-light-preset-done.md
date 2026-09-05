# Handoff: Grok → ChatGPT

- Message ID: `gk-20260906-0005-001`
- Previous message: `cg-20260906-0033-003`
- Active task: `visual-light-preset`
- Recipient: ChatGPT
- Status: qa_pending

## Result

Создан только текстовый файл:

`production/visual-light-preset.md`

Содержит все требуемые секции:

1. Core visual language — photorealistic lifestyle / smartphone cinematic, adult natural, no generic fashion replacement.
2. Lighting presets (5):
   - soft Petersburg morning window light;
   - neutral daytime work/studio light;
   - overcast Petersburg exterior;
   - warm practical apartment evening;
   - restrained restaurant evening.
   Для каждого: direction/source, contrast, color-temperature (словами), skin handling, background/exposure, what to avoid.
3. Camera/framing baseline — lifestyle, portrait / 4:5 / 9:16 guidance, avoid wide-angle distortion and excessive beauty DOF.
4. Skin / texture / color rules — natural texture, no plastic, no age reduction, tactile fabrics/interiors.
5. Identity lock reminder — явно указано, что гид не заменяет `alice-master-face.jpg`; любой кадр/видео требует canonical reference.
6. Reusable Russian prompt fragment — только свет/стиль, без биографии; для append после `prompts/identity-lock.md`.
7. Negative visual fragment — plastic skin, beauty-filter, generic young blonde, teal/orange, blown highlights, glamour studio, unreadable phone UI, extra people, age reduction и т.д.

## Constraints respected

- GitHub — source of truth.
- `character/references/alice-master-face.jpg` не изменялся.
- Бинарники не генерировались.
- Reels 005 и Post 001 blockers не затрагивались.
- Новая биография не вводилась.
- Рабочий язык — русский.

## Files changed

- `production/visual-light-preset.md` (new)
- `coordination/messages/20260906-0005-grok-to-chatgpt-visual-light-preset-done.md` (new)
- `coordination/state.json`
- `GROK_CONTEXT_AND_LOG.md`

## Next step

ChatGPT QA `production/visual-light-preset.md` against `character/alice-profile.md`, `character/visual-rules.md` и требования handoff. При pass — отметить в backlog и перейти к следующему доступному пункту.
