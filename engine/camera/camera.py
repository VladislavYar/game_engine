from typing import Iterable

from engine.objects import Object
from engine.objects.groups import BaseGroup
from engine.metaclasses.singleton import SingletonMeta
from engine.settings import Settings
from engine.constants import Size
from engine.tile_grid import TileGrid


class Camera(metaclass=SingletonMeta):
    """Класс камеры."""

    def __init__(self, obj: Object, groups_shift: Iterable[BaseGroup]) -> None:
        """Инициализация камеры.

        Args:
            obj (Object): объект для отслеживания.
            groups_shift (Iterable[BaseGroup]): группы для сдвига.
        """
        self.obj = obj
        self._groups_shift = groups_shift
        self._settings: Settings = Settings()
        self._tile_grid: TileGrid = TileGrid()
        self._base_visible_map_size: Size = Size(*self._settings['engine']['base_visible_map_size'])
        self._half_width: float = self._base_visible_map_size.width / 2
        self._half_height: float = self._base_visible_map_size.height / 2

    def _debug_mode(self, move_x: float, move_y: float) -> None:
        """Debug mode.

        Args:
            move_x (float): перемещение по x.
            move_y (float): перемещение по y.
        """
        if not self._settings['engine']['debug_mode']:
            return
        self._tile_grid.rect.x += move_x
        self._tile_grid.rect.y += move_y

    def update(self) -> None:
        """Обновление камеры."""
        move_x = self._half_width - self.obj.rect.x
        move_y = self._half_height - self.obj.rect.y
        self._debug_mode(move_x, move_y)
        for group in self._groups_shift:
            group.move(move_x, move_y)
