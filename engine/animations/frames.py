from functools import lru_cache
from typing import Callable

from pygame import transform, Surface, mask

from engine.constants import Size
from engine.constants.direction import DirectionGroupEnum
from engine.settings import Settings


class BaseFrame:
    """Класс представляющий базовый кадр.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        _map_flip_by_derection: (dict[DirectionGroupEnum | None, Callable]):
            словарь - направления и функция переворота изображения.
    """

    _settings: Settings = Settings()
    _map_flip_by_derection: dict[DirectionGroupEnum | None, Callable] = {
        None: lambda image: image,
        DirectionGroupEnum.RIGHT: lambda image: image,
        DirectionGroupEnum.UP: lambda image: image,
        DirectionGroupEnum.LEFT: lambda image: transform.flip(image, True, False),
        DirectionGroupEnum.DOWN: lambda image: transform.flip(image, False, True),
    }

    def __init__(self, image: Surface) -> None:
        """Инициализация базового кадра.

        Args:
            image (Surface): изображение кадра анимации.
        """
        self._set_data_frame(image)
        self._original_image = image
        self._original_size = Size(self.rect.size[0], self.rect.size[1])
        self.direction = None
        self.scale()

    def _set_data_frame(self, image: Surface) -> None:
        """Устанавливает данные по кадру анимации.

        Args:
            image (Surface): изображение кадра анимации.
        """
        self._image = image
        self.rect = image.get_frect()
        self.mask = mask.from_surface(image)

    def scale(self) -> None:
        """Изменяет размер кадра анимации под текущий размер экрана."""

    @property
    def image(self) -> Surface:
        """Getter изображения.

        Returns:
            Surface: изображение.
        """
        return self._map_flip_by_derection[self.direction](self._image)

    def __deepcopy__(self, *arg, **kwarg) -> 'BaseFrame':
        """Копирует frame.

        Returns:
            BaseFrame: копия frame.
        """
        return self.__class__(self._original_image.copy())


class EmptyFrame(BaseFrame):
    """Класс представляющий пустой кадр."""


class Frame(BaseFrame):
    """Класс представляющий кадр анимации.

    Attributes:
        base_screen_size Size: базовый размер экрана для вычисления размера кадра.
        base_visible_map_size (Size): базовый размер видимой карты.
    """

    base_screen_size: Size = Size(*BaseFrame._settings['engine']['base_screen_size_frame'])
    base_visible_map_size: Size = Size(*BaseFrame._settings['engine']['base_visible_map_size'])

    @classmethod
    @lru_cache
    def _get_coef(cls, width: int, height: int) -> tuple[float, float]:
        """Отдаёт коэффициент разности разрешения экрана от базового.

        Args:
            width (int): ширина разрешения экрана.
            height (int): высота разрешения экрана.
        Returns:
            tuple[float, float]: коэффициент разности разрешения экрана от базового.
        """
        return width / cls.base_screen_size.width, height / cls.base_screen_size.height

    def scale(self) -> None:
        """Изменяет размер кадра анимации под текущий размер видимой карты."""
        coef_width, coef_height = self._get_coef(*self.base_visible_map_size)
        size = Size(self._original_size.width * coef_width, self._original_size.height * coef_height)
        self._set_data_frame(transform.scale(self._original_image.copy(), size))
