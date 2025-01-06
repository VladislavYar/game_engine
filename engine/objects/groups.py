from typing import TYPE_CHECKING, Optional

from pygame.sprite import Group, collide_mask
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
    """

    _settings: Settings = Settings()

    def collide_side_rect_with_mask(
        self,
        obj: 'Object',
        side: DirectionGroupEnum,
    ) -> Optional[tuple['Object', Coordinate]]:
        """Проверяет коллизию rect объекта с масками группы объектов с определённой стороны.

        Args:
            obj (Object): объект для проверки коллизии.
            side (DirectionGroupEnum): сторона для проверки.

        Returns:
            Optional[tuple[Object, Coordinate]]: координаты коллизии и объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if coordinate := obj.collide_side_rect_with_mask(sprite, side):
                return sprite, coordinate

    def collide_side_mask(
        self,
        obj: 'Object',
        side: DirectionGroupEnum,
    ) -> Optional[tuple['Object', Coordinate]]:
        """Проверяет коллизию по маске с группой объектов с определённой стороны.

        Args:
            obj (Object): объект для проверки коллизии.
            side (DirectionGroupEnum): сторона для проверки.

        Returns:
            Optional[tuple[Object, Coordinate]]: координаты коллизии и объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if coordinate := obj.collide_side_mask(sprite, side):
                return sprite, coordinate

    def collide_mask(self, obj: 'Object') -> Optional[tuple['Object', Coordinate]]:
        """Проверяет коллизию по маске с группой объектов.

        Args:
            obj (Object): объект для проверки коллизии.

        Returns:
            Optional[tuple[Object, Coordinate]]: координаты коллизии и объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if not obj.rect.colliderect(sprite.rect):
                continue
            if coordinate := collide_mask(obj, sprite):
                return sprite, Coordinate(*coordinate)

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
        if not self._settings['engine']['debug_mode']:
            return
        for sprite in self.sprites():
            draw.rect(
                surface,
                Color(*self._settings['engine']['rect_outline']['rect_outline_color']),
                sprite.rect,
                width=self._settings['engine']['rect_outline']['rect_outline_width'],
            )

    def draw(self, surface: Surface, *arg, **kwarg) -> list['Object']:
        """Добавляет обводку спрайтам при отладке."""
        self._debug_mode(surface)
        return super().draw(surface, *arg, **kwarg)

    def move(self, dx: float = 0, dy: float = 0) -> None:
        """Перемещение спрайтов..

        Args:
            dx (float, optional): перемещение по x. По дефолту 0.
            dy (float, optional): перемещение по y. По дефолту 0.
        """
        for sprite in self.sprites():
            rect = sprite.rect
            rect.x += dx
            rect.y += dy


class AllObjectsGroup(BaseGroup):
    """Группа всех объектов."""


class TextObjectsGroup(BaseGroup):
    """Группа текстов."""


class SolidObjectsGroup(BaseGroup):
    """Группа твёрдых объектов."""


class DynamicObjectsGroup(BaseGroup):
    """Группа динамических объектов."""
