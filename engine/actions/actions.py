from typing import TYPE_CHECKING, Iterator
from dataclasses import dataclass

from engine.events import Events, Pressed
from engine.audio import Audio
from engine.utils.events import check_events

if TYPE_CHECKING:
    from engine.objects.base_object import BaseObject


class Action:
    """Класс представляющий действие."""

    _audio: Audio = Audio()

    def __init__(self, sound: str | None = None) -> None:
        """Инициализация действия.

        Args:
            sound (str | None): название файла аудио действия. По дефолту None.
        """
        self._sound = self._audio.load_effect(sound) if sound else None

    def perform(self, obj: 'BaseObject') -> None:
        """Совершает действие.

        Args:
            obj (BaseObject): игровой объект над которым совершается действие.
        """


@dataclass
class EventsAction:
    """Dataclass представляющий связь events и действия."""

    events: Events
    action: Action

    def __eq__(self, other: Events) -> bool:
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
        return self.events == other

    def __hash__(self) -> int:
        """Создаёт хэш из множества events.

        Returns:
            int: хэш.
        """
        return hash(self.events)


class EventsActionGroup:
    """Класс группы EventsAction."""

    def __init__(self, *arg: EventsAction) -> None:
        """Инициализирует группу EventsAction."""
        self._events_actions = {events_action: events_action for events_action in arg}

    def __getitem__(self, key: Events) -> EventsAction | None:
        """Отдаёт связь events и действия по ключу.

        Args:
            key (Events): ключ events.

        Returns:
            EventsAnimation | None: связь events и действия.
        """
        return self._events_actions.get(key)

    def __iter__(self) -> Iterator[EventsAction]:
        """Итератор по объектам EventsAction.

        Yields:
            Iterator: итератор по объектам EventsAction.
        """
        return iter(self._events_actions.values())


class ActionGroup:
    """Класс представляющий группу действий."""

    def __init__(
        self,
        events_actions: EventsActionGroup,
        obj: 'BaseObject',
    ) -> None:
        """Инициализация группы действий.

        Args:
            events_actions (EventsActionGroup): группа объектов EventsAction.
            obj (BaseObject): игровой объект.
        """
        self._events_actions = events_actions
        self._obj = obj

    def events(self, pressed: Pressed) -> None:
        """Проверка событий, совершённых пользователем.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        for events_action in self._events_actions:
            if check_events(events_action.events, pressed):
                events_action.action.perform(self._obj)
