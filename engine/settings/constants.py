from enum import IntEnum, Enum

from engine.constants.path import BasePathEnum

from engine.constants import Size


BASE_SCREEN_SIZE_FRAME = BASE_SCREEN_SIZE_ACTION = Size(1280, 720)

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

SCREEN_RESOLUTION_MESSAGE_ERROR = 'Разрешение экрана {}x{} не поддерживается'

MAX_LEN_CAPTION_TITLE = 120

DEFAULT_NAME_ICON = 'icon.ico'

ENCODING = 'utf-8'


class TimeBetweenAnimationFrames(IntEnum):
    """Enum промежуток времени между кадрами."""

    DEFAULT_TIME = 150
    MIN_TIME = 1
    MAX_TIME = 1000


class TimeBetweenAnimationActions(IntEnum):
    """Enum промежуток времени между действиями."""

    DEFAULT_TIME = 50
    MIN_TIME = 1
    MAX_TIME = 1000


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
