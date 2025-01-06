from typing import TYPE_CHECKING, Iterator
from dataclasses import dataclass

from engine.events import Events, Pressed
from engine.audio import Audio
from engine.utils.events import check_events
from engine.mixins.management import ManagementMixin
from engine.settings import Settings
from engine.constants.direction import DirectionGroupEnum

if TYPE_CHECKING:
    from engine.objects.groups import BaseGroup
    from engine.objects import Object


class Action(ManagementMixin):
    """Класс представляющий действие.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        _audio (Audio): объект для работы с аудио.
        time_between (int): время между действиями.
    """

    _settings: Settings = Settings()
    _audio: Audio = Audio()
    time_between: int = _settings['engine']['time_between']['time_between_actions']

    def __init__(
        self,
        is_loop: bool = False,
        sound: str | None = None,
        time_between: int | None = None,
    ) -> None:
        """Инициализация действия.

        Args:
            is_loop (bool, optional): зацикленная анимация. По дефолту False.
            sound (str | None): название файла аудио действия. По дефолту None.
            time_between (int | None, optional): Время между действиями. По дефолту None.
        """
        self.time_between = time_between if time_between else self.time_between
        self._sound = self._audio.load_effect(sound) if sound else None
        self.is_loop = is_loop
        self._set_default_values()

    def _get_count_actions_performed(self) -> int:
        """Необходимое количество совершения действия."""
        count_actions_performed, self._elapsed = self._update_elapsed()
        if not self.is_active or not count_actions_performed:
            return 0
        if not self.is_loop:
            self.stop()
            return 1
        return count_actions_performed

    def perform(self, obj: 'Object') -> None:
        """Совершает действие.

        Args:
            obj (Object): игровой объект над которым совершается действие.
        """


class DynamicAction(Action):
    """Класс представляющий динамическое действие."""

    def _push_out_object(
        self,
        obj: 'Object',
        group: 'BaseGroup',
        direction: DirectionGroupEnum,
        sing_x_y: tuple[int, int],
    ) -> None:
        """Метод выталкивания объекта.

        Args:
            obj (Object): объект для выталкивания.
            group (BaseGroup): группа для проверки коллизии.
            direction (DirectionGroupEnum): направление проверки коллизии.
            sing_x_y (tuple[int, int]): направление выталкивания.
        """
        if sprite_coordinate := group.collide_side_mask(obj, direction):
            sign_x, sign_y = sing_x_y
            while True:
                obj.rect.y -= sign_y
                obj.rect.x -= sign_x
                if not obj.collide_side_rect_with_mask(sprite_coordinate[0], direction):
                    obj.rect.y += sign_y
                    obj.rect.x += sign_x
                    break


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

    def __init__(self, *arg: EventsAction | tuple[EventsAction]) -> None:
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

    def __iter__(self) -> Iterator[EventsAction | tuple[EventsAction]]:
        """Итератор по объектам EventsAction.

        Yields:
            Iterator: итератор по объектам EventsAction.
        """
        return iter(self._events_actions.values())


class ActiveActions:
    """Класс активных действий."""

    def __init__(self, obj: 'Object') -> None:
        """Инициализация объекта активных действий.

        Args:
            obj (Object): игровой объект.
        """
        self._obj = obj
        self._active_actions: dict[Events, Action] = {}

    def __setitem__(self, key: Events, value: Action) -> None:
        """Устанавливает активное действие.

        Args:
            key (Events): events.
            value (Action): действие.
        """
        if not self._active_actions.get(key):
            self._active_actions[key] = value
            value.start()
        value.perform(self._obj)

    def __delitem__(self, key: Events) -> None:
        """Удаляет активное действие.

        Args:
            key (Events): events.
        """
        if action := self._active_actions.get(key):
            action.stop()
            del self._active_actions[key]


class ActionGroup:
    """Класс представляющий группу действий."""

    def __init__(
        self,
        events_actions: EventsActionGroup,
        obj: 'Object',
    ) -> None:
        """Инициализация группы действий.

        Args:
            events_actions (EventsActionGroup): группа объектов EventsAction.
            obj (Object): игровой объект.
        """
        self._events_actions = events_actions
        self._active_actions = ActiveActions(obj)

    def _check_group_events(self, events_actions: tuple[EventsAction, ...], pressed: Pressed) -> None:
        """Проверка группу событий.

        Args:
            events_actions (tuple[EventsAction, ...]): кортеж отношения events к действию.
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        is_set_action = False
        for events_action in events_actions:
            if check_events(events_action.events, pressed) and not is_set_action:
                is_set_action = True
                self._active_actions[events_action.events] = events_action.action
            else:
                del self._active_actions[events_action.events]

    def events(self, pressed: Pressed) -> None:
        """Проверка событий, совершённых пользователем.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        for events_action in self._events_actions:
            if isinstance(events_action, tuple):
                self._check_group_events(events_action, pressed)
            elif check_events(events_action.events, pressed):
                self._active_actions[events_action.events] = events_action.action
            else:
                del self._active_actions[events_action.events]
