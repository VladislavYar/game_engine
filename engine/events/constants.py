from enum import IntEnum

from engine.events.events import Events


class EventEnum(IntEnum):
    """Кастомные event."""

    DEFAULT_EVENT = 2000000001
    INACTIVE_EVENT = 2000000002
    COLLISION_MOS_EVENT = 2000000003
    FOCUS_EVENT = 2000000004


DEFAULT_EVENT = Events(EventEnum.DEFAULT_EVENT)
INACTIVE_EVENT = Events(EventEnum.INACTIVE_EVENT)
COLLISION_MOS_EVENT = Events(EventEnum.COLLISION_MOS_EVENT)
FOCUS_EVENT = Events(EventEnum.FOCUS_EVENT)
