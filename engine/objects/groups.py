from pygame.sprite import Group
from pygame import key


class BaseGroup(Group):
    """Базовая группа объектов. Расширяет стандартный класс группы спрайтов."""

    def events(self, *args, **kwargs) -> None:
        """Запускает у объектов проверку событий."""
        pressed = key.get_pressed()
        for sprite in self.sprites():
            sprite.events(pressed=pressed, *args, **kwargs)
