from pygame import sprite, mask as mk

from engine.objects.groups import AllObjectsGroup, BaseGroup
from engine.constants.empty import EMPTY_FRAME, ZERO_COORDINATES, ZERO_COORDINATES_SHIFT


class BaseObject(sprite.Sprite):
    """Базовый объект игрового процесса.

    Attributes:
        _all_objects_group (AllObjectsGroup): группа всех игровых объектов.
        groups (tuple[BaseGroup, ...]): кортеж групп игровых объектов. По дефолту tuple.
    """

    _all_objects_group = AllObjectsGroup()
    groups: tuple[BaseGroup, ...] = tuple()

    def __init__(self) -> None:
        """Инициализация базового объекта."""
        super().__init__(self._all_objects_group, *self.groups)
        self._set_empty_frame()

    def _set_empty_frame(self) -> None:
        """Устанавливает пустой frame."""
        self.image = EMPTY_FRAME.image
        self.rect = self.image.get_frect()
        self.rect.center = ZERO_COORDINATES
        self.coordinate_shift = ZERO_COORDINATES_SHIFT
        self.mask = mk.from_surface(self.image)
        self.rect_mask = self.mask
