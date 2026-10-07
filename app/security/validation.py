"""Проверка недоверенных текстовых данных."""


def validate_text(
    value: str,
    min_length: int = 2,
    max_length: int = 100,
) -> str:
    """Нормализовать и проверить текстовое значение."""

    if not isinstance(value, str):
        raise ValueError("Ожидается текстовое значение")
    if min_length < 0 or max_length < min_length:
        raise ValueError("Некорректные ограничения длины")

    normalized = value.strip()

    if len(normalized) < min_length:
        raise ValueError("Значение слишком короткое")
    if len(normalized) > max_length:
        raise ValueError("Значение слишком длинное")

    return normalized
