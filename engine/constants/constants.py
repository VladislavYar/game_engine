from collections import namedtuple


ZERO_COORDINATES = (0, 0)

Size = namedtuple('Size', ('width', 'height'))
Color = namedtuple('Color', ('red', 'green', 'blue'))

WRITING_ONLY = AttributeError('Атрибут доступен только для записи')
