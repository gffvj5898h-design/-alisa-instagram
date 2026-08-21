# QA аватара Instagram

Автоматический технический контроль: `production/validate_avatar.py`.

Запуск:

```bash
python3 production/validate_avatar.py
python3 production/validate_avatar.py --json
python3 production/validate_avatar.py --strict
```

По умолчанию проверяются все изображения в `content/profile/`.
Канон всегда `character/references/alice-master-face.jpg`.

## Что проверяется автоматически

| Проверка | Порог | Эффект |
| --- | --- | --- |
| Файл существует, JPEG/PNG/WEBP | сигнатура | fail |
| Размер файла | 2 KB … 8 MB | fail |
| Минимальная сторона | ≥ 320 px | fail |
| Предпочтительная сторона | ≥ 1080 px | warn |
| Квадрат | \|w−h\| / max ≤ 8% | warn |
| Совпадение с master | SHA-256 | `exact_master_fallback` + warn |
| Расхождение с master | aHash / MAE центрального квадрата | warn или fail |

Instagram режет аватар кругом из центра. Неквадратный кадр 320×400 технически проходит, но обрежет верх/низ.

## Чего скрипт не делает

Не заменяет визуальный QA Grok, если candidate — не побитовая копия канона:

- возраст ~40;
- форма лица, глаза, нос, губы;
- отсутствие beauty-filter / чужого лица;
- плотность кропа (плечи vs лицо).

## CI

`.github/workflows/avatar-qa.yml` гоняет скрипт на изменения `content/profile/**` и канона.

- `fail` валит workflow;
- `warn` не валит (текущий exact-master fallback остаётся видимым);
- `--strict` можно включить вручную, когда нужен квадрат 1080.

## Вердикты

- `pass` — квадрат ≥1080 и тот же identity, не byte-copy fallback.
- `warn` — можно ставить в профиль, но это fallback или слабый кроп.
- `fail` — не использовать как аватар.
