import pygame

from engine.events import Events
from engine.actions import EventsAction, EventsActionGroup
from engine.events.constants import FALL_EVENT, DEFAULT_EVENT, JUMP_EVENT, DOUBLE_JUMP_EVENT
from engine.physics.platformer.actions import (
    WalkLeftAction,
    WalkRightAction,
    RunLeftAction,
    RunRightAction,
    FallAction,
    CheckObjectAction,
    JumpStatusAction,
    JumpAction,
    DoubleJumpAction,
    # _RunUpAction,
    # _RunDownAction,
)


class PlatformerPhysics:
    """Физический движок платформера."""

    physics_events_action_group = EventsActionGroup(
        EventsAction(DEFAULT_EVENT, CheckObjectAction(is_loop=True)),
        EventsAction(
            Events(
                pygame.K_SPACE,
            ),
            JumpStatusAction(),
        ),
        (
            EventsAction(DOUBLE_JUMP_EVENT, DoubleJumpAction(is_loop=True)),
            EventsAction(JUMP_EVENT, JumpAction(is_loop=True)),
            EventsAction(FALL_EVENT, FallAction(is_loop=True)),
        ),
        (
            EventsAction(Events(pygame.K_a, pygame.K_LSHIFT), RunLeftAction(is_loop=True)),
            EventsAction(Events(pygame.K_d, pygame.K_LSHIFT), RunRightAction(is_loop=True)),
            EventsAction(Events(pygame.K_a), WalkLeftAction(is_loop=True)),
            EventsAction(Events(pygame.K_d), WalkRightAction(is_loop=True)),
            # EventsAction(Events(pygame.K_w), _RunUpAction(is_loop=True)),
            # EventsAction(Events(pygame.K_s), _RunDownAction(is_loop=True)),
        ),
    )
