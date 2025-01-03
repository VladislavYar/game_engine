from engine.constants.direction import DirectionGroupEnum
from engine.physics.actions import WalkAction


class WalkUpAction(WalkAction):
    """Ходьба вверх."""

    direction_movement = DirectionGroupEnum.UP


class WalkDownAction(WalkAction):
    """Ходьба вниз."""

    direction_movement = DirectionGroupEnum.DOWN


class WalkRightUpAction(WalkAction):
    """Ходьба вправо-вверх."""

    direction_movement = DirectionGroupEnum.UP_RIGHT


class WalkLeftDownAction(WalkAction):
    """Ходьба влево-вниз."""

    direction_movement = DirectionGroupEnum.DOWN_LEFT


class WalkLeftUpAction(WalkAction):
    """Ходьба влево-вверх."""

    direction_movement = DirectionGroupEnum.UP_LEFT


class WalkRightDownAction(WalkAction):
    """Ходьба вправо-вниз."""

    direction_movement = DirectionGroupEnum.DOWN_RIGHT


class WalkLeftAction(WalkAction):
    """Ходьба влево."""

    direction_movement = DirectionGroupEnum.LEFT


class WalkRightAction(WalkAction):
    """Ходьба вправо."""

    direction_movement = DirectionGroupEnum.RIGHT
