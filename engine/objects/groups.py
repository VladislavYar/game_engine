from typing import TYPE_CHECKING, Optional

from pygame.sprite import Group, collide_mask
from pygame import Surface, draw

from engine.events import Pressed
from engine.metaclasses.singleton import SingletonMeta
from engine.constants.direction import DirectionGroupEnum
from engine.settings import Settings
from engine.constants import Color

if TYPE_CHECKING:
    from engine.objects import BaseObject


class BaseGroup(Group, metaclass=SingletonMeta):
    """Базовая группа объектов. Расширяет стандартный класс группы спрайтов.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
    """

    _settings: Settings = Settings()

    def collide_side_rect_with_mask(self, obj: 'BaseObject', side: DirectionGroupEnum) -> Optional['BaseObject']:
        """Проверяет коллизию rect объекта с масками группы объектов с определённой стороны.

        Args:
            obj (BaseObject): объект для проверки коллизии.
            side (DirectionGroupEnum): сторона для проверки.

        Returns:
            Optional[BaseObject]: объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if obj.collide_side_rect_with_mask(sprite, side):
                return sprite

    def collide_side_mask(self, obj: 'BaseObject', side: DirectionGroupEnum) -> Optional['BaseObject']:
        """Проверяет коллизию по маске с группой объектов с определённой стороны.

        Args:
            obj (BaseObject): объект для проверки коллизии.
            side (DirectionGroupEnum): сторона для проверки.

        Returns:
            Optional[BaseObject]: объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if obj.collide_side_mask(sprite, side):
                return sprite

    def collide_mask(self, obj: 'BaseObject') -> Optional['BaseObject']:
        """Проверяет коллизию по маске с группой объектов.

        Args:
            obj (BaseObject): объект для проверки коллизии.

        Returns:
            Optional[BaseObject]: объект, с которым произошла коллизия.
        """
        for sprite in self.sprites():
            if obj.rect.colliderect(sprite.rect) and collide_mask(obj, sprite):
                return sprite

    def events(self, *args, **kwargs) -> None:
        """Запускает у объектов проверку событий."""
        pressed = Pressed()
        for sprite in self.sprites():
            sprite.events(pressed=pressed, *args, **kwargs)

    def scale(self, *args, **kwargs) -> None:
        """Изменяет размер объектов под текущий размер экрана."""
        for sprite in self.sprites():
            sprite.scale(*args, **kwargs)

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
                Color(*self._settings['engine']['rect_outline_color']),
                sprite.rect,
                width=self._settings['engine']['rect_outline_width'],
            )

    def draw(self, surface: Surface, *arg, **kwarg) -> list['BaseObject']:
        """Добавляет обводку спрайтам при отладке."""
        self._debug_mode(surface)
        return super().draw(surface, *arg, **kwarg)


class AllObjectsGroup(BaseGroup):
    """Группа всех объектов."""


class SolidObjectsGroup(BaseGroup):
    """Группа твёрдых объектов."""


class DynamicObjectsGroup(BaseGroup):
    """Группа динамических объектов."""
