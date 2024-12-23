import os
import json
from pathlib import Path

from engine.settings.types import TYPES_SETTINGS, SETTINGS_SCHEMAS
from engine.settings.schemas import AllSettingsSchema
from engine.settings.constants import SettingsFilesPathEnum, ENCODING


class Settings:
    """Класс настроек игрового процесса."""

    def __init__(self) -> None:
        """Инициализация настроек."""
        self._settings = self._get_settings()

    def _check_existence_settings_file(self, path: Path) -> None:
        """Проверяет наличие файла настроек и пути до него.

        Args:
            path (Path): путь до файла настроек.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        path.touch(exist_ok=True)

    def _read_settings(self, path: Path) -> dict[str, TYPES_SETTINGS]:
        """Загружает файл с настройками.

        Args:
            path (Path): путь до файла настроек.

        Returns:
            dict[str, TYPES_SETTINGS]: настройки игрового процесса.
        """
        with open(path, 'r', encoding=ENCODING) as file_settings:
            try:
                settings = json.load(file_settings)
                if isinstance(settings, dict):
                    return settings
                raise ValueError()
            except Exception:
                return {}

    def _get_settings(self) -> AllSettingsSchema:
        """Отдаёт настройки игрового процесса.

        Returns:
            AllSettingsSchema: настройки игрового процесса.
        """
        settings = {}
        for path in SettingsFilesPathEnum:
            self._check_existence_settings_file(path.value)
            settings[path.name.lower()] = self._read_settings(path.value)
        return AllSettingsSchema(**settings)

    def __getitem__(self, key: str) -> SETTINGS_SCHEMAS:
        """Отдаёт группу настроек по ключу.

        Args:
            key (str): ключ группы настроек.

        Returns:
            SETTINGS_SCHEMAS: группа настроек.
        """
        return getattr(self._settings, key)
