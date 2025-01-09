from collections import namedtuple


Coordinate = namedtuple('Coordinate', ('x', 'y'))

Size = namedtuple('Size', ('width', 'height'))

Color = namedtuple('Color', ('red', 'green', 'blue'))

ZERO_COORDINATES = Coordinate(0, 0)

ZERO_COORDINATES_SHIFT = ZERO_COORDINATES

WRITING_ONLY = AttributeError('Атрибут доступен только для записи')

WITHOUT_SIZE = Size(0, 0)
