from enum import Enum

from engine.constants import BasePathEnum


class SoundsPathEnum(Enum):
    """Enum путей до звуков."""

    MUSICS = BasePathEnum.SOUNDS_PATH.value / 'musics'
    EFFECTS = BasePathEnum.SOUNDS_PATH.value / 'effects'
    VOICES = BasePathEnum.SOUNDS_PATH.value / 'voices'
