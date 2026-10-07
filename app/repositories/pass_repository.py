"""Контракт слоя доступа к данным о пропусках."""

from typing import Protocol


class PassRepository(Protocol):
    """Интерфейс будущего хранилища пропусков."""

    def has_pass_for_application(self, application_id: str) -> bool:
        """Проверить наличие пропуска для заявки."""

    def create_pass(self, application_id: str) -> str:
        """Создать пропуск для допустимой заявки."""

    def change_status(self, pass_id: str, new_status: str) -> None:
        """Изменить состояние существующего пропуска."""
