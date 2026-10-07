"""Контракт компонента аутентификации версии v0.4.

Проверка учетных данных еще не реализована. Архитектурно модуль должен
создавать контекст только после успешной проверки личности пользователя.
"""

from dataclasses import dataclass

from app.security.access_control import Role


@dataclass(frozen=True)
class AuthenticatedPrincipal:
    """Минимальный контекст уже аутентифицированного пользователя."""

    username: str
    role: Role
