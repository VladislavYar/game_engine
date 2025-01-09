from engine.constants.direction import DirectionGroupEnum

from engine.actions import DynamicAction
from engine.objects.constants import NameSpeedEnum, NameStatusEnum
from engine.objects.groups import SolidObjectsGroup
from engine.physics.actions import MovementAction, WalkAction, RunAction


class CheckObjectAction(DynamicAction):
    """Action проверки игрового объекта.

    Attributes:
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _check_status_fall(self) -> None:
        """Проверка статуса падения."""
        if self._obj.status.jump or self._obj.status.double_jump:
            return
        moving_y = self._obj.speed.fall
        self._obj.rect.y += moving_y
        if self._solid_objects_group.collide_rect_with_mask(self._obj, DirectionGroupEnum.DOWN):
            self._elapsed = 0
            self._obj.status.fall = False
        else:
            self._obj.status.fall = True
        self._obj.rect.y -= moving_y

    def perform(self) -> None:
        """Логика проверки статусов игрового объекта."""
        self._check_status_fall()


class JumpStatusAction(DynamicAction):
    """Проверка статуса прыжка."""

    def perform(self) -> None:
        """Логика проверки статуса прыжка."""
        status = self._obj.status
        if not status.jump:
            status.fall = False
            status.jump = True
            return
        status.fall = status.jump = False
        status.double_jump = True


class JumpAction(MovementAction):
    """Прыжок."""

    name_field_speed = NameSpeedEnum.JUMP
    name_field_boost = NameSpeedEnum.JUMP_BOOST
    direction_movement = DirectionGroupEnum.UP
    name_statuses_field = (NameStatusEnum.JUMP, NameStatusEnum.FALL)


class DoubleJumpAction(MovementAction):
    """Двойной прыжок."""

    name_field_speed = NameSpeedEnum.DOUBLE_JUMP
    name_field_boost = NameSpeedEnum.DOUBLE_JUMP_BOOST
    direction_movement = DirectionGroupEnum.UP
    name_statuses_field = (NameStatusEnum.DOUBLE_JUMP, NameStatusEnum.FALL)


class FallAction(MovementAction):
    """Падение."""

    name_field_speed = NameSpeedEnum.FALL
    name_field_boost = NameSpeedEnum.FALL_BOOST
    direction_movement = DirectionGroupEnum.DOWN
    name_statuses_field = (NameStatusEnum.FALL,)


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
