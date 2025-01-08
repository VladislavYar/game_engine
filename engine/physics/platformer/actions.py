from engine.constants.direction import DirectionGroupEnum

from engine.actions import DynamicAction
from engine.objects.constants import NameSpeedEnum
from engine.objects.groups import SolidObjectsGroup
from engine.physics.actions import MovementAction, WalkAction, RunAction
from engine.physics.constants import SING_X_Y


class CheckObjectAction(DynamicAction):
    """Action проверки игрового объекта.

    Attributes:
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _check_status_fall(self) -> None:
        """Проверка статуса падения."""
        if self._get_count_actions_performed():
            self._obj.status.fall = True
        moving_y = self._obj.speed.fall
        self._obj.rect.y += moving_y
        if self._solid_objects_group.collide_rect_with_mask(self._obj):
            self._elapsed = 0
            self._obj.status.fall = False
        self._obj.rect.y -= moving_y

    def _check_jamming(self) -> None:
        """Проверка на застревание."""

        for direction in (DirectionGroupEnum.DOWN,):
            self._push_out_object(self._obj, self._solid_objects_group, direction, SING_X_Y[direction])

    def perform(self) -> None:
        """Логика проверки статусов игрового объекта."""
        self._check_status_fall()
        self._check_jamming()


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
