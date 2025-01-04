from copy import deepcopy

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
    """

    _all_objects_group = AllObjectsGroup()
    groups: tuple[BaseGroup, ...] = tuple()
    events_action_group: EventsActionGroup = EventsActionGroup()
    events_animation_group: EventsAnimationGroup

    def __init__(self) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_objects_group, *self.groups)
        self._set_default_values()
        self._animation_group = AnimationGroup(events_animations=deepcopy(self.events_animation_group), obj=self)
        self._actions_group = ActionGroup(events_actions=deepcopy(self.events_action_group), obj=self)

    def _set_default_values(self) -> None:
        """Устанавливает дефолтные значения для игрового объекта."""
        self.status = Status(self)
        self.image = EMPTY_FRAME.image
        self.rect = self.image.get_rect()
        self.rect.center = ZERO_COORDINATES
        self.mask = mk.from_surface(self.image)
        self.direction: DirectionGroupEnum | None = None

    def events(self, pressed: Pressed) -> None:
        """Проверка совершённых событий.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        pressed.status = self.status
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

    def _get_collision_side(self, obj: 'BaseObject') -> DirectionGroupEnum:
        """Отдаёт сторону коллизии.

        Args:
            obj ('BaseObject'): объект для проверки стороны коллизии.

        Returns:
            DirectionGroupEnum: сторона коллизии.
        """
        if self.rect.bottom <= obj.rect.top + obj.rect.height and self.rect.bottom >= obj.rect.top:
            return DirectionGroupEnum.DOWN
        elif self.rect.top <= obj.rect.bottom and self.rect.top >= obj.rect.bottom - obj.rect.height:
            return DirectionGroupEnum.UP
        elif self.rect.right >= obj.rect.left and self.rect.left <= obj.rect.left:
            return DirectionGroupEnum.RIGHT
        elif self.rect.left <= obj.rect.right and self.rect.right >= obj.rect.right:
            return DirectionGroupEnum.LEFT

    def collide_side_rect_with_mask(self, obj: 'BaseObject', side: DirectionGroupEnum) -> bool:
        """Проверяет сторону коллизии rect объекта c маской другого объекта.

        Args:
            obj (BaseObject): объект для проверки коллизии.
            side (DirectionGroupEnum): сторона для проверки.

        Returns:
            bool: флаг коллизии.
        """
        if not self.rect.colliderect(obj.rect):
            return False
        xoffset = obj.rect[0] - self.rect[0]
        yoffset = obj.rect[1] - self.rect[1]
        if self.mask.overlap(obj.mask, (xoffset, yoffset)) and self._get_collision_side(obj) == side:
            return True
        return False

    def collide_side_mask(self, obj: 'BaseObject', side: DirectionGroupEnum) -> bool:
        """Проверяет коллизию по маске с объектом с определённой стороны.

        Args:
            obj (BaseObject): объект для проверки коллизии.
            side (DirectionGroupEnum): сторона для проверки.

        Returns:
            bool: флаг коллизии.
        """
        if not self.rect.colliderect(obj.rect):
            return False
        if sprite.collide_mask(self, obj) and self._get_collision_side(obj) == side:
            return True
        return False


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
