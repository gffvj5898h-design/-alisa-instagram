# QA аватара Instagram

Автоматический контроль: `production/validate_avatar.py`.

Ключевое правило: сначала полностью декодируется canonical master, и только после успешной проверки его целостности выполняется identity comparison. Побитовое совпадение с повреждённым JPEG больше не может дать `warn/pass`.

Проверяется:

- расширение и сигнатура;
- для JPEG обязательный EOI marker;
- `Pillow.verify()` и полный `load()` для master и candidate;
- SHA-256, размеры и минимальная сторона;
- квадратность / предпочтительные 1080×1080;
- exact valid master fallback или aHash/MAE для производного crop.

`fail` всегда валит CI. `--strict` также превращает предупреждения в failure.

Визуальная identity QA другого агента по-прежнему нужна для любого не-pixel-identical производного изображения.
