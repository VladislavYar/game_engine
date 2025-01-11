from enum import Enum
from pathlib import Path


class BasePathEnum(Enum):
    """Enum базовых путей."""

    BASE_PATH = Path(__file__).parent.parent.parent
    RESOURCES_PATH = BASE_PATH / 'resources'
    SOUNDS_PATH = RESOURCES_PATH / 'sounds'
    SETTINGS_PATH = RESOURCES_PATH / 'settings'
    IMAGES_PATH = RESOURCES_PATH / 'images'
    FONTS_PATH = BASE_PATH / 'fonts'
    ICONS_PATH = IMAGES_PATH / 'icons'
    ANIMATIONS_PATH = IMAGES_PATH / 'animations'
    BACKGROUNDS_PATH = IMAGES_PATH / 'backgrounds'
