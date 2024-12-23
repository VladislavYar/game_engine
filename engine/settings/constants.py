from enum import IntEnum, Enum

from engine.constants import BasePathEnum


COEFS_SCREEN = {
    2560: 1,
    1920: 1.33,
    1600: 1.6,
    1366: 1.874,
    1280: 2,
}

SCREEN_RESOLUTIONS = (
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
    (2160, 1080),
    (2560, 1440),
    (2960, 1440),
    (3200, 1800),
    (3840, 2160),
)

SCREEN_RESOLUTION_MESSAGE_ERROR = 'Разрешение экрана {}x{} не поддерживается'

MAX_LEN_CAPTION_TITLE = 120

DEFAULT_NAME_ICON = 'icon.ico'

ENCODING = 'utf-8'


class TimeBetweenAnimationFrames(IntEnum):
    """Enum промежуток времени между кадрами."""

    DEFAULT_TIME = 150
    MIN_TIME = 10
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
