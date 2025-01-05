from enum import IntEnum, Enum

from engine.constants.path import BasePathEnum

from engine.constants import Size


SCREEN_RESOLUTIONS = (
    Size(1280, 720),
    Size(1366, 768),
    Size(1600, 900),
    Size(1920, 1080),
    Size(2160, 1080),
    Size(2560, 1440),
    Size(2960, 1440),
    Size(3200, 1800),
    Size(3840, 2160),
)

BASE_SCREEN_SIZE_FRAME = BASE_SCREEN_SIZE_ACTION = BASE_SCREEN_SIZE_TEXT = SCREEN_RESOLUTIONS[0]

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


class TimeBetweenAnimationActionsEnum(IntEnum):
    """Enum промежуток времени между действиями."""

    DEFAULT_TIME = 50
    MIN_TIME = 1
    MAX_TIME = 1000


class RectOutlineWidthEnum(IntEnum):
    """Enum ширины обводки rect."""

    DEFAULT_WIDTH = 3
    MIN_WIDTH = 0
    MAX_WIDTH = 10


class CoefDropCheckEnum(Enum):
    """Enum коэффициента к проверке падения."""

    DEFAULT_COEF = 1
    MIN_COEF = 1
    MAX_COEF = 10


class RGBColorEnum(IntEnum):
    """Enum RGB цвета."""

    DEFAULT_RED = 255
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
