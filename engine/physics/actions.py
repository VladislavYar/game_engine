from engine.actions import DynamicAction
from engine.constants.direction import DirectionGroupEnum
from engine.physics.constants import SING_X_Y
from engine.objects.constants import NameSpeedEnum
from engine.objects.groups import SolidObjectsGroup


class MovementAction(DynamicAction):
    """Движение.

    Attributes:
        direction_movement (DirectionGroupEnum): направление движения.
        name_field_speed (NameSpeedEnum): название поля скорости.
        name_field_boost (NameSpeedEnum | None, optional): название поля ускорения. По дефолту None.
        boost (float): ускорение действия.
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    direction_movement: DirectionGroupEnum
    name_field_speed: NameSpeedEnum
    name_field_boost: NameSpeedEnum | None = None
    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _set_default_values(self) -> None:
        """Добавляет к дефолтным значениям обновление текущего ускорения."""
        super()._set_default_values()
        self._current_boost = 0

    def perform(self) -> None:
        """Логика выполнения действия движения."""
        if self.direction_movement not in (DirectionGroupEnum.UP, DirectionGroupEnum.DOWN):
            self._obj.direction = self.direction_movement
        count_actions_performed = self._get_count_actions_performed()
        sign_x, sign_y = SING_X_Y[self.direction_movement]
        boost = 0
        if self.name_field_boost:
            boost = getattr(self._obj.speed, self.name_field_boost)
        for _ in range(count_actions_performed):
            self._current_boost += boost
            move_x = (getattr(self._obj.speed, self.name_field_speed) + self._current_boost) * sign_x
            move_y = (getattr(self._obj.speed, self.name_field_speed) + self._current_boost) * sign_y
            self._obj.rect.x += move_x
            self._obj.rect.y += move_y
            if self._solid_objects_group.collide_mask(self._obj):
                self._obj.rect.x -= move_x
                self._obj.rect.y -= move_y
                break


class WalkAction(MovementAction):
    """Ходьба."""

    name_field_speed = NameSpeedEnum.WALK
    name_field_boost = NameSpeedEnum.WALK_BOOST


class RunAction(MovementAction):
    """Бег."""

    name_field_speed = NameSpeedEnum.RUN
    name_field_boost = NameSpeedEnum.RUN_BOOST
