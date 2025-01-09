from typing import Iterable

from engine.actions import DynamicAction
from engine.constants.direction import DirectionGroupEnum
from engine.physics.constants import SING_X_Y
from engine.objects.constants import NameSpeedEnum, NameStatusEnum
from engine.objects.groups import SolidObjectsGroup


class MovementAction(DynamicAction):
    """Движение.

    Attributes:
        direction_movement (DirectionGroupEnum): направление движения.
        name_field_speed (NameSpeedEnum): название поля скорости.
        name_field_boost (NameSpeedEnum | None, optional): название поля ускорения. По дефолту None.
        name_statuses_field (Iterable[NameStatusEnum], optional): названия полей статуса. По дефолту list.
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    direction_movement: DirectionGroupEnum
    name_field_speed: NameSpeedEnum
    name_field_boost: NameSpeedEnum | None = None
    name_statuses_field: Iterable[NameStatusEnum] = []
    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _set_default_values(self) -> None:
        """Добавляет к дефолтным значениям обновление текущего ускорения."""
        super()._set_default_values()
        self._current_boost = 0

    def perform(self) -> None:
        """Логика выполнения действия движения."""
        if self.direction_movement not in (DirectionGroupEnum.UP, DirectionGroupEnum.DOWN):
            self._obj.direction = self.direction_movement
        sign_x, sign_y = SING_X_Y[self.direction_movement]
        boost = 0
        if self.name_field_boost:
            boost = getattr(self._obj.speed, self.name_field_boost)
        self._current_boost += boost * self._global_clock.dt
        speed = getattr(self._obj.speed, self.name_field_speed) + self._current_boost
        move_x = speed * sign_x * self._global_clock.dt
        move_y = speed * sign_y * self._global_clock.dt
        self._obj.rect.x += move_x
        self._obj.rect.y += move_y
        if self._solid_objects_group.collide_rect_with_mask(self._obj):
            for status in self.name_statuses_field:
                setattr(self._obj.status, status, False)
            self._obj.rect.x -= move_x
            self._obj.rect.y -= move_y


class WalkAction(MovementAction):
    """Ходьба."""

    name_field_speed = NameSpeedEnum.WALK
    name_field_boost = NameSpeedEnum.WALK_BOOST


class RunAction(MovementAction):
    """Бег."""

    name_field_speed = NameSpeedEnum.RUN
    name_field_boost = NameSpeedEnum.RUN_BOOST
