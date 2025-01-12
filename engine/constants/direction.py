from enum import StrEnum, Enum


class DirectionEnum(StrEnum):
    """Enum направлений."""

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class DirectionGroupEnum(Enum):
    """Enum групп направлений."""

    UP = frozenset((DirectionEnum.UP,))
    DOWN = frozenset((DirectionEnum.DOWN,))
    LEFT = frozenset((DirectionEnum.LEFT,))
    RIGHT = frozenset((DirectionEnum.RIGHT,))
    UP_RIGHT = frozenset((DirectionEnum.UP, DirectionEnum.RIGHT))
    UP_LEFT = frozenset((DirectionEnum.UP, DirectionEnum.LEFT))
    DOWN_LEFT = frozenset((DirectionEnum.DOWN, DirectionEnum.LEFT))
    DOWN_RIGHT = frozenset((DirectionEnum.DOWN, DirectionEnum.RIGHT))


OPPOSITE_DIRECTIONS = {
    DirectionEnum.UP: DirectionEnum.DOWN,
    DirectionEnum.DOWN: DirectionEnum.UP,
    DirectionEnum.LEFT: DirectionEnum.RIGHT,
    DirectionEnum.RIGHT: DirectionEnum.LEFT,
}
