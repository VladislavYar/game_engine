from enum import IntEnum

from engine.events.events import Events


class EventEnum(IntEnum):
    """Кастомные event."""

    DEFAULT_EVENT = 2000000001
    INACTIVE_EVENT = 2000000002
    COLLISION_MOS_EVENT = 2000000003
    FOCUS_EVENT = 2000000004
    JUMP_EVENT = 2000000005
    DOUBLE_JUMP_EVENT = 2000000006
    FALL_EVENT = 2000000007
    HIT_EVENT = 2000000008
    DEATH_EVENT = 2000000009


DEFAULT_EVENT = Events(EventEnum.DEFAULT_EVENT)
INACTIVE_EVENT = Events(EventEnum.INACTIVE_EVENT)
COLLISION_MOS_EVENT = Events(EventEnum.COLLISION_MOS_EVENT)
FOCUS_EVENT = Events(EventEnum.FOCUS_EVENT)
JUMP_EVENT = Events(EventEnum.JUMP_EVENT)
DOUBLE_JUMP_EVENT = Events(EventEnum.DOUBLE_JUMP_EVENT)
FALL_EVENT = Events(EventEnum.FALL_EVENT)
HIT_EVENT = Events(EventEnum.HIT_EVENT)
DEATH_EVENT = Events(EventEnum.DEATH_EVENT)
