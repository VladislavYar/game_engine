from pydantic import BaseModel, Field, model_validator, field_validator, FilePath
from screeninfo import get_monitors
from pygame import font

from engine.settings.constants import (
    SCREEN_RESOLUTIONS,
    SCREEN_RESOLUTION_MESSAGE_ERROR,
    MAX_LEN_CAPTION_TITLE,
    BASE_VISIBLE_MAP_SIZE,
    ACCEPTABLE_ICON_FORMATS,
    ACCEPTABLE_FONT_FORMATS,
    NO_FONT_IN_SYSTEM_MESSAGE_ERROR,
    RectInnerOutlineWidthEnum,
    DisplayFPSCoordinateEnum,
    RectOutlineWidthEnum,
    TimeBetweenAnimationFramesEnum,
    VolumeEnum,
    FPSEnum,
    RGBColorEnum,
    TextSizeEnum,
    ImageScaleEnum,
    SizeEnum,
    ColumnsRowsEnum,
    RectInnerOutlineRGBColorEnum,
    RectOutlineRGBColorEnum,
    CameraSmoothnessEnum,
    CoefFrameTimeEnum,
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
        if isinstance(value, BaseModel) and not isinstance(value, BaseSettingsSchema):
            return tuple(value.model_dump().values())
        return value

    def __setitem__(self, key: str, value: TYPES_SETTINGS) -> None:
        """Устанавливает настройку по ключу.

        Args:
            key (str): ключ настройки.
            value (TYPES_SETTINGS): значение настройки.
        """
        setattr(self, key, value)


class SizeSchema(BaseModel):
    """Схема размера."""

    width: int = Field(
        default=SizeEnum.DEFAULT_SIZE,
        ge=SizeEnum.MIN_SIZE,
        description='Ширина',
    )
    height: int = Field(
        default=SizeEnum.DEFAULT_SIZE,
        ge=SizeEnum.MIN_SIZE,
        description='Высота',
    )


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


class CoordinateSchema(BaseModel):
    """Схема координатов."""

    x: int = Field(description='Координата x')
    y: int = Field(description='Координата y')


class GraphicsSettingsSchema(BaseSettingsSchema):
    """Схема настроек графики."""

    screen_resolution: ScreenResolutionSchema = Field(
        default=ScreenResolutionSchema(width=get_monitors()[0].width, height=get_monitors()[0].height),
        description='Разрешение экрана',
    )
    fullscreen: bool = Field(default=True, description='Флаг полного экрана')
    max_fps: int = Field(
        default=FPSEnum.MAX_FPS, le=FPSEnum.MAX_FPS, ge=FPSEnum.MIN_FPS, description='Максимальная частота кадров'
    )


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


class RectOutlineSchema(BaseSettingsSchema):
    """Схема обводки rect."""

    rect_outline_color: RGBColorSchema = Field(
        default=RGBColorSchema(
            red=RectOutlineRGBColorEnum.DEFAULT_RED,
            green=RectOutlineRGBColorEnum.DEFAULT_GREEN,
            blue=RectOutlineRGBColorEnum.DEFAULT_BLUE,
        ),
        description='Цвет обводки rect',
    )
    rect_outline_width: int = Field(
        default=RectOutlineWidthEnum.DEFAULT_WIDTH,
        ge=RectOutlineWidthEnum.MIN_WIDTH,
        le=RectOutlineWidthEnum.MAX_WIDTH,
        description='Ширина обводки rect',
    )
    rect_inner_outline_color: RGBColorSchema = Field(
        default=RGBColorSchema(
            red=RectInnerOutlineRGBColorEnum.DEFAULT_RED,
            green=RectInnerOutlineRGBColorEnum.DEFAULT_GREEN,
            blue=RectInnerOutlineRGBColorEnum.DEFAULT_BLUE,
        ),
        description='Цвет внутренний обводки rect',
    )
    rect_inner_outline_width: int = Field(
        default=RectInnerOutlineWidthEnum.DEFAULT_WIDTH,
        ge=RectInnerOutlineWidthEnum.MIN_WIDTH,
        le=RectInnerOutlineWidthEnum.MAX_WIDTH,
        description='Ширина внутренний обводки rect',
    )


class TextSchema(BaseSettingsSchema):
    """Схема текста."""

    text_color: RGBColorSchema = Field(
        default=RGBColorSchema(
            red=RGBColorEnum.DEFAULT_RED,
            green=RGBColorEnum.DEFAULT_GREEN,
            blue=RGBColorEnum.DEFAULT_BLUE,
        ),
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
        default_factory=lambda: TextSchema._correct_name_fount(font.get_default_font()),
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


class TileGridSchema(RectOutlineSchema):
    """Схема сетки тайтлов."""

    columns: int = Field(
        description='Количество столбцов',
        default=ColumnsRowsEnum.DEFAULT_COUNT,
        ge=ColumnsRowsEnum.MIN_COUNT,
    )
    rows: int = Field(
        description='Количество строк',
        default=ColumnsRowsEnum.DEFAULT_COUNT,
        ge=ColumnsRowsEnum.MIN_COUNT,
    )
    tile_size: SizeSchema = Field(
        default=SizeSchema(width=SizeEnum.DEFAULT_SIZE, height=SizeEnum.DEFAULT_SIZE),
        description='Размер тайтла',
    )


class DebugSchema(RectOutlineSchema):
    """Схема debug."""

    debug_mode: bool = Field(default=False, description='Флаг debug mode')
    display_fps_coordinate: CoordinateSchema = Field(
        default=CoordinateSchema(x=DisplayFPSCoordinateEnum.X, y=DisplayFPSCoordinateEnum.Y),
        description='Координаты вывода fps',
    )


class CameraSchema(RectOutlineSchema):
    """Схема камеры."""

    camera_smoothness: float = Field(
        default=CameraSmoothnessEnum.DEFAULT_SMOOTHNESS.value,
        ge=CameraSmoothnessEnum.MIN_SMOOTHNESS.value,
        le=CameraSmoothnessEnum.MAX_SMOOTHNESS.value,
        description='Плавность камеры',
    )
    dead_zone: SizeSchema = Field(
        default=SizeSchema(width=SizeEnum.DEFAULT_SIZE, height=SizeEnum.DEFAULT_SIZE),
        description='Мёртвая зона камеры',
    )


class EngineSettingsSchema(BaseSettingsSchema):
    """Схема настроек движка."""

    caption_title: str | None = Field(
        default=None, description='Заголовок окна игры', max_length=MAX_LEN_CAPTION_TITLE
    )
    path_icon: FilePath | None = Field(default=None, alias='name_icon', description='Название иконки окна игры')
    base_visible_map_size: ScreenResolutionSchema = Field(
        default=ScreenResolutionSchema(width=BASE_VISIBLE_MAP_SIZE.width, height=BASE_VISIBLE_MAP_SIZE.height),
        description='Базовый размер видимой игровой карты',
    )
    camera: CameraSchema = Field(
        default=CameraSchema(
            camera_smoothness=CameraSmoothnessEnum.DEFAULT_SMOOTHNESS.value,
            dead_zone=SizeSchema(width=SizeEnum.DEFAULT_SIZE, height=SizeEnum.DEFAULT_SIZE),
        ),
        description='Камера',
    )
    time_between_animation_frames: int = Field(
        default=TimeBetweenAnimationFramesEnum.DEFAULT_TIME,
        ge=TimeBetweenAnimationFramesEnum.MIN_TIME,
        le=TimeBetweenAnimationFramesEnum.MAX_TIME,
        description='Время между кадрами анимаций',
    )
    debug: DebugSchema = Field(
        default=DebugSchema(
            debug_mode=False,
            display_fps_coordinate=CoordinateSchema(x=DisplayFPSCoordinateEnum.X, y=DisplayFPSCoordinateEnum.Y),
        ),
        description='Debug',
    )
    rect_outline: RectOutlineSchema = Field(
        default=RectOutlineSchema(
            rect_outline_color=RGBColorSchema(
                red=RGBColorEnum.DEFAULT_RED,
                green=RGBColorEnum.DEFAULT_GREEN,
                blue=RGBColorEnum.DEFAULT_BLUE,
            ),
            rect_outline_width=RectOutlineWidthEnum.DEFAULT_WIDTH,
            rect_inner_outline_color=RGBColorSchema(
                red=RGBColorEnum.DEFAULT_RED,
                green=RGBColorEnum.DEFAULT_GREEN,
                blue=RGBColorEnum.DEFAULT_BLUE,
            ),
            rect_inner_outline_width=RectOutlineWidthEnum.DEFAULT_WIDTH,
        ),
        description='Обводка rect',
    )
    text: TextSchema = Field(
        default=TextSchema(
            text_color=RGBColorSchema(
                red=RGBColorEnum.DEFAULT_RED,
                green=RGBColorEnum.DEFAULT_GREEN,
                blue=RGBColorEnum.DEFAULT_BLUE,
            ),
            text_size=TextSizeEnum.DEFAULT_SIZE,
            name_fount=TextSchema._correct_name_fount(font.get_default_font()),
        ),
        description='Текст',
    )
    scale_image: float = Field(
        default=ImageScaleEnum.DEFAULT_SCALE.value,
        ge=ImageScaleEnum.MIN_SCALE.value,
        le=ImageScaleEnum.MAX_SCALE.value,
        description='Scale изображений',
    )
    tile_grid: TileGridSchema = Field(
        default=TileGridSchema(
            columns=ColumnsRowsEnum.DEFAULT_COUNT,
            rows=ColumnsRowsEnum.DEFAULT_COUNT,
            tile_size=SizeSchema(width=SizeEnum.DEFAULT_SIZE, height=SizeEnum.DEFAULT_SIZE),
            rect_outline_color=RGBColorSchema(
                red=RGBColorEnum.DEFAULT_RED,
                green=RGBColorEnum.DEFAULT_GREEN,
                blue=RGBColorEnum.DEFAULT_BLUE,
            ),
            rect_outline_width=RectOutlineWidthEnum.DEFAULT_WIDTH,
        ),
        description='Сетка тайтлов',
    )
    coef_frame_time: float = Field(
        default=CoefFrameTimeEnum.DEFAULT_COEF.value,
        ge=CoefFrameTimeEnum.MIN_COEF.value,
        le=CoefFrameTimeEnum.MAX_COEF.value,
        description='Коэффициент времени кадра',
    )

    @field_validator('path_icon', mode='before')
    @classmethod
    def validate_path_icon(cls, value: str) -> str:
        """Фомирование путь до иконки окна игры и валидирует тип файла."""
        validate_format_file(value, ACCEPTABLE_ICON_FORMATS)
        return BasePathEnum.ICONS_PATH.value / value


class AllSettingsSchema(BaseModel):
    """Схема всех настроек."""

    audio: AudioSettingsSchema = Field(description='Настройки звука')
    graphics: GraphicsSettingsSchema = Field(description='Настройки графики')
    engine: EngineSettingsSchema = Field(description='Настройки движка')
