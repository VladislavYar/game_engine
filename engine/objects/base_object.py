from pygame import key, sprite

from engine.animations import AnimationGroup, EventsAnimationGroup
from engine.objects.groups import BaseGroup


class BaseObject(sprite.Sprite):
    """Базовый объект игровог процесса.

    Attributes:
        _all_sprites (BaseGroup): группа всех спрайтов.
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
    """

    _all_sprites = BaseGroup()
    events_animation_group: EventsAnimationGroup

    def __init__(self, *arg: BaseGroup) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_sprites, *arg)
        self._animation_group = AnimationGroup(events_animations=self.events_animation_group)

    def events(self, pressed: key.ScancodeWrapper) -> None:
        """Проверка совершённых событий.

        Args:
            pressed (key.ScancodeWrapper): кортеж состояний кнопок.
        """
        self._animation_group.events(pressed)

    def update(self) -> None:
        """Логика обновления спрайта."""
        frame = self._animation_group.frame
        self.image = frame.image
        self.rect = frame.rect
        self.mask = frame.mask
        self.rect.center = (500, 500)
