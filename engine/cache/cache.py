from typing import Callable

from pygame import Surface, Sound

from engine.metaclasses.singleton import SingletonMeta


class Cache(metaclass=SingletonMeta):
    """Класс кэширования."""

    def __init__(self) -> None:
        """Инициализация кэша."""
        self._cache = {}

    def get(self, args_key: tuple, func: Callable, *args, callback: str | None = None, **kwargs) -> Surface | Sound:
        """Отдаёт значение из кэша.

        Args:
            key (tuple): аргументы ключа.
            func (Callable): функция для получения объекта.
            callback (str | None, optional): название функции обратного вызова. По дефолту None.

        Returns:
            Surface | Sound: объект.
        """
        if obj := self._cache.get(args_key):
            return obj
        obj = func(*args, **kwargs)
        if callback:
            obj = getattr(obj, callback)()
        self._cache[args_key] = obj
        return obj
