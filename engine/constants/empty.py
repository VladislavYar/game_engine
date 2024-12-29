from pygame import Surface, SRCALPHA

from engine.animations.frames import EmptyFrame
from engine.constants import Size


WITHOUT_SIZE = Size(0, 0)

EMPTY_SURFACE = Surface(WITHOUT_SIZE, SRCALPHA)

EMPTY_FRAME = EmptyFrame(EMPTY_SURFACE)
