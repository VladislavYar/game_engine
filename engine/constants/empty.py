from pygame import Surface, SRCALPHA

from engine.animations.frames import EmptyFrame
from engine.constants import Size, Coordinate


ZERO_COORDINATES = Coordinate(0, 0)

WITHOUT_SIZE = Size(0, 0)

ZERO_COORDINATES_SHIFT = ZERO_COORDINATES

EMPTY_SURFACE = Surface(WITHOUT_SIZE, SRCALPHA)

EMPTY_FRAME = EmptyFrame(EMPTY_SURFACE, ZERO_COORDINATES_SHIFT)
