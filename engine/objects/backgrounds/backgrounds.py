from pygame.sprite import LayeredUpdates
from pygame import image, transform, Surface, FRect

from engine.metaclasses.singleton import SingletonMeta
from engine.objects.base_object import BaseObject
from engine.constants.path import BasePathEnum
from engine.settings import Settings
from engine.cache import Cache
from engine.constants import Size, Coordinate
from engine.objects.backgrounds.constants import Background, CoefShiftRate


class BackgroundsGroup(LayeredUpdates, metaclass=SingletonMeta):
    """Группа заднего фона игры со слоями отрисовки.

    Attributes:
        _base_visible_map_size (Size): размер видимой игровой карты.
    """

    _base_visible_map_size: Size = Size(*Settings()['engine']['base_visible_map_size'])

    def move(self, move: Coordinate) -> None:
        """Перемещение спрайтов.

        Args:
            move (Coordinate): перемещение по осям x, y.
        """
        for sprite in self.sprites():
            rect: FRect = sprite.rect
            coef_shift_rate: CoefShiftRate = sprite.coef_shift_rate
            rect.x += move.x * coef_shift_rate.x
            rect.y += move.y * coef_shift_rate.y
            bottomright = list(rect.bottomright)
            if rect.y > 0:
                rect.y = 0
            elif bottomright[1] < self._base_visible_map_size.height:
                bottomright[1] = self._base_visible_map_size.height
                rect.bottomright = bottomright
            if rect.x > 0:
                rect.x = 0
            elif bottomright[0] < self._base_visible_map_size.width:
                bottomright[0] = self._base_visible_map_size.width
                rect.bottomright = bottomright


class BackgroundsObject(BaseObject):
    """Объект заднего плана.

    Attributes:
        _base_visible_map_size (Size): размер видимой игровой карты.
        _cache: (Cache): кэш.
    """

    _base_visible_map_size: Size = Size(*Settings()['engine']['base_visible_map_size'])
    _cache: Cache = Cache()
    groups: tuple[BackgroundsGroup] = (BackgroundsGroup(),)

    def __init__(self, background: Background, layer: int = 0) -> None:
        """Инициализация объекта заднего плана.

        Args:
            background (Background): данные по заднему плану.
            layer (int, optional): Слой отрисовки. По дефолту 0.
        """
        super().__init__()
        path_image = BasePathEnum.BACKGROUNDS_PATH.value / background.path_image
        self.new_layer = layer
        self.coef_shift_rate: CoefShiftRate = background.coef_shift_rate
        self.image = self._cache.get((path_image,), image.load, path_image, callback='convert_alpha')
        self.rect = self.image.get_frect()
        scale_height = self._base_visible_map_size.height / self.rect.height * background.scale.height
        scale_width = self._base_visible_map_size.width / self.rect.width * background.scale.width
        scale = Size(self.rect.width * scale_width, self.rect.height * scale_height)
        self.image = self._cache.get(
            (path_image, scale),
            transform.scale,
            self.image,
            scale,
        )
        self.rect = self.image.get_frect()


class BackgroundsSurface:
    """Отображение заднего плана.

    Attributes:
        _base_visible_map_size (Size): размер видимой игровой карты.
        _backgrounds_group (BackgroundsGroup): группа заднего плана.
    """

    _base_visible_map_size: Size = Size(*Settings()['engine']['base_visible_map_size'])
    _backgrounds_group: BackgroundsGroup = BackgroundsGroup()

    def __init__(self, *args: Background) -> None:
        """Инициализация заднего плана."""
        for layer, background in enumerate(args):
            BackgroundsObject(background, layer)
        self.image = Surface(self._base_visible_map_size)
        self.rect = self.image.get_frect()
        self._backgrounds_group.draw(self.image)

    def draw(self, surface: Surface) -> None:
        """Отрисовывает задний план.

        Args:
            surface (Surface): отображение для отрисовки заднего плана.
        """
        surface.blit(self.image, self.rect)

    def move(self, move: Coordinate) -> None:
        pass
