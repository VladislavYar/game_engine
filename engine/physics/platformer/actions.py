from engine.constants.direction import DirectionGroupEnum

from engine.actions import DynamicAction
from engine.objects import DynamicObject
from engine.physics.constants import SING_X_Y, COEF_DROP_CHECK
from engine.objects.constants import NameSpeedEnum
from engine.objects.groups import SolidObjectsGroup


class MovementAction(DynamicAction):
    """Движение.

    Attributes:
        direction_movement (DirectionGroupEnum): направление движения.
        name_field_speed (NameSpeedEnum): название поля скорости.
        boost (float): ускорение действия.
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    direction_movement: DirectionGroupEnum
    name_field_speed: NameSpeedEnum
    boost: float = 0
    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _set_default_values(self) -> None:
        """Добавляет к дефолтным значениям обновление текущего ускорения."""
        super()._set_default_values()
        self._current_boost = 0

    def perform(self, obj: DynamicObject) -> None:
        """Логика выполнения действия движения.

        Args:
            obj (BaseObject): игровой объект над которым совершается действие.
        """
        if self.direction_movement not in (DirectionGroupEnum.UP, DirectionGroupEnum.DOWN):
            obj.direction = self.direction_movement
        coef_x, coef_y = self._get_coef(*self.base_visible_map_size)
        count_actions_performed = self._get_count_actions_performed()
        sign_x, sign_y = SING_X_Y[self.direction_movement]
        for _ in range(count_actions_performed):
            self._current_boost += self.boost
            obj.rect.x += (getattr(obj.speed, self.name_field_speed) + self._current_boost) * coef_x * sign_x
            obj.rect.y += (getattr(obj.speed, self.name_field_speed) + self._current_boost) * coef_y * sign_y
            self._push_out_object(obj, self._solid_objects_group, self.direction_movement, (sign_x, sign_y))


class CheckObjectAction(DynamicAction):
    """Action проверки игрового объекта.

    Attributes:
        _solid_objects_group (SolidObjectsGroup): группа твёрдых объектов.
    """

    _solid_objects_group: SolidObjectsGroup = SolidObjectsGroup()

    def _check_status_fall(self, obj: DynamicObject) -> None:
        """Проверка статуса падения.

        Args:
            obj (BaseObject): игровой объект над которым совершается действие.
        """
        if self._get_count_actions_performed():
            obj.status.fall = True
        _, coef_y = self._get_coef(*self.base_visible_map_size)
        moving_y = obj.speed.fall * coef_y * COEF_DROP_CHECK
        obj.rect.y += moving_y
        if sprite := self._solid_objects_group.collide_side_mask(obj, DirectionGroupEnum.DOWN):
            obj.rect.bottom = sprite.rect.top
            self._elapsed = 0
            obj.status.fall = False
            return
        obj.rect.y -= moving_y

    def _check_jamming(self, obj: DynamicObject) -> None:
        """Проверка на застревание.

        Args:
            obj (BaseObject): игровой объект над которым совершается действие.
        """
        for direction in (DirectionGroupEnum.LEFT, DirectionGroupEnum.UP, DirectionGroupEnum.RIGHT):
            self._push_out_object(obj, self._solid_objects_group, direction, SING_X_Y[direction])

    def perform(self, obj: DynamicObject) -> None:
        """Логика проверки статусов игрового объекта.

        Args:
            obj (BaseObject): игровой объект над которым совершается действие.
        """
        self._check_status_fall(obj)
        self._check_jamming(obj)


class FallAction(MovementAction):
    """Падение."""

    name_field_speed = NameSpeedEnum.FALL
    direction_movement = DirectionGroupEnum.DOWN
    boost = 0.05


class WalkAction(MovementAction):
    """Ходьба."""

    name_field_speed = NameSpeedEnum.WALK


class RunAction(MovementAction):
    """Бег."""

    name_field_speed = NameSpeedEnum.RUN


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


class _WalkUpAction(WalkAction):
    direction_movement = DirectionGroupEnum.UP


class _WalkDownAction(WalkAction):
    direction_movement = DirectionGroupEnum.DOWN
