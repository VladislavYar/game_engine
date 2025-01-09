from copy import deepcopy

from pygame import sprite

from engine.animations import AnimationGroup, EventsAnimationGroup
from engine.actions import EventsActionGroup, ActionGroup
from engine.objects.groups import SolidObjectsGroup, DynamicObjectsGroup
from engine.events import Pressed
from engine.constants import Coordinate
from engine.objects.dataclasses import Speed, Status, DynamicStatus
from engine.constants.direction import DirectionGroupEnum
from engine.tile_grid import TileGrid
from engine.objects.base_object import BaseObject


class Object(BaseObject):
    """Объект игрового процесса.

    Attributes:
        _status_class (Status): класс статусов. По дефолту Status.
        _tile_grid (TileGrid): сетка тайтлов.
        events_action_group (EventsActionGroup): группа событий и связанных с ними действий.
            По дефолту пустой EventsActionGroup.
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
    """

    _status_class: Status = Status
    _tile_grid: TileGrid = TileGrid()

    events_action_group: EventsActionGroup = EventsActionGroup()
    events_animation_group: EventsAnimationGroup

    def __init__(self) -> None:
        super().__init__()
        self._set_default_values()
        self._init_animation_actions_group()
        self.events(Pressed())
        self.update()

    def _init_animation_actions_group(self) -> None:
        """Инициализация групп animation и actions."""
        self._animation_group = AnimationGroup(deepcopy(self.events_animation_group, memo={'obj': self}))
        self._actions_group = ActionGroup(deepcopy(self.events_action_group, memo={'obj': self}))

    def _set_default_values(self) -> None:
        """Устанавливает дефолтные значения для игрового объекта."""
        self.status = self._status_class(self)
        self.direction: DirectionGroupEnum | None = None

    def set_rect_for_tile_grid(self, row: int, column: int, position: str = 'center') -> None:
        """Устанавливает rect по позиции в тайтл сетке.

        Args:
            row (int): строка.
            column (int): колонка.
            position (str, optional): позиция rect. По дефолту 'center'.
        """
        setattr(self.rect, position, Coordinate(*getattr(self._tile_grid[row][column].rect, position)))

    def _animation_actions_events(self, pressed: Pressed) -> None:
        """Проверка совершённых событий группах animation и actions.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        self._actions_group.events(pressed)
        self._animation_group.events(pressed)

    def events(self, pressed: Pressed) -> None:
        """Проверка совершённых событий.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        pressed.status = self.status
        self._animation_actions_events(pressed)

    def _new_frame(self) -> None:
        """Устанавливает новый фрейм."""
        rect_center = self.rect.center
        frame = self._animation_group.frame
        self.image = frame.image
        self.rect = frame.rect
        self.rect.center = rect_center
        self.coordinate_shift = frame.coordinate_shift
        self.mask = frame.mask
        self.rect_mask = frame.rect_mask

    def update(self) -> None:
        """Логика обновления спрайта."""
        self._new_frame()

    def _get_collision_side(self, obj: 'Object') -> DirectionGroupEnum:
        """Отдаёт сторону коллизии.

        Args:
            obj ('Object'): объект для проверки стороны коллизии.

        Returns:
            DirectionGroupEnum: сторона коллизии.
        """
        if self.rect.bottom <= obj.rect.top + obj.rect.height and self.rect.bottom >= obj.rect.top:
            return DirectionGroupEnum.DOWN
        elif self.rect.top <= obj.rect.bottom and self.rect.top >= obj.rect.bottom - obj.rect.height:
            return DirectionGroupEnum.UP
        if self.rect.right >= obj.rect.left and self.rect.left <= obj.rect.left:
            return DirectionGroupEnum.RIGHT
        if self.rect.left <= obj.rect.right and self.rect.right >= obj.rect.right:
            return DirectionGroupEnum.LEFT

    def collide_rect_with_mask(self, obj: 'Object', side: DirectionGroupEnum | None = None) -> Coordinate | None:
        """Проверяет сторону коллизии rect объекта c маской другого объекта.

        Args:
            obj (Object): объект для проверки коллизии.
            side (DirectionGroupEnum | None, optional): сторона для проверки. По дефолту None.

        Returns:
            Coordinate | None: координаты коллизии.
        """
        if not self.rect.colliderect(obj.rect):
            return
        offset = (self.rect.x - obj.rect.x, self.rect.y - obj.rect.y)
        coordinate = obj.mask.overlap(self.rect_mask, offset)
        if coordinate and (not side or self._get_collision_side(obj) == side):
            return Coordinate(*coordinate)
        return

    def collide_mask(self, obj: 'Object', side: DirectionGroupEnum | None = None) -> Coordinate | None:
        """Проверяет коллизию по маске с объектом.

        Args:
            obj (Object): объект для проверки коллизии.
            side (DirectionGroupEnum | None, optional): сторона для проверки. По дефолту None.

        Returns:
            Coordinate | None: координаты коллизии.
        """
        if not self.rect.colliderect(obj.rect):
            return
        coordinate = sprite.collide_mask(self, obj)
        if coordinate and (not side or self._get_collision_side(obj) == side):
            return Coordinate(*coordinate)
        return


class SolidObject(Object):
    """Класс твёрдого объекта."""

    groups: tuple[SolidObjectsGroup] = (SolidObjectsGroup(),)


class DynamicObject(Object):
    """Класс динамического объекта.

    Attributes:
        speed (Speed): скорость динамического объекта.
        physics_events_action_group (EventsAnimationGroup): группа событий и действий физики.
    """

    _status_class = DynamicStatus
    speed: Speed
    physics_events_action_group: EventsActionGroup = EventsActionGroup()
    groups: tuple[DynamicObjectsGroup] = (DynamicObjectsGroup(),)

    def _init_animation_actions_group(self) -> None:
        super()._init_animation_actions_group()
        self._physics_actions_group = ActionGroup(deepcopy(self.physics_events_action_group, memo={'obj': self}))

    def _animation_actions_events(self, pressed: Pressed) -> None:
        self._physics_actions_group.events(pressed)
        super()._animation_actions_events(pressed)
