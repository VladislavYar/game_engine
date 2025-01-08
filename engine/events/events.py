from typing import Iterator


class Events:
    """Класс предоставляющий набора событий."""

    def __init__(self, *args: int) -> None:
        """Создаёт набор событий."""
        self._events = frozenset(args)

    def __eq__(self, other: 'Events') -> bool:
        """Проверка на равество объектов.

        Args:
            other (Events): сравниваемый объект.

        Raises:
            TypeError: ошибка не верного типа объекта.

        Returns:
            bool: результат сравнения.
        """
        if not isinstance(other, Events):
            raise TypeError('Сравниваемый объект должен быть типа Events')
        return self._events == other._events

    def __hash__(self) -> int:
        """Создаёт хэш из неизменяемого множества _events.

        Returns:
            int: хэш.
        """
        return hash(self._events)

    def __iter__(self) -> Iterator[int]:
        """Итератор по events.

        Yields:
            Iterator[int]: итератор по events.
        """
        return iter(self._events)
