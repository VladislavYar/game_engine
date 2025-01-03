from pygame import sprite, mask as mk

from engine.animations import AnimationGroup, EventsAnimationGroup
from engine.actions import EventsActionGroup, ActionGroup
from engine.objects.groups import AllObjectsGroup, BaseGroup, SolidObjectsGroup, DynamicObjectsGroup
from engine.events import Pressed
from engine.constants import ZERO_COORDINATES
from engine.constants.empty import EMPTY_FRAME
from engine.objects.dataclasses import Speed, Status
from engine.constants.direction import DirectionGroupEnum


class BaseObject(sprite.Sprite):
    """Базовый объект игрового процесса.

    Attributes:
        _all_objects_group (AllObjectsGroup): группа всех игровых объектов.
        groups (tuple[BaseGroup, ...]): кортеж групп игровых объектов. По дефолту tuple.
        events_action_group (EventsActionGroup): группа событий и связанных с ними действий.
            По дефолту пустой EventsActionGroup.
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
        image (Surface): начальное отображение объекта.
        rect (Rect): прямоугольник начального отображения объекта.
        mask (Mask): маска начального отображения объекта.
        direction (DirectionGroupEnum | None, optional): направление объекта. По дефолту None.
    """

    _all_objects_group = AllObjectsGroup()
    groups: tuple[BaseGroup, ...] = tuple()
    events_action_group: EventsActionGroup = EventsActionGroup()
    events_animation_group: EventsAnimationGroup
    image = EMPTY_FRAME.image
    rect = image.get_rect()
    rect.center = ZERO_COORDINATES
    mask = mk.from_surface(image)
    direction: DirectionGroupEnum | None = None

    def __init__(self) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_objects_group, *self.groups)
        self._animation_group = AnimationGroup(events_animations=self.events_animation_group, obj=self)
        self._actions_group = ActionGroup(events_actions=self.events_action_group, obj=self)
        self.status = Status()

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


class SolidObject(BaseObject):
    """Класс твёрдого объекта."""

    groups: tuple[SolidObjectsGroup] = (SolidObjectsGroup(),)


class DynamicObject(BaseObject):
    """Класс динамического объекта.

    Attributes:
        speed (Speed): скорость динамического объекта.
        derection (DirectionEnum, optional): направление объекта. По дефолту DirectionEnum.RIGHT.
    """

    groups: tuple[DynamicObjectsGroup] = (DynamicObjectsGroup(),)
    speed: Speed
