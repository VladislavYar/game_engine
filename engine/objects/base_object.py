from pygame import sprite

from engine.objects.groups import AllObjectsGroup, BaseGroup


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
