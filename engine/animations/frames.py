from typing import Callable, TYPE_CHECKING, Optional, Self

from pygame import transform, Surface, mask, Mask, image

from engine.constants import Size, Coordinate
from engine.animations.constants import Flip, ScaleRect, ScaleImage
from engine.constants.direction import DirectionGroupEnum
from engine.settings import Settings
from engine.cache import Cache
from engine.animations.constants import EMPTY_SURFACE

if TYPE_CHECKING:
    from engine.objects import Object


class Frame:
    """Класс представляющий базовый кадр.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        _cache: (Cache): кэш.
        _map_flip_by_derection: (dict[DirectionGroupEnum | None, Callable]):
            словарь - направления и функция переворота изображения.
    """

    _settings: Settings = Settings()
    _cache: Cache = Cache()
    _map_flip_by_derection: dict[DirectionGroupEnum | None, Callable] = {
        None: lambda self: self._image,
        DirectionGroupEnum.RIGHT: lambda self: self._image,
        DirectionGroupEnum.UP: lambda self: self._image,
        DirectionGroupEnum.LEFT: lambda self: self._cache.get(
            (self._path_image, self._flip.x, self._flip.y, *self._scale_image, True, False),
            transform.flip,
            self._image,
            True,
            False,
        ),
        DirectionGroupEnum.DOWN: lambda self: self._cache.get(
            (self._path_image, self._flip.x, self._flip.y, *self._scale_image, False, True),
            transform.flip,
            self._image,
            False,
            True,
        ),
    }

    def __init__(
        self,
        flip: Flip,
        scale_rect: ScaleRect,
        scale_image: ScaleImage,
        path_image: str | None = None,
        obj: Optional['Object'] = None,
    ) -> None:
        """Инициализация кадра.

        Args:
            path_image (str | None, optional): путь до изображения кадра анимации. По дефолту None.
            flip (Flip):
                Флаги отражения по вертикале, горизонтале и по направлению движения.
            scale_rect (ScaleRect): scale rect.
            scale_image (ScaleImage): scale image.
            obj (Optional['Object'], optional): игровой объект. По дефолту None.
        """
        self._flip = flip
        self._path_image = path_image
        self._scale_rect = scale_rect
        self._scale_image = scale_image
        self._obj = obj

    def _get_image(self) -> Surface:
        """Отдаёт изображение кадра.

        Returns:
            Surface: изображение кадра.
        """
        if self._path_image is None:
            return EMPTY_SURFACE
        return self._cache.get((self._path_image,), image.load, self._path_image, callback='convert_alpha')

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
        image = self._cache.get(
            (self._path_image, self._flip.x, self._flip.y),
            transform.flip,
            self._get_image(),
            self._flip.x,
            self._flip.y,
        )
        rect = image.get_frect()
        scale = Size(rect.width * self._scale_image.width, rect.height * self._scale_image.height)
        self._image = self._cache.get(
            (self._path_image, self._flip.x, self._flip.y, *self._scale_image),
            transform.scale,
            image,
            scale,
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
        return self._map_flip_by_derection[self._obj.direction if self._flip.direction else None](self)

    def __deepcopy__(self, memo: dict) -> 'Frame':
        """Копирует frame.

        Returns:
            BaseFrame: копия frame.
        """
        return self.__class__(
            self._flip,
            self._scale_rect,
            self._scale_image,
            self._path_image,
            memo.get('obj', self._obj),
        ).after_init()
