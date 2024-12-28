from pygame.sprite import Group

from engine.events import Pressed


class BaseGroup(Group):
    """Базовая группа объектов. Расширяет стандартный класс группы спрайтов."""

    def events(self, *args, **kwargs) -> None:
        """Запускает у объектов проверку событий."""
        pressed = Pressed()
        for sprite in self.sprites():
            sprite.events(pressed=pressed, *args, **kwargs)
