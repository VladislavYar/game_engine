from enum import IntEnum

from engine.events.events import Events


class EventEnum(IntEnum):
    """Кастомные event."""

    DEFAULT_EVENT = -1


DEFAULT_EVENT = Events(EventEnum.DEFAULT_EVENT)
