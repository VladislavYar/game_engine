from collections import namedtuple

from engine.constants import Scale


CoefShiftRate = namedtuple('CoefShiftRate', ('x', 'y'), defaults=(1, 1))

Background = namedtuple(
    'Background', ('path_image', 'scale', 'coef_shift_rate'), defaults=('', Scale(), CoefShiftRate())
)
