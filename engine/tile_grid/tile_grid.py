from pygame import FRect, Surface, draw

from engine.metaclasses.singleton import SingletonMeta
from engine.settings import Settings
from engine.constants import Size, Coordinate, Color, ZERO_COORDINATES
from engine.constants.empty import EMPTY_FRAME
from engine.tile_grid.constants import POSITION_RECT_INNER_OUTLINE, SHIFT_NUMBER_POSITION_BY_X
from engine.objects.text import Text


class Tile:
    """Класс тайтла.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        _size (Size): размер тайтла.
    """

    _settings: Settings = Settings()
    _size: Size = Size(*_settings['engine']['tile_grid']['tile_size'])

    def __init__(self, row: int, column: int) -> None:
        """Инициализация тайтла.

        Args:
            row (int): строка тайтла.
            column (int): столбец тайтла.
        """
        left = column * self._size.width
        top = row * self._size.height
        self.rect = FRect(Coordinate(left, top), self._size)


class TileGrid(metaclass=SingletonMeta):
    """Класс сетки тайлов."""

    def __init__(self) -> None:
        """Инициализация игровой сетки."""
        self._settings = Settings()
        self._tile_grid: tuple[tuple[Tile]] = tuple(
            tuple(Tile(row, column) for column in range(self._settings['engine']['tile_grid']['rows']))
            for row in range(self._settings['engine']['tile_grid']['columns'])
        )
        self.rect = EMPTY_FRAME.rect
        self._debug = self._settings['engine']['debug']['debug_mode']
        self._debug_mode()

    def __getitem__(self, index: int) -> tuple[Tile]:
        """Отдаёт строку по индексу.

        Args:
            index (int): индекс строки.

        Returns:
            tuple[Tile]: строка.
        """
        return self._tile_grid[index]

    def __len__(self) -> int:
        """Отдаёт количество строк."""
        return len(self._tile_grid)

    def _create_surface(self) -> None:
        """Создаёт surface сетки."""
        tile_size = Size(*self._settings['engine']['tile_grid']['tile_size'])
        self.surface = Surface(
            Size(
                self._settings['engine']['tile_grid']['columns'] * tile_size.width,
                self._settings['engine']['tile_grid']['rows'] * tile_size.height,
            )
        )
        self.rect = self.surface.get_frect()
        self.rect.center = Coordinate(self.rect.width / 2, self.rect.height / 2)

    def _get_data_draw_tile(self) -> tuple[FRect, Color, int, Color, int]:
        """Отдаёт данные для вывода тайтлов.

        Returns:
            tuple[Size, Color, int, Color, int]: данные для вывода тайтлов.
        """
        tile_size = Size(*self._settings['engine']['tile_grid']['tile_size'])
        rect = FRect(ZERO_COORDINATES, Size(tile_size.width / 2, tile_size.height / 2))
        rect_inner_outline_color = Color(*self._settings['engine']['tile_grid']['rect_inner_outline_color'])
        rect_inner_outline_width = self._settings['engine']['tile_grid']['rect_inner_outline_width']
        rect_outline_color = Color(*self._settings['engine']['tile_grid']['rect_outline_color'])
        rect_outline_width = self._settings['engine']['tile_grid']['rect_outline_width']
        return rect, rect_inner_outline_color, rect_inner_outline_width, rect_outline_color, rect_outline_width

    def _draw_tile(self) -> None:
        """Выводит тайтлый на surface сетки."""
        rect, rect_inner_outline_color, rect_inner_outline_width, rect_outline_color, rect_outline_width = (
            self._get_data_draw_tile()
        )
        number_row = Text()
        number_column = Text()
        for i, row in enumerate(self._tile_grid):
            number_row.text = f'{i}'
            for j, tile in enumerate(row):
                number_column.text = f'{j}'
                for position in POSITION_RECT_INNER_OUTLINE:
                    setattr(rect, position, Coordinate(*getattr(tile.rect, position)))
                    draw.rect(self.surface, rect_inner_outline_color, rect, rect_inner_outline_width)
                number_row.rect.topleft = tile.rect.topleft
                number_column.rect.bottomleft = tile.rect.bottomleft
                number_row.rect.x += SHIFT_NUMBER_POSITION_BY_X
                number_column.rect.x += SHIFT_NUMBER_POSITION_BY_X
                self.surface.blits(((number_row.text, number_row), (number_column.text, number_column.rect)))
                draw.rect(self.surface, rect_outline_color, tile.rect, rect_outline_width)

    def _debug_mode(self) -> None:
        """Debug mode."""
        if not self._debug:
            return
        self._create_surface()
        self._draw_tile()

    def move(self, move: Coordinate) -> None:
        """Перемещение сетки тайтлов.

        Args:
            move (Coordinate): перемещение по осям x, y.
        """
        self.rect.x += move.x
        self.rect.y += move.y
        for column in self._tile_grid:
            for tile in column:
                tile.rect.x += move.x
                tile.rect.y += move.y
