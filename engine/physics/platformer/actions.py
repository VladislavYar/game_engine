from engine.constants.direction import DirectionGroupEnum

from engine.actions import DynamicAction
from engine.objects import DynamicObject
from engine.physics.constants import SING_X_Y
from engine.objects.constants import NameSpeedEnum
from engine.objects.groups import SolidObjectsGroup
from engine.physics.actions import MovementAction, WalkAction, RunAction


class CheckObjectAction(DynamicAction):
    """Action проверки игрового объекта.

    Attributes:
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _check_status_fall(self, obj: DynamicObject) -> None:
        """Проверка статуса падения.

        Args:
            obj (Object): игровой объект над которым совершается действие.
        """
        if self._get_count_actions_performed():
            obj.status.fall = True
        moving_y = obj.speed.fall
        obj.rect.y += moving_y
        if self._solid_objects_group.collide_side_rect_with_mask(obj, DirectionGroupEnum.DOWN):
            self._elapsed = 0
            obj.status.fall = False
        obj.rect.y -= moving_y

    def _check_jamming(self, obj: DynamicObject) -> None:
        """Проверка на застревание.

        Args:
            obj (Object): игровой объект над которым совершается действие.
        """
        for direction in (DirectionGroupEnum.DOWN, DirectionGroupEnum.LEFT, DirectionGroupEnum.RIGHT):
            self._push_out_object(obj, self._solid_objects_group, direction, SING_X_Y[direction])

    def perform(self, obj: DynamicObject) -> None:
        """Логика проверки статусов игрового объекта.

        Args:
            obj (Object): игровой объект над которым совершается действие.
        """
        self._check_status_fall(obj)
        self._check_jamming(obj)


class FallAction(MovementAction):
    """Падение."""

    name_field_speed = NameSpeedEnum.FALL
    name_field_boost = NameSpeedEnum.FALL_BOOST
    direction_movement = DirectionGroupEnum.DOWN


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


class _RunUpAction(RunAction):
    direction_movement = DirectionGroupEnum.UP


class _RunDownAction(RunAction):
    direction_movement = DirectionGroupEnum.DOWN
