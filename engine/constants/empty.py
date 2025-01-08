from pygame import Surface, SRCALPHA

from engine.animations.frames import EmptyFrame
from engine.constants import Size
from engine.animations.constants import Flip, ScaleRect


WITHOUT_SIZE = Size(0, 0)

EMPTY_SURFACE = Surface(WITHOUT_SIZE, SRCALPHA)

EMPTY_FRAME = EmptyFrame(EMPTY_SURFACE, Flip(), ScaleRect(), 0)
