from pydantic import BaseModel, Field, model_validator, field_validator, FilePath
from screeninfo import get_monitors
from pygame import font

from engine.settings.constants import (
    SCREEN_RESOLUTIONS,
    SCREEN_RESOLUTION_MESSAGE_ERROR,
    MAX_LEN_CAPTION_TITLE,
    BASE_SCREEN_SIZE_FRAME,
    BASE_SCREEN_SIZE_ACTION,
    BASE_SCREEN_SIZE_TEXT,
    BASE_VISIBLE_MAP_SIZE,
    ACCEPTABLE_ICON_FORMATS,
    ACCEPTABLE_FONT_FORMATS,
    NO_FONT_IN_SYSTEM_MESSAGE_ERROR,
    CoefDropCheckEnum,
    RectOutlineWidthEnum,
    TimeBetweenAnimationActionsEnum,
    TimeBetweenAnimationFramesEnum,
    VolumeEnum,
    FPSEnum,
    RGBColorEnum,
    TextSizeEnum,
)
from engine.utils.file import validate_format_file
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

    caption_title: str | None = Field(
        default=None, description='Заголовок окна игры', max_length=MAX_LEN_CAPTION_TITLE
    )
    path_icon: FilePath | None = Field(default=None, alias='name_icon', description='Название иконки окна игры')
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
    base_screen_size_text: ScreenResolutionSchema = Field(
        default_factory=lambda: EngineSettingsSchema.get_base_screen_size_text(),
        description='Базовое разрешение экрана расчёта размера текста',
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
    coef_drop_check: float = Field(
        default=CoefDropCheckEnum.DEFAULT_COEF.value,
        ge=CoefDropCheckEnum.MIN_COEF.value,
        le=CoefDropCheckEnum.MAX_COEF.value,
        description='Коэффициент к проверке падения',
    )
    text_color: RGBColorSchema = Field(
        default_factory=lambda: EngineSettingsSchema.get_text_color(),
        description='Цвет текста',
    )
    text_size: int = Field(
        default=TextSizeEnum.DEFAULT_SIZE,
        ge=TextSizeEnum.MIN_SIZE,
        le=TextSizeEnum.MAX_SIZE,
        description='Размер текста',
    )
    path_fount: FilePath | None = Field(default=None, description='Путь до ширифта')
    name_fount: str = Field(
        default_factory=lambda: EngineSettingsSchema._correct_name_fount(font.get_default_font()),
        description='Название ширифта',
    )

    @staticmethod
    def _correct_name_fount(name_fount: str) -> str:
        """Корректирует название ширифта.

        Args:
            name_fount (str): название ширифта.

        Returns:
            str: корректное название ширифта.
        """
        return ''.join(name_fount.lower().split()).split('.')[0]

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
    def get_text_color() -> RGBColorSchema:
        """Отдаёт цвет текста.

        Returns:
            RGBColorSchema: отдаёт цвет текста.
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
    def get_base_screen_size_text() -> ScreenResolutionSchema:
        """Отдаёт базовое значение разрешения экрана расчёта размера текста.

        Returns:
            ScreenResolutionSchema: разрешение экрана.
        """
        return ScreenResolutionSchema(width=BASE_SCREEN_SIZE_TEXT.width, height=BASE_SCREEN_SIZE_TEXT.height)

    @staticmethod
    def get_base_visible_map_size() -> ScreenResolutionSchema:
        """Отдаёт базовое значение размера видимой игровой карты.

        Returns:
            ScreenResolutionSchema: разрешение экрана.
        """
        return ScreenResolutionSchema(width=BASE_VISIBLE_MAP_SIZE.width, height=BASE_VISIBLE_MAP_SIZE.height)

    @field_validator('path_icon', mode='before')
    @classmethod
    def validate_path_icon(cls, value: str) -> str:
        """Фомирование путь до иконки окна игры и валидирует тип файла."""
        validate_format_file(value, ACCEPTABLE_ICON_FORMATS)
        return BasePathEnum.ICONS_PATH.value / value

    @field_validator('path_fount', mode='before')
    @classmethod
    def validate_path_fount(cls, value: FilePath) -> FilePath:
        """Фомирование путь до шрифта игры и валидирует тип файла."""
        validate_format_file(value, ACCEPTABLE_FONT_FORMATS)
        return BasePathEnum.FONTS_PATH.value / value

    @field_validator('name_fount', mode='after')
    @classmethod
    def validate_name_fount(cls, value: str) -> str:
        """Проверяет наличие ширифта в системе."""
        if cls._correct_name_fount(value) in font.get_fonts():
            return value
        raise ValueError(NO_FONT_IN_SYSTEM_MESSAGE_ERROR.format(value))


class AllSettingsSchema(BaseModel):
    """Схема всех настроек."""

    audio: AudioSettingsSchema = Field(description='Настройки звука')
    graphics: GraphicsSettingsSchema = Field(description='Настройки графики')
    engine: EngineSettingsSchema = Field(description='Настройки движка')
