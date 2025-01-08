from typing import TYPE_CHECKING, Optional

from pygame.sprite import Group
from pygame import Surface, draw

from engine.events import Pressed
from engine.metaclasses.singleton import SingletonMeta
from engine.constants.direction import DirectionGroupEnum
from engine.settings import Settings
from engine.constants import Color, Coordinate

if TYPE_CHECKING:
    from engine.objects import Object


class BaseGroup(Group, metaclass=SingletonMeta):
    """Базовая группа объектов. Расширяет стандартный класс группы спрайтов.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        _debug (bool): флаг debug-a.
    """

    _settings: Settings = Settings()
    _debug: bool = _settings['engine']['debug']['debug_mode']

    def collide_rect_with_mask(
        self,
        obj: 'Object',
        side: DirectionGroupEnum | None = None,
    ) -> Optional[tuple['Object', Coordinate]]:
        """Проверяет коллизию rect объекта с масками группы объектов.

        Args:
            obj (Object): объект для проверки коллизии.
            side (DirectionGroupEnum | None, optional): сторона для проверки. По дефолту None.

        Returns:
            Optional[tuple[Object, Coordinate]]: координаты коллизии и объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if coordinate := obj.collide_rect_with_mask(sprite, side):
                return sprite, coordinate

    def collide_mask(
        self,
        obj: 'Object',
        side: DirectionGroupEnum | None = None,
    ) -> Optional[tuple['Object', Coordinate]]:
        """Проверяет коллизию по маске с группой объектов.

        Args:
            obj (Object): объект для проверки коллизии.
            side (DirectionGroupEnum | None, optional): сторона для проверки. По дефолту None.

        Returns:
            Optional[tuple[Object, Coordinate]]: координаты коллизии и объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if coordinate := obj.collide_mask(sprite, side):
                return sprite, coordinate

    def events(self, *args, **kwargs) -> None:
        """Запускает у объектов проверку событий."""
        pressed = Pressed()
        for sprite in self.sprites():
            sprite.events(pressed=pressed, *args, **kwargs)

    def _debug_mode(self, surface: Surface) -> None:
        """Debug mode

        Args:
            surface (Surface): отображение.
        """
        if not self._debug:
            return
        for sprite in self.sprites():
            draw.rect(
                surface,
                Color(*self._settings['engine']['rect_outline']['rect_outline_color']),
                sprite.rect,
                width=self._settings['engine']['rect_outline']['rect_outline_width'],
            )

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        """Добавляет обводку спрайтам при отладке и меняет логину отрисовки."""
        self._debug_mode(surface)
        sprites = self.sprites()
        self.spritedict.update(
            zip(
                sprites,
                surface.blits(
                    (spr.image, (spr.rect.x - spr.coordinate_shift.x, spr.rect.y - spr.coordinate_shift.y))
                    for spr in sprites
                ),
            )
        )

    def move(self, move: Coordinate) -> None:
        """Перемещение спрайтов..

        Args:
            move (Coordinate): перемещение по осям x, y.
        """
        for sprite in self.sprites():
            rect = sprite.rect
            rect.x += move.x
            rect.y += move.y


class AllObjectsGroup(BaseGroup):
    """Группа всех объектов."""


class TextObjectsGroup(BaseGroup):
    """Группа текстов."""


class SolidObjectsGroup(BaseGroup):
    """Группа твёрдых объектов."""


class DynamicObjectsGroup(BaseGroup):
    """Группа динамических объектов."""
