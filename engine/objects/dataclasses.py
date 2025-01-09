from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import mouse

if TYPE_CHECKING:
    from engine.objects import Object


@dataclass
class Speed:
    """Dataclass скорости динамического объекта.

    Attributes:
        walk (int, optional): скорость ходьбы. По дефолту 0.
        run (int, optional): скорость бега. По дефолту 0.
        squat (int, optional): скорость в присяде. По дефолту 0.
        fall (int, optional): скорость падения. По дефолту 0.
        jump (int, optional): скорость прыжка. По дефолту 0.
        double_jump (int, optional): скорость двойного прыжка. По дефолту 0.
        walk_boost (int, optional): ускорение ходьбы. По дефолту 0.
        run_boost (int, optional): ускорение бега. По дефолту 0.
        squat_boost (int, optional): ускорение в присяде. По дефолту 0.
        fall_boost (int, optional): ускорение падения. По дефолту 0.
        jump_boost (int, optional): ускорение прыжка. По дефолту 0.
        double_jump_boostt (int, optional): ускорение двойного прыжка. По дефолту 0.
    """

    walk: int = 0
    run: int = 0
    squat: int = 0
    fall: int = 0
    jump: int = 0
    double_jump: int = 0
    walk_boost: int = 0
    run_boost: int = 0
    squat_boost: int = 0
    fall_boost: int = 0
    jump_boost: int = 0
    double_jump_boost: int = 0


@dataclass
class Status:
    """Cтатусы объекта.

    Attributes:
        obj (Object): игровой объект.
        inactive (bool): статус неактивности.
        focus (bool): статус фокуса.
        jump (bool): статус прыжка.
        double_jump (bool): статус двойного прыжка.
        fall (bool): статус падения.
        hit (bool): статус урона.
        death (bool): статус смерти.
    """

    _obj: 'Object'
    inactive: bool = False
    focus: bool = False

    @property
    def collision_mos(self) -> bool:
        """Флаг коллизии объекта с мышкой.

        Returns:
            bool: флаг коллизии объекта с мышкой.
        """
        pos = mouse.get_pos()
        pos_in_mask = pos[0] - self._obj.rect.x, pos[1] - self._obj.rect.y
        return bool(self._obj.rect.collidepoint(*pos) and self._obj.mask.get_at(pos_in_mask))


@dataclass
class DynamicStatus(Status):
    """Cтатусы динамического объекта объекта.

    Attributes:
        jump (bool): статус прыжка.
        double_jump (bool): статус двойного прыжка.
        fall (bool): статус падения.
        hit (bool): статус урона.
        death (bool): статус смерти.
    """

    jump: bool = False
    double_jump: bool = False
    fall: bool = False
    hit: bool = False
    death: bool = False
