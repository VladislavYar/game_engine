from weakref import WeakValueDictionary
from typing import Tuple


from pygame.sprite import LayeredUpdates
from pygame import image, transform, Surface, FRect

from engine.metaclasses.singleton import SingletonMeta
from engine.objects.base_object import BaseObject
from engine.constants.path import BasePathEnum
from engine.settings import Settings
from engine.cache import Cache
from engine.constants import Size, Coordinate
from engine.objects.backgrounds.constants import Background, CoefShiftRate
from engine.constants.direction import DirectionEnum, OPPOSITE_DIRECTIONS


class BackgroundsGroup(LayeredUpdates, metaclass=SingletonMeta):
    """Группа заднего фона игры со слоями отрисовки.

    Attributes:
        _base_visible_map_size (Size): размер видимой игровой карты.
    """

    _base_visible_map_size: Size = Size(*Settings()['engine']['base_visible_map_size'])
    _half_width: float = _base_visible_map_size.width / 2
    _half_height: float = _base_visible_map_size.height / 2

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
            bottomright = Coordinate(*rect.bottomright)

            if bottomright.x < -self._base_visible_map_size.width:
                sprite.kill()
            elif rect.x > self._base_visible_map_size.width:
                sprite.kill()

            if bottomright.y < -self._base_visible_map_size.height:
                sprite.kill()
            elif rect.y > self._base_visible_map_size.height:
                sprite.kill()

            if rect.collidepoint(self._half_width, self._half_height):
                sprite.create_adjacent_backgrounds()


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
        self.background = background
        self.adjacent_backgrounds = WeakValueDictionary()
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

    def _create_left_right_adjacent_backgrounds(self) -> Tuple['BackgroundsObject', 'BackgroundsObject']:
        """Создаёт левый и правый фоны.

        Returns:
            Tuple[BackgroundsObject, BackgroundsObject]: левый и правый фоны.
        """
        background_left, background_right = (
            self.adjacent_backgrounds.get(DirectionEnum.LEFT),
            self.adjacent_backgrounds.get(DirectionEnum.RIGHT),
        )
        if not background_left:
            background_left = BackgroundsObject(self.background, self.new_layer)
            self.adjacent_backgrounds[DirectionEnum.LEFT] = background_left
            background_left.rect.topright = self.rect.topleft
            background_left.adjacent_backgrounds[OPPOSITE_DIRECTIONS[DirectionEnum.LEFT]] = self
        if not background_right:
            background_right = BackgroundsObject(self.background, self.new_layer)
            self.adjacent_backgrounds[DirectionEnum.RIGHT] = background_right
            background_right.rect.topleft = self.rect.topright
            background_right.adjacent_backgrounds[OPPOSITE_DIRECTIONS[DirectionEnum.RIGHT]] = self
        return background_left, background_right

    def _create_up_down_adjacent_backgrounds(self) -> Tuple['BackgroundsObject', 'BackgroundsObject']:
        """Создаёт верхний и нижний фоны.

        Returns:
            Tuple[BackgroundsObject, BackgroundsObject]: верхний и нижний фоны.
        """
        background_up, background_down = (
            self.adjacent_backgrounds.get(DirectionEnum.UP),
            self.adjacent_backgrounds.get(DirectionEnum.DOWN),
        )
        if not background_up:
            background_up = BackgroundsObject(self.background, self.new_layer)
            self.adjacent_backgrounds[DirectionEnum.UP] = background_up
            background_up.rect.bottomleft = self.rect.topleft
            background_up.adjacent_backgrounds[OPPOSITE_DIRECTIONS[DirectionEnum.UP]] = self
        if not background_down:
            background_down = BackgroundsObject(self.background, self.new_layer)
            self.adjacent_backgrounds[DirectionEnum.DOWN] = background_down
            background_down.rect.topleft = self.rect.bottomleft
            background_down.adjacent_backgrounds[OPPOSITE_DIRECTIONS[DirectionEnum.DOWN]] = self
        return background_up, background_down

    def create_adjacent_backgrounds(self) -> None:
        """Создаёт соседние фоны."""
        background_up, background_down = self._create_up_down_adjacent_backgrounds()
        background_left, background_right = self._create_left_right_adjacent_backgrounds()
        background_up_left, background_up_right = background_up._create_left_right_adjacent_backgrounds()
        background_down_left, background_down_right = background_down._create_left_right_adjacent_backgrounds()
        background_left.adjacent_backgrounds[DirectionEnum.UP] = background_up_left
        background_left.adjacent_backgrounds[DirectionEnum.DOWN] = background_down_left
        background_right.adjacent_backgrounds[DirectionEnum.UP] = background_up_right
        background_right.adjacent_backgrounds[DirectionEnum.DOWN] = background_down_right


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
