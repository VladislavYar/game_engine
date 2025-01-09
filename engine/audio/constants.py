from enum import Enum, StrEnum

from engine.constants.path import BasePathEnum


class SoundsPathEnum(Enum):
    """Enum путей до звуков."""

    MUSICS = BasePathEnum.SOUNDS_PATH.value / 'musics'
    EFFECTS = BasePathEnum.SOUNDS_PATH.value / 'effects'
    VOICES = BasePathEnum.SOUNDS_PATH.value / 'voices'


class SoundTypeEnum(StrEnum):
    """Enum типа звука."""

    EFFECT = 'effect'
    VOICE = 'voice'
