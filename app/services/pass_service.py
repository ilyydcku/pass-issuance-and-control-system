"""Минимальный прототип сервисного уровня для операций с пропусками."""

from pathlib import Path

from app.audit.audit_logger import log_security_event
from app.security.access_control import Permission, Role, has_permission
from app.security.validation import validate_text


def change_pass_status(
    user: str,
    role: Role | str,
    pass_id: str,
    new_status: str,
    *,
    log_path: str | Path = "security.log",
) -> dict[str, str]:
    """Проверить входные данные и полномочия перед изменением состояния."""

    checked_user = validate_text(user, min_length=1, max_length=64)
    checked_pass_id = validate_text(pass_id, min_length=1, max_length=64)
    checked_status = validate_text(new_status, min_length=2, max_length=32)

    if not has_permission(role, Permission.CHANGE_PASS_STATUS):
        log_security_event(
            checked_user,
            "change_pass_status",
            "access_denied",
            object_id=checked_pass_id,
            log_path=log_path,
        )
        raise PermissionError("Недостаточно прав")

    log_security_event(
        checked_user,
        "change_pass_status",
        "success",
        object_id=checked_pass_id,
        new_state=checked_status,
        log_path=log_path,
    )

    return {
        "pass_id": checked_pass_id,
        "status": checked_status,
    }
