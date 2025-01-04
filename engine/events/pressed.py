from typing import Callable, TYPE_CHECKING

from pygame import key

from engine.metaclasses.singleton import PressedSingletonMeta
from engine.events.constants import EventEnum
from engine.constants import WRITING_ONLY

if TYPE_CHECKING:
    from engine.objects.dataclasses import Status


class Pressed(metaclass=PressedSingletonMeta):
    """Класс проверки зажатия клавиш, коллизии мыши и активности объекта.

    Attributes:
        _pressed (key.ScancodeWrapper): кортеж состояний кнопок.
        _map_status_events: (dict[int, Callable]): словарь событие - функция получения статуса.
    """

    _pressed: key.ScancodeWrapper
    _map_get_status_events: dict[int, Callable] = {
        EventEnum.COLLISION_MOS_EVENT: lambda status: getattr(status, 'collision_mos'),
        EventEnum.INACTIVE_EVENT: lambda status: getattr(status, 'inactive'),
        EventEnum.FOCUS_EVENT: lambda status: getattr(status, 'focus'),
        EventEnum.JUMP_EVENT: lambda status: getattr(status, 'jump'),
        EventEnum.DOUBLE_JUMP_EVENT: lambda status: getattr(status, 'double_jump'),
        EventEnum.FALL_EVENT: lambda status: getattr(status, 'fall'),
        EventEnum.HIT_EVENT: lambda status: getattr(status, 'hit'),
        EventEnum.DEATH_EVENT: lambda status: getattr(status, 'death'),
    }

    @property
    def status(self) -> 'Status':
        raise WRITING_ONLY

    @status.setter
    def status(self, value: 'Status') -> None:
        """Setter статуса игрового объекта.

        Args:
            value (Status): статус игрового объекта.
        """
        self._status = value

    def __getitem__(self, key: int) -> bool:
        """Отдаёт флаг состояние события.

        Args:
            key (int): событие.

        Returns:
            bool: флаг события.
        """
        return self._map_get_status_events.get(key, lambda _: self._pressed[key])(self._status)
