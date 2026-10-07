"""Тесты защитных механизмов архитектуры v0.4."""

from pathlib import Path

import pytest

from app.audit.audit_logger import log_security_event
from app.security.access_control import Permission, Role, has_permission
from app.security.validation import validate_text
from app.services.pass_service import change_pass_status


def test_valid_text_is_accepted() -> None:
    """Корректные данные проходят проверку."""

    assert validate_text("  PASS-101  ", min_length=1) == "PASS-101"


def test_invalid_text_is_rejected() -> None:
    """Пустое значение отклоняется."""

    with pytest.raises(ValueError):
        validate_text("   ")


def test_applicant_has_insufficient_permission() -> None:
    """Заявитель не получает право менять состояние пропуска."""

    assert not has_permission(
        Role.APPLICANT,
        Permission.CHANGE_PASS_STATUS,
    )


def test_denied_operation_is_written_to_audit(tmp_path: Path) -> None:
    """Запрещенная операция фиксируется в журнале безопасности."""

    log_path = tmp_path / "security.log"

    with pytest.raises(PermissionError):
        change_pass_status(
            user="applicant_test",
            role=Role.APPLICANT,
            pass_id="PASS-201",
            new_status="suspended",
            log_path=log_path,
        )

    content = log_path.read_text(encoding="utf-8")
    assert "action=change_pass_status" in content
    assert "result=access_denied" in content
    assert "object_id=PASS-201" in content


def test_unknown_role_is_fail_secure() -> None:
    """Неизвестная роль получает пустой набор разрешений."""

    assert not has_permission(
        "unknown",
        Permission.MANAGE_ACCOUNTS,
    )


def test_audit_can_record_state_transition(tmp_path: Path) -> None:
    """Критичное изменение может содержать прежнее и новое состояние."""

    log_path = tmp_path / "security.log"

    log_security_event(
        user="security_test",
        action="change_pass_status",
        result="success",
        object_id="PASS-301",
        old_state="active",
        new_state="suspended",
        log_path=log_path,
    )

    content = log_path.read_text(encoding="utf-8")
    assert "old_state=active" in content
    assert "new_state=suspended" in content
