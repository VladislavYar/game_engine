from typing import TYPE_CHECKING, Callable

from pygame import key, mouse

from engine.metaclasses.singleton import PressedSingletonMeta
from engine.events.constants import EventEnum

if TYPE_CHECKING:
    from engine.objects import BaseObject


class Pressed(metaclass=PressedSingletonMeta):
    """Класс проверки зажатия клавиш, коллизии мыши и активности объекта.

    Attributes:
        _pressed (key.ScancodeWrapper): кортеж состояний кнопок.
        _inactive (bool): флаг неактивности объекта.
        _focus (bool): флаг фокуса на объекте.
        _collision_mos (bool): флаг коллизии мыши с объектом.
        _map_get_status_events: (dict[int, Callable]): словарь событие - функция его получения.
    """

    _pressed: key.ScancodeWrapper
    _inactive: bool
    _focus: bool
    _collision_mos: bool
    _map_get_status_events: dict[int, Callable] = {
        EventEnum.COLLISION_MOS_EVENT: lambda self: getattr(self, '_collision_mos'),
        EventEnum.INACTIVE_EVENT: lambda self: getattr(self, '_inactive'),
        EventEnum.FOCUS_EVENT: lambda self: getattr(self, '_focus'),
    }

    def __call__(self, obj: 'BaseObject') -> None:
        """Актуализирует pressed с учётом игрового объекта.

        Args:
            obj (BaseObject): игровой объект.
        """
        self._collision_mos = self._check_collision_mos(obj)
        self._inactive = obj.status.inactive
        self._focus = obj.status.focus

    def _check_collision_mos(self, obj: 'BaseObject') -> bool:
        """Проверка коллизии мышки с маской.

        Returns:
            bool: флаг коллизии мышки с маской.
        """
        pos = mouse.get_pos()
        pos_in_mask = pos[0] - obj.rect.x, pos[1] - obj.rect.y
        return bool(obj.rect.collidepoint(*pos) and obj.mask.get_at(pos_in_mask))

    def __getitem__(self, key: int) -> bool:
        """Отдаёт флаг состояние события.

        Args:
            key (int): событие.

        Returns:
            bool: флаг события.
        """
        return self._map_get_status_events.get(key, lambda self: self._pressed[key])(self)
