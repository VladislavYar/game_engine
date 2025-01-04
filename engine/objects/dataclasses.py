from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import mouse

if TYPE_CHECKING:
    from engine.objects import BaseObject


@dataclass
class Speed:
    """Dataclass скорости динамического объекта.

    Attributes:
        walk (int, optional): скорость ходьбы. По дефолту 0.
        run (int, optional): скорость бега. По дефолту 0.
        squat (int, optional): скорость в присяде. По дефолту 0.
        fall (int, optional): скорость падения. По дефолту 0.
    """

    walk: int = 0
    run: int = 0
    squat: int = 0
    fall: int = 0


@dataclass
class Status:
    """Cтатусы объекта.

    Attributes:
        obj (BaseObject): игровой объект.
        inactive (bool): статус неактивности.
        focus (bool): статус фокуса.
        jump (bool): статус прыжка.
        double_jump (bool): статус двойного прыжка.
        fall (bool): статус падения.
        hit (bool): статус урона.
        death (bool): статус смерти.
    """

    _obj: 'BaseObject'
    inactive: bool = False
    focus: bool = False
    jump: bool = False
    double_jump: bool = False
    fall: bool = False
    hit: bool = False
    death: bool = False

    @property
    def collision_mos(self) -> bool:
        """Флаг коллизии объекта с мышкой.

        Returns:
            bool: флаг коллизии объекта с мышкой.
        """
        pos = mouse.get_pos()
        pos_in_mask = pos[0] - self._obj.rect.x, pos[1] - self._obj.rect.y
        return bool(self._obj.rect.collidepoint(*pos) and self._obj.mask.get_at(pos_in_mask))
