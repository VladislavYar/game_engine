from pydantic import BaseModel, Field, model_validator, field_validator
from screeninfo import get_monitors

from engine.settings.constants import (
    SCREEN_RESOLUTIONS,
    SCREEN_RESOLUTION_MESSAGE_ERROR,
    MAX_LEN_CAPTION_TITLE,
    DEFAULT_NAME_ICON,
    BaseScreenSizeFrameEnum,
    TimeBetweenAnimationFrames,
    VolumeEnum,
    FPSEnum,
)
from engine.settings.types import TYPES_SETTINGS
from engine.constants.path import BasePathEnum


class BaseSettingsSchema(BaseModel):
    """Базовая схема настроек."""

    def __getitem__(self, key: str) -> TYPES_SETTINGS:
        """Отдаёт настройку по ключу.

        Args:
            key (str): ключ настройки.

        Returns:
            TYPES_SETTINGS: настройка.
        """
        value = getattr(self, key)
        if isinstance(value, BaseModel):
            return tuple(value.model_dump().values())
        return value

    def __setitem__(self, key: str, value: TYPES_SETTINGS) -> None:
        """Устанавливает настройку по ключу.

        Args:
            key (str): ключ настройки.
            value (TYPES_SETTINGS): значение настройки.
        """
        setattr(self, key, value)


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


class GraphicsSettingsSchema(BaseSettingsSchema):
    """Схема настроек графики."""

    screen_resolution: ScreenResolutionShema = Field(
        default_factory=lambda: GraphicsSettingsSchema.get_default_screen_resolution(),
        description='Разрешение экрана',
    )
    fullscreen: bool = Field(default=True, description='Флаг полного экрана')
    max_fps: int = Field(
        default=FPSEnum.MAX_FPS, le=FPSEnum.MAX_FPS, ge=FPSEnum.MIN_FPS, description='Максимальная частота кадров'
    )

    @staticmethod
    def get_default_screen_resolution() -> ScreenResolutionShema:
        """Отдаёт дефолтное значение разрешение экрана.

        Returns:
            ScreenResolutionShema: разрешение экрана.
        """
        monitor = get_monitors()[0]
        return ScreenResolutionShema(width=monitor.width, height=monitor.height)


class AudioSettingsSchema(BaseSettingsSchema):
    """Схема настроек звука."""

    music_volume: float = Field(
        default=VolumeEnum.DEFAULT_VOLUME.value,
        ge=VolumeEnum.MIN_VOLUME.value,
        le=VolumeEnum.MAX_VOLUME.value,
        description='Громкость музыки',
    )
    effects_volume: float = Field(
        default=VolumeEnum.DEFAULT_VOLUME.value,
        ge=VolumeEnum.MIN_VOLUME.value,
        le=VolumeEnum.MAX_VOLUME.value,
        description='Громкость эффектов',
    )
    voices_volume: float = Field(
        default=VolumeEnum.DEFAULT_VOLUME.value,
        ge=VolumeEnum.MIN_VOLUME.value,
        le=VolumeEnum.MAX_VOLUME.value,
        description='Громкость голоса',
    )


class EngineSettingsSchema(BaseSettingsSchema):
    """Схема настроек движка."""

    caption_title: str = Field(default='Game', description='Заголовок окна игры', max_length=MAX_LEN_CAPTION_TITLE)
    path_icon: str = Field(
        default_factory=lambda: str(BasePathEnum.ICONS_PATH.value / DEFAULT_NAME_ICON),
        alias='name_icon',
        description='Название иконки окна игры',
    )
    time_between_animation_frames: int = Field(
        default=TimeBetweenAnimationFrames.DEFAULT_TIME,
        ge=TimeBetweenAnimationFrames.MIN_TIME,
        le=TimeBetweenAnimationFrames.MAX_TIME,
        description='Время между кадрами анимаций',
    )
    base_screen_size_frame: ScreenResolutionShema = Field(
        default_factory=lambda: EngineSettingsSchema.get_base_screen_size_frame(),
        description='Базовое разрешение экрана расчёта размера фрейма',
    )

    @staticmethod
    def get_base_screen_size_frame() -> ScreenResolutionShema:
        """Отдаёт базовое значение разрешения экрана расчёта размера фрейма.

        Returns:
            ScreenResolutionShema: разрешение экрана.
        """
        return ScreenResolutionShema(width=BaseScreenSizeFrameEnum.WIDTH, height=BaseScreenSizeFrameEnum.HEIGHT)

    @field_validator('path_icon', mode='after')
    @classmethod
    def forming_path_icon(cls, value: str) -> str:
        """Фомирование путь до иконки окна игры."""
        return str(BasePathEnum.ICONS_PATH.value / value)


class AllSettingsSchema(BaseModel):
    """Схема всех настроек."""

    audio: AudioSettingsSchema = Field(description='Настройки звука')
    graphics: GraphicsSettingsSchema = Field(description='Настройки графики')
    engine: EngineSettingsSchema = Field(description='Настройки движка')
