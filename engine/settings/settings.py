import os
import json
from pathlib import Path

from pydantic import BaseModel

from engine.settings.types import TYPES_SETTINGS
from engine.settings.schemas import SettingsSchema


class Settings:
    """Класс настроек игрового процесса."""

    def __init__(self) -> None:
        """Инициализация настроек."""
        self.settings = SettingsSchema(**self._read_settings())

    def _get_path_settings(self) -> Path:
        """Отдаёт путь до файла настроек.

        Returns:
            Path: путь до файла настроек.
        """
        return Path(__file__).parent.parent.parent / 'data' / 'settings.json'

    def _check_existence_settings_file(self, path: Path) -> None:
        """Проверяет наличие файла настроек и пути до него.

        Args:
            path (Path): путь до файла настроек.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        path.touch(exist_ok=True)

    def _read_settings(self) -> dict[str, TYPES_SETTINGS]:
        """Загрузка настроек из файла.

        Returns:
            dict[str, TYPES_SETTINGS]: настройки игрового процесса.
        """
        path = self._get_path_settings()
        self._check_existence_settings_file(path)
        with open(path, 'r') as file_settings:
            try:
                settings = json.load(file_settings)
                if isinstance(settings, dict):
                    return settings
                raise ValueError()
            except Exception:
                return {}

    def __getitem__(self, key: str) -> TYPES_SETTINGS:
        """Отдаёт настройку по ключу.

        Args:
            key (str): ключ настройки.

        Returns:
            TYPES_SETTINGS: настройка.
        """
        value = getattr(self.settings, key)
        if isinstance(value, BaseModel):
            return tuple(value.model_dump().values())
        return value

    def __setitem__(self, key: str, value: TYPES_SETTINGS) -> None:
        """Устанавливает настройку по ключу.

        Args:
            key (str): ключ настройки.
            value (TYPES_SETTINGS): значение настройки.
        """
        setattr(self.settings, key, value)
