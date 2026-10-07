"""Ролевая модель и серверная проверка разрешений."""

from enum import Enum


class Role(str, Enum):
    """Роли приложения."""

    APPLICANT = "applicant"
    SECURITY_OFFICER = "security_officer"
    ADMIN = "admin"


class Permission(str, Enum):
    """Разрешения, необходимые архитектуре версии v0.4."""

    CREATE_APPLICATION = "create_application"
    VIEW_OWN_APPLICATION = "view_own_application"
    REVIEW_APPLICATION = "review_application"
    DECIDE_APPLICATION = "decide_application"
    ISSUE_PASS = "issue_pass"
    CHANGE_PASS_STATUS = "change_pass_status"
    MANAGE_ACCOUNTS = "manage_accounts"
    VIEW_AUDIT_LOG = "view_audit_log"
    MANAGE_CONFIGURATION = "manage_configuration"


ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    Role.APPLICANT.value: frozenset(
        {
            Permission.CREATE_APPLICATION,
            Permission.VIEW_OWN_APPLICATION,
        }
    ),
    Role.SECURITY_OFFICER.value: frozenset(
        {
            Permission.REVIEW_APPLICATION,
            Permission.DECIDE_APPLICATION,
            Permission.ISSUE_PASS,
            Permission.CHANGE_PASS_STATUS,
        }
    ),
    Role.ADMIN.value: frozenset(
        {
            Permission.MANAGE_ACCOUNTS,
            Permission.VIEW_AUDIT_LOG,
            Permission.MANAGE_CONFIGURATION,
        }
    ),
}


def has_permission(
    role: Role | str,
    permission: Permission,
) -> bool:
    """Проверить разрешение. Неизвестная роль получает пустой набор прав."""

    role_value = role.value if isinstance(role, Role) else str(role).strip().lower()
    permissions = ROLE_PERMISSIONS.get(role_value, frozenset())
    return permission in permissions


def require_permission(
    role: Role | str,
    permission: Permission,
) -> None:
    """Отклонить операцию при отсутствии разрешения."""

    if not has_permission(role, permission):
        raise PermissionError("Недостаточно прав")
