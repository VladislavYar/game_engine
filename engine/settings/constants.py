from enum import IntEnum, Enum

from engine.constants.path import BasePathEnum

from engine.constants import Size


SCREEN_RESOLUTIONS = (
    Size(1280, 720),
    Size(1366, 768),
    Size(1600, 900),
    Size(1920, 1080),
    Size(2560, 1440),
    Size(3840, 2160),
)

BASE_VISIBLE_MAP_SIZE = SCREEN_RESOLUTIONS[-1]

SCREEN_RESOLUTION_MESSAGE_ERROR = 'Разрешение экрана {}x{} не поддерживается'

NO_FONT_IN_SYSTEM_MESSAGE_ERROR = 'Ширифт {} отсутсвует в системе'

MAX_LEN_CAPTION_TITLE = 120

ENCODING = 'utf-8'

ACCEPTABLE_ICON_FORMATS = ('.png', '.bmp', '.jpeg', '.gif', '.tga')

ACCEPTABLE_FONT_FORMATS = ('.ttf', '.otf', '.bdf', 'pcf')


class TimeBetweenAnimationFramesEnum(IntEnum):
    """Enum промежуток времени между кадрами."""

    DEFAULT_TIME = 150
    MIN_TIME = 1
    MAX_TIME = 1000


class TimeBetweenActionsEnum(IntEnum):
    """Enum промежуток времени между действиями."""

    DEFAULT_TIME = 50
    MIN_TIME = 1
    MAX_TIME = 1000


class RectOutlineWidthEnum(IntEnum):
    """Enum ширины обводки rect."""

    DEFAULT_WIDTH = 3
    MIN_WIDTH = 0
    MAX_WIDTH = 10


class RectInnerOutlineWidthEnum(IntEnum):
    """Enum ширины внутренний обводки rect."""

    DEFAULT_WIDTH = 2
    MIN_WIDTH = 0
    MAX_WIDTH = 10


class RGBColorEnum(IntEnum):
    """Enum RGB цвета."""

    DEFAULT_RED = 255
    DEFAULT_GREEN = DEFAULT_RED
    DEFAULT_BLUE = DEFAULT_GREEN
    MIN_COLOR = 0
    MAX_COLOR = 255


class RectOutlineRGBColorEnum(IntEnum):
    """Enum RGB цвета обводки rect."""

    DEFAULT_RED = 200
    DEFAULT_GREEN = DEFAULT_RED
    DEFAULT_BLUE = DEFAULT_GREEN
    MIN_COLOR = 0
    MAX_COLOR = 255


class RectInnerOutlineRGBColorEnum(IntEnum):
    """Enum RGB цвета обводки rect."""

    DEFAULT_RED = 100
    DEFAULT_GREEN = DEFAULT_RED
    DEFAULT_BLUE = DEFAULT_GREEN
    MIN_COLOR = 0
    MAX_COLOR = 255


class SettingsFilesPathEnum(Enum):
    """Enum путей до до настроек."""

    GRAPHICS = BasePathEnum.SETTINGS_PATH.value / 'graphics.json'
    AUDIO = BasePathEnum.SETTINGS_PATH.value / 'audio.json'
    ENGINE = BasePathEnum.SETTINGS_PATH.value / 'engine.json'


class VolumeEnum(Enum):
    """Enum громкости."""

    DEFAULT_VOLUME = 0.5
    MIN_VOLUME = 0
    MAX_VOLUME = 1


class FPSEnum(IntEnum):
    """Enum максимального и минимального ограничения FPS."""

    MAX_FPS = 300
    MIN_FPS = 30


class TextSizeEnum(IntEnum):
    """Enum размер текста."""

    DEFAULT_SIZE = 18
    MIN_SIZE = 1
    MAX_SIZE = 100


class ImageScaleEnum(Enum):
    """Enum scale изображений."""

    DEFAULT_SCALE = 1
    MIN_SCALE = 1
    MAX_SCALE = 100


class DisplayFPSCoordinateEnum(IntEnum):
    """Enum координат вывода fps."""

    X = 30
    Y = 30


class SizeEnum(IntEnum):
    """Enum размеров."""

    DEFAULT_SIZE = 32
    MIN_SIZE = 0


class ColumnsRowsEnum(IntEnum):
    """Enum столбцов и строчек."""

    DEFAULT_COUNT = 500
    MIN_COUNT = 1
