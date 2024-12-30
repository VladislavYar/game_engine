from engine.events.constants import DEFAULT_EVENT
from engine.events import Events, Pressed


def check_events(events: Events, pressed: Pressed) -> bool:
    """Проверка событий.

    Args:
        events (Events): события для проверки.
        pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.

    Returns:
        bool: флаг соответсвия событиям.
    """
    return events == DEFAULT_EVENT or all([pressed[event] for event in events])
