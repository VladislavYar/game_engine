from collections import namedtuple


Coordinate = namedtuple('Coordinate', ('x', 'y'))

Size = namedtuple('Size', ('width', 'height'))

Color = namedtuple('Color', ('red', 'green', 'blue'))

Scale = namedtuple('Scale', ('width', 'height'), defaults=(1, 1))

WRITING_ONLY = AttributeError('Атрибут доступен только для записи')
