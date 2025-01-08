from collections import namedtuple

Flip = namedtuple('Flip', ('x', 'y', 'direction'), defaults=(False, False, False))

ScaleRect = namedtuple('ScaleRect', ('width', 'height'), defaults=(1, 1))

ScaleImage = namedtuple('ScaleImage', ('width', 'height'), defaults=(1, 1))
