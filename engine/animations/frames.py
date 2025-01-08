from typing import Callable, TYPE_CHECKING, Optional, Self

from pygame import transform, Surface, mask, Mask

from engine.constants import Size, Coordinate
from engine.animations.constants import Flip, ScaleRect, ScaleImage
from engine.constants.direction import DirectionGroupEnum
from engine.settings import Settings

if TYPE_CHECKING:
    from engine.objects import Object


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

    def __init__(
        self,
        image: Surface,
        flip: Flip,
        scale_rect: ScaleRect,
        scale_image: ScaleImage,
        obj: Optional['Object'] = None,
    ) -> None:
        """Инициализация базового кадра.

        Args:
            image (Surface): изображение кадра анимации.
            flip (Flip):
                Флаги отражения по вертикале, горизонтале и по направлению движения.
            scale_rect (ScaleRect): scale rect.
            scale_image (ScaleImage): scale image.
            obj (Optional['Object'], optional): игровой объект. По дефолту None.
        """
        self._flip = flip
        self._image = image
        self._scale_rect = scale_rect
        self._scale_image = scale_image
        self._obj = obj

    def after_init(self) -> Self:
        """Инициализация frame после основной инициализации.

        Returns:
            Self: возвращает ссылку на себя же.
        """
        self._transform_image()
        self._set_data_frame()
        return self

    def _transform_image(self) -> None:
        """Преобразует изображение кадра анимации."""
        image = transform.flip(self._image, self._flip.x, self._flip.y)
        rect = image.get_frect()
        self._image = transform.scale(
            image, Size(rect.width * self._scale_image.width, rect.height * self._scale_image.height)
        )

    def _set_data_frame(self) -> None:
        """Устанавливает данные по кадру анимации."""
        self.rect = self._image.get_frect()
        original_width = self.rect.width
        original_height = self.rect.height
        self.rect.width *= self._scale_rect.width
        self.rect.height *= self._scale_rect.height
        self.coordinate_shift = Coordinate(
            (original_width - self.rect.width) / 2, (original_height - self.rect.height) / 2
        )
        self.mask = mask.from_surface(self._image)
        self.rect_mask = Mask((self.rect.width, self.rect.height))
        self.rect_mask.fill()

    @property
    def image(self) -> Surface:
        """Getter изображения.

        Returns:
            Surface: изображение.
        """
        return self._map_flip_by_derection[self._obj.direction if self._flip.direction else None](self._image)

    def __deepcopy__(self, memo: dict) -> 'BaseFrame':
        """Копирует frame.

        Returns:
            BaseFrame: копия frame.
        """
        return self.__class__(
            self._image,
            self._flip,
            self._scale_rect,
            self._scale_image,
            memo.get('obj', self._obj),
        ).after_init()


class EmptyFrame(BaseFrame):
    """Класс представляющий пустой кадр."""


class Frame(BaseFrame):
    """Класс представляющий кадр анимации."""
