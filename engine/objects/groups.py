from pygame.sprite import Group

from engine.events import Pressed
from engine.metaclasses.singleton import SingletonMeta


class BaseGroup(Group, metaclass=SingletonMeta):
    """Базовая группа объектов. Расширяет стандартный класс группы спрайтов."""

    def events(self, *args, **kwargs) -> None:
        """Запускает у объектов проверку событий."""
        pressed = Pressed()
        for sprite in self.sprites():
            sprite.events(pressed=pressed, *args, **kwargs)

    def scale(self, *args, **kwargs) -> None:
        """Изменяет размер объектов под текущий размер экрана."""
        for sprite in self.sprites():
            sprite.scale(*args, **kwargs)


class AllObjectsGroup(BaseGroup):
    """Группа всех объектов."""
