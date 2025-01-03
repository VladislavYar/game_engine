from engine.actions import DynamicAction
from engine.objects import DynamicObject
from engine.utils.screen import get_sreen_resolution
from engine.constants.direction import DirectionGroupEnum
from engine.physics.constants import SING_X_Y
from engine.objects.constants import NameSpeedEnum


class MovementAction(DynamicAction):
    """Движение.

    Attributes:
        direction_movement (DirectionGroupEnum): направление движения.
        name_field_speed (NameSpeedEnum): название поля скорости.
    """

    direction_movement: DirectionGroupEnum
    name_field_speed: NameSpeedEnum

    def perform(self, obj: DynamicObject) -> None:
        """Логика выполнения действия движения.

        Args:
            obj (BaseObject): игровой объект над которым совершается действие.
        """
        obj.direction = self.direction_movement
        coef_x, coef_y = self._get_coef(*get_sreen_resolution())
        count_actions_performed = self._get_count_actions_performed()
        sign_x, sign_y = SING_X_Y[self.direction_movement]
        for _ in range(count_actions_performed):
            obj.rect.y += getattr(obj.speed, self.name_field_speed) * coef_y * sign_y
            obj.rect.x += getattr(obj.speed, self.name_field_speed) * coef_x * sign_x


class WalkAction(MovementAction):
    """Ходьба."""

    name_field_speed = NameSpeedEnum.WALK


class RunAction(MovementAction):
    """Бег."""

    name_field_speed = NameSpeedEnum.RUN
