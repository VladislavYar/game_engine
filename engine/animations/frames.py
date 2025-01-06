from typing import Callable

from pygame import transform, Surface, mask, Mask

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
        self._original_size = Size(self.rect.width, self.rect.height)
        self.direction = None

    def _set_data_frame(self, image: Surface) -> None:
        """Устанавливает данные по кадру анимации.

        Args:
            image (Surface): изображение кадра анимации.
        """
        self._image = image
        self.rect = image.get_frect()
        self.mask = mask.from_surface(image)
        self.rect_mask = Mask((self.rect.width, self.rect.height))
        self.rect_mask.fill()

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
    """Класс представляющий кадр анимации."""
