from pygame import sprite, mask as mk

from engine.animations import AnimationGroup, EventsAnimationGroup
from engine.objects.groups import BaseGroup
from engine.events import Pressed
from engine.constants import ZERO_COORDINATES
from engine.constants.empty import EMPTY_FRAME


class BaseObject(sprite.Sprite):
    """Базовый объект игровог процесса.

    Attributes:
        _all_sprites (BaseGroup): группа всех спрайтов.
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
        image (Surface): начальное отображение объекта.
        rect (Rect): прямоугольник начального отображения объекта.
        mask (Mask): маска начального отображения объекта.
    """

    _all_sprites = BaseGroup()
    events_animation_group: EventsAnimationGroup
    image = EMPTY_FRAME.image
    rect = image.get_rect()
    rect.center = ZERO_COORDINATES
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

    def _new_frame(self) -> None:
        """Устанавливает новый фрейм."""
        frame = self._animation_group.frame
        self.image = frame.image
        self.rect = frame.rect
        self.mask = frame.mask

    def update(self) -> None:
        """Логика обновления спрайта."""
        self._new_frame()

    def scale(self) -> None:
        """Изменяет размер объекта под текущий размер экрана."""
        self._animation_group.scale()
