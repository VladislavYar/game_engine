from pygame import sprite, mask as mk

from engine.animations import AnimationGroup, EventsAnimationGroup
from engine.actions import EventsActionGroup, ActionGroup
from engine.objects.groups import BaseGroup
from engine.events import Pressed
from engine.constants import ZERO_COORDINATES
from engine.constants.empty import EMPTY_FRAME


class BaseObject(sprite.Sprite):
    """Базовый объект игровог процесса.

    Attributes:
        _all_sprites (BaseGroup): группа всех спрайтов.
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
        events_action_group (EventsActionGroup): группа событий и связанных с ними действий.
        image (Surface): начальное отображение объекта.
        rect (Rect): прямоугольник начального отображения объекта.
        mask (Mask): маска начального отображения объекта.
    """

    _all_sprites = BaseGroup()
    events_animation_group: EventsAnimationGroup
    events_action_group: EventsActionGroup
    image = EMPTY_FRAME.image
    rect = image.get_rect()
    rect.center = ZERO_COORDINATES
    mask = mk.from_surface(image)

    def __init__(self, *arg: BaseGroup) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_sprites, *arg)
        self._animation_group = AnimationGroup(events_animations=self.events_animation_group)
        self._actions_group = ActionGroup(events_actions=self.events_action_group, obj=self)
        self.inactive = False
        self.focus = False

    def events(self, pressed: Pressed) -> None:
        """Проверка совершённых событий.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        pressed(self)
        self._animation_group.events(pressed)
        self._actions_group.events(pressed)

    def _new_frame(self) -> None:
        """Устанавливает новый фрейм."""
        rect_center = self.rect.center
        frame = self._animation_group.frame
        self.image = frame.image
        self.rect = frame.rect
        self.rect.center = rect_center
        self.mask = frame.mask

    def update(self) -> None:
        """Логика обновления спрайта."""
        self._new_frame()

    def scale(self) -> None:
        """Изменяет размер объекта под текущий размер экрана."""
        self._animation_group.scale()
