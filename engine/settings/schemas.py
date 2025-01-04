from pydantic import BaseModel, Field, model_validator, field_validator
from screeninfo import get_monitors

from engine.settings.constants import (
    SCREEN_RESOLUTIONS,
    SCREEN_RESOLUTION_MESSAGE_ERROR,
    MAX_LEN_CAPTION_TITLE,
    DEFAULT_NAME_ICON,
    BASE_SCREEN_SIZE_FRAME,
    BASE_SCREEN_SIZE_ACTION,
    BASE_VISIBLE_MAP_SIZE,
    RectOutlineWidthEnum,
    TimeBetweenAnimationActionsEnum,
    TimeBetweenAnimationFramesEnum,
    VolumeEnum,
    FPSEnum,
    RGBColorEnum,
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


class ScreenResolutionSchema(BaseModel):
    """Схема разрешения экрана."""

    width: int = Field(description='Ширина экрана')
    height: int = Field(description='Высота экрана')

    @model_validator(mode='after')
    @classmethod
    def validate_all_before(cls, values: 'ScreenResolutionSchema') -> 'ScreenResolutionSchema':
        """Валидация разрешения экрана после валидации полей.

        Args:
            values (ScreenResolutionSchema): данные по полям.

        Returns:
            ScreenResolutionSchema: отвалидированные данные по полям.
        """
        if (values.width, values.height) in SCREEN_RESOLUTIONS:
            return values
        raise ValueError(SCREEN_RESOLUTION_MESSAGE_ERROR.format(values.width, values.height))


class RGBColorSchema(BaseModel):
    """Схема RGB цвета."""

    red: int = Field(
        default=RGBColorEnum.DEFAULT_RED,
        ge=RGBColorEnum.MIN_COLOR,
        le=RGBColorEnum.MAX_COLOR,
        description='Красный цвет',
    )
    green: int = Field(
        default=RGBColorEnum.DEFAULT_GREEN,
        ge=RGBColorEnum.MIN_COLOR,
        le=RGBColorEnum.MAX_COLOR,
        description='Зелёный цвет',
    )
    blue: int = Field(
        default=RGBColorEnum.DEFAULT_BLUE,
        ge=RGBColorEnum.MIN_COLOR,
        le=RGBColorEnum.MAX_COLOR,
        description='Голубой',
    )


class GraphicsSettingsSchema(BaseSettingsSchema):
    """Схема настроек графики."""

    screen_resolution: ScreenResolutionSchema = Field(
        default_factory=lambda: GraphicsSettingsSchema.get_default_screen_resolution(),
        description='Разрешение экрана',
    )
    fullscreen: bool = Field(default=True, description='Флаг полного экрана')
    max_fps: int = Field(
        default=FPSEnum.MAX_FPS, le=FPSEnum.MAX_FPS, ge=FPSEnum.MIN_FPS, description='Максимальная частота кадров'
    )

    @staticmethod
    def get_default_screen_resolution() -> ScreenResolutionSchema:
        """Отдаёт дефолтное значение разрешение экрана.

        Returns:
            ScreenResolutionSchema: разрешение экрана.
        """
        monitor = get_monitors()[0]
        return ScreenResolutionSchema(width=monitor.width, height=monitor.height)


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
        default=TimeBetweenAnimationFramesEnum.DEFAULT_TIME,
        ge=TimeBetweenAnimationFramesEnum.MIN_TIME,
        le=TimeBetweenAnimationFramesEnum.MAX_TIME,
        description='Время между кадрами анимаций',
    )
    time_between_animation_actions: int = Field(
        default=TimeBetweenAnimationActionsEnum.DEFAULT_TIME,
        ge=TimeBetweenAnimationActionsEnum.MIN_TIME,
        le=TimeBetweenAnimationActionsEnum.MAX_TIME,
        description='Время между действиями',
    )
    base_screen_size_frame: ScreenResolutionSchema = Field(
        default_factory=lambda: EngineSettingsSchema.get_base_screen_size_frame(),
        description='Базовое разрешение экрана расчёта размера фрейма',
    )
    base_screen_size_action: ScreenResolutionSchema = Field(
        default_factory=lambda: EngineSettingsSchema.get_base_screen_size_action(),
        description='Базовое разрешение экрана расчёта скорости действия',
    )
    base_visible_map_size: ScreenResolutionSchema = Field(
        default_factory=lambda: EngineSettingsSchema.get_base_visible_map_size(),
        description='Базовый размер видимой игровой карты',
    )
    debug_mode: bool = Field(default=False, description='Флаг debug mode')
    rect_outline_color: RGBColorSchema = Field(
        default_factory=lambda: EngineSettingsSchema.get_rect_outline_color(),
        description='Цвет обводки rect',
    )
    rect_outline_width: int = Field(
        default=RectOutlineWidthEnum.DEFAULT_WIDTH,
        ge=RectOutlineWidthEnum.MIN_WIDTH,
        le=RectOutlineWidthEnum.MAX_WIDTH,
        description='Ширина обводки rect',
    )

    @staticmethod
    def get_rect_outline_color() -> RGBColorSchema:
        """Отдаёт цвет обводки rect.

        Returns:
            RGBColorSchema: цвет обводки rect.
        """
        return RGBColorSchema(
            red=RGBColorEnum.DEFAULT_RED,
            green=RGBColorEnum.DEFAULT_GREEN,
            blue=RGBColorEnum.DEFAULT_BLUE,
        )

    @staticmethod
    def get_base_screen_size_frame() -> ScreenResolutionSchema:
        """Отдаёт базовое значение разрешения экрана расчёта размера фрейма.

        Returns:
            ScreenResolutionSchema: разрешение экрана.
        """
        return ScreenResolutionSchema(width=BASE_SCREEN_SIZE_FRAME.width, height=BASE_SCREEN_SIZE_FRAME.height)

    @staticmethod
    def get_base_screen_size_action() -> ScreenResolutionSchema:
        """Отдаёт базовое значение разрешения экрана расчёта скорости действия.

        Returns:
            ScreenResolutionSchema: разрешение экрана.
        """
        return ScreenResolutionSchema(width=BASE_SCREEN_SIZE_ACTION.width, height=BASE_SCREEN_SIZE_ACTION.height)

    @staticmethod
    def get_base_visible_map_size() -> ScreenResolutionSchema:
        """Отдаёт базовое значение размера видимой игровой карты.

        Returns:
            ScreenResolutionSchema: разрешение экрана.
        """
        return ScreenResolutionSchema(width=BASE_VISIBLE_MAP_SIZE.width, height=BASE_VISIBLE_MAP_SIZE.height)

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
