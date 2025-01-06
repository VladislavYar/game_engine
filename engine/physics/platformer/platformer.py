import pygame

from engine.events import Events
from engine.events.constants import FALL_EVENT, DEFAULT_EVENT
from engine.actions import EventsAction, EventsActionGroup

from engine.physics.platformer.actions import (
    WalkLeftAction,
    WalkRightAction,
    RunLeftAction,
    RunRightAction,
    FallAction,
    _RunUpAction,
    _RunDownAction,
    CheckObjectAction,
)


class PlatformerPhysics:
    """Физический движок платформера.

    Attributes:
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
    """

    events_action_group = EventsActionGroup(
        (
            EventsAction(Events(pygame.K_a, pygame.K_LSHIFT), RunLeftAction(is_loop=True)),
            EventsAction(Events(pygame.K_d, pygame.K_LSHIFT), RunRightAction(is_loop=True)),
            EventsAction(Events(pygame.K_a), WalkLeftAction(is_loop=True)),
            EventsAction(Events(pygame.K_d), WalkRightAction(is_loop=True)),
            EventsAction(Events(pygame.K_w), _RunUpAction(is_loop=True)),
            EventsAction(Events(pygame.K_s), _RunDownAction(is_loop=True)),
        ),
        EventsAction(FALL_EVENT, FallAction(is_loop=True)),
        EventsAction(DEFAULT_EVENT, CheckObjectAction(is_loop=True)),
    )
