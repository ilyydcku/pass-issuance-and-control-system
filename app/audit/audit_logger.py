"""Журналирование событий безопасности без записи секретных значений."""

import logging
from pathlib import Path


def _safe_field(value: str) -> str:
    """Исключить переносы строк из полей события."""

    return str(value).replace("\r", " ").replace("\n", " ").strip()


def log_security_event(
    user: str,
    action: str,
    result: str,
    *,
    object_id: str | None = None,
    old_state: str | None = None,
    new_state: str | None = None,
    log_path: str | Path = "security.log",
) -> None:
    """Записать минимальное событие безопасности в указанный журнал."""

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(f"pass_control.audit.{path.resolve()}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(handler)

    parts = [
        f"user={_safe_field(user)}",
        f"action={_safe_field(action)}",
        f"result={_safe_field(result)}",
    ]
    if object_id is not None:
        parts.append(f"object_id={_safe_field(object_id)}")
    if old_state is not None:
        parts.append(f"old_state={_safe_field(old_state)}")
    if new_state is not None:
        parts.append(f"new_state={_safe_field(new_state)}")

    try:
        logger.info(" ".join(parts))
        handler.flush()
    finally:
        logger.removeHandler(handler)
        handler.close()
