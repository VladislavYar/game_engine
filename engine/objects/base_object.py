from pygame import sprite
import pygame

from engine.animations import Animation, AnimationGroup, EventsAnimation, EventAnimationGroup
from engine.events.constants import DEFAULT_EVENT
from engine.events import Events


class BaseObject(sprite.Sprite):
    """Базовый объект игровог процесса.

    Attributes:
        _all_sprites (sprite.Group): группа всех спрайтов.
    """

    _all_sprites = sprite.Group()

    _events_animations = EventAnimationGroup(
        EventsAnimation(Events(pygame.K_w, pygame.K_a), Animation('test3', is_loop=True)),
        EventsAnimation(Events(pygame.K_a), Animation('test2', is_loop=True)),
        EventsAnimation(DEFAULT_EVENT, Animation('test', is_loop=True)),
    )

    def __init__(self) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_sprites)
        self._animation_group = AnimationGroup(events_animations=self._events_animations)

    def update(self) -> None:
        self._animation_group.events()
        frame = self._animation_group.frame
        self.image = frame
        self.rect = frame.get_rect()
        self.rect.center = (500, 500)
