from typing import Iterable

from engine.objects import Object
from engine.objects.groups import BaseGroup
from engine.metaclasses.singleton import SingletonMeta
from engine.settings import Settings
from engine.constants import Size, Coordinate
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
        settings: Settings = Settings()
        self._tile_grid: TileGrid = TileGrid()
        self._smoothness: float = settings['engine']['camera']['camera_smoothness']
        base_visible_map_size: Size = Size(*settings['engine']['base_visible_map_size'])
        self._dead_zone: Size = Size(*settings['engine']['camera']['dead_zone'])
        self._half_width: float = base_visible_map_size.width / 2
        self._half_height: float = base_visible_map_size.height / 2
        move = self._get_move()
        self._move(move)

    def _get_move(self) -> Coordinate:
        """Отдаёт перемещение по осям x, y.

        Returns:
            move (Coordinate): перемещение по осям x, y.
        """
        move_x = self._half_width - self.obj.rect.x
        move_y = self._half_height - self.obj.rect.y
        coordinate = Coordinate(
            0 if abs(move_x) <= self._dead_zone.width else move_x,
            0 if abs(move_y) <= self._dead_zone.height else move_y,
        )
        return coordinate

    def _move(self, move: Coordinate) -> None:
        """Перемещение камеры.

        Args:
            move (Coordinate): перемещение по осям x, y.
        """
        self._tile_grid.move(move)
        for group in self._groups_shift:
            group.move(move)

    def update(self) -> None:
        """Обновление камеры."""
        move = self._get_move()
        move = Coordinate(move.x * self._smoothness, move.y * self._smoothness)
        self._move(move)
