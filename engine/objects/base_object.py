from pygame import sprite, surface, mask as mk

from engine.animations import AnimationGroup, EventsAnimationGroup
from engine.objects.groups import BaseGroup
from engine.events import Pressed


class BaseObject(sprite.Sprite):
    """Базовый объект игровог процесса.

    Attributes:
        _all_sprites (BaseGroup): группа всех спрайтов.
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
        image (surface.Surface): начальное отображение объекта.
        rect (rt.Rect): прямоугольник начального отображения объекта.
        mask (mk.Mask): маска начального отображения объекта.
    """

    _all_sprites = BaseGroup()
    events_animation_group: EventsAnimationGroup
    image = surface.Surface((0, 0))
    rect = image.get_rect()
    mask = mk.from_surface(image)

    def __init__(self, *arg: BaseGroup) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_sprites, *arg)
        self._animation_group = AnimationGroup(events_animations=self.events_animation_group)
        self.inactive = False
        self.focus = False

    def events(self, pressed: Pressed) -> None:
        """Проверка совершённых событий.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        pressed(self)
        self._animation_group.events(pressed)

    def update(self) -> None:
        """Логика обновления спрайта."""
        frame = self._animation_group.frame
        self.image = frame.image
        self.rect = frame.rect
        self.mask = frame.mask
        self.rect.center = (500, 500)
