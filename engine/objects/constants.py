from enum import StrEnum


class NameSpeedEnum(StrEnum):
    """Enum названий скоростей."""

    WALK = 'walk'
    RUN = 'run'
    SQUAT = 'squat'
    FALL = 'fall'
    JUMP = 'jump'
    DOUBLE_JUMP = 'double_jump'
    WALK_BOOST = 'walk_boost'
    RUN_BOOST = 'run_boost'
    SQUAT_BOOST = 'squat_boost'
    FALL_BOOST = 'fall_boost'
    JUMP_BOOST = 'jump_boost'
    DOUBLE_JUMP_BOOST = 'double_jump_boost'


class NameStatusEnum(StrEnum):
    """Enum названий статусов."""

    INACTIVE = 'inactive'
    FOCUS = 'focus'
    COLLISION_MOS = 'collision_mos'
    WALK = 'walk'
    RUN = 'run'
    SQUAT = 'squat'
    FALL = 'fall'
    JUMP = 'jump'
    DOUBLE_JUMP = 'double_jump'
