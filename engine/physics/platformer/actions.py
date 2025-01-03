from engine.constants.direction import DirectionGroupEnum
from engine.physics.actions import WalkAction, RunAction


class WalkLeftAction(WalkAction):
    """Ходьба влево."""

    direction_movement = DirectionGroupEnum.LEFT


class WalkRightAction(WalkAction):
    """Ходьба вправо."""

    direction_movement = DirectionGroupEnum.RIGHT


class RunLeftAction(RunAction):
    """Бег влево."""

    direction_movement = DirectionGroupEnum.LEFT


class RunRightAction(RunAction):
    """Бег вправо."""

    direction_movement = DirectionGroupEnum.RIGHT
