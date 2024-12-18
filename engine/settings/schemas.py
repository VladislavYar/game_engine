from pathlib import Path

from pydantic import BaseModel, Field, model_validator, field_validator
from screeninfo import get_monitors

from engine.settings.constants import (
    SCREEN_RESOLUTIONS,
    SCREEN_RESOLUTION_MESSAGE_ERROR,
    MAX_LEN_CAPTION_TITLE,
    DEFAULT_NAME_ICON,
    FPSEnum,
)


class ScreenResolutionShema(BaseModel):
    """Схема разрешения экрана."""

    width: int = Field(description='Ширина экрана')
    height: int = Field(description='Высота экрана')

    @model_validator(mode='after')
    @classmethod
    def validate_all_before(cls, values: 'ScreenResolutionShema') -> 'ScreenResolutionShema':
        """Валидация разрешения экрана после валидации полей.

        Args:
            values (ScreenResolutionShema): данные по полям.

        Returns:
            ScreenResolutionShema: отвалидированные данные по полям.
        """
        if (values.width, values.height) in SCREEN_RESOLUTIONS:
            return values
        raise ValueError(SCREEN_RESOLUTION_MESSAGE_ERROR.format(values.width, values.height))


class SettingsSchema(BaseModel):
    """Схема настроек игрового процесса."""

    fullscreen: bool = Field(default=True, description='Флаг полного экрана')
    max_fps: int = Field(
        default=FPSEnum.MAX_FPS, le=FPSEnum.MAX_FPS, ge=FPSEnum.MIN_FPS, description='Максимальная частота кадров'
    )
    screen_resolution: ScreenResolutionShema = Field(
        default_factory=lambda: SettingsSchema.get_default_screen_resolution(),
        description='Разрешение экрана',
    )

    caption_title: str = Field(default='Game', description='Заголовок окна игры', max_length=MAX_LEN_CAPTION_TITLE)
    path_icon: str = Field(
        default_factory=lambda: str(Path(__file__).parent.parent.parent / 'data' / DEFAULT_NAME_ICON),
        alias='name_icon',
        description='Название иконки окна игры',
    )

    @staticmethod
    def get_default_screen_resolution() -> ScreenResolutionShema:
        """Отдаёт дефолтное значение разрешение экрана.

        Returns:
            ScreenResolutionShema: разрешение экрана.
        """
        monitor = get_monitors()[0]
        return ScreenResolutionShema(width=monitor.width, height=monitor.height)

    @field_validator('path_icon', mode='after')
    @classmethod
    def forming_path_icon(cls, value: str) -> str:
        """Фомирование пути до иконки окна игры."""
        return str(Path(__file__).parent.parent.parent / 'data' / value)
