from collections import namedtuple

from pygame import Surface, SRCALPHA

from engine.constants import WITHOUT_SIZE


Flip = namedtuple('Flip', ('x', 'y', 'direction'), defaults=(False, False, False))

ScaleRect = namedtuple('ScaleRect', ('width', 'height'), defaults=(1, 1))

ScaleImage = namedtuple('ScaleImage', ('width', 'height'), defaults=(1, 1))

EMPTY_SURFACE = Surface(WITHOUT_SIZE, SRCALPHA)
