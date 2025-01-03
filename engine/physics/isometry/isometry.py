import pygame

from engine.events import Events
from engine.actions import EventsAction, EventsActionGroup
from engine.physics.isometry.actions import (
    WalkDownAction,
    WalkLeftDownAction,
    WalkLeftUpAction,
    WalkRightDownAction,
    WalkRightUpAction,
    WalkUpAction,
    WalkLeftAction,
    WalkRightAction,
)


class IsometryPhysics:
    """Физический движок изометрии.

    Attributes:
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
    """

    events_action_group = EventsActionGroup(
        (
            EventsAction(Events(pygame.K_w, pygame.K_a), WalkUpAction(is_loop=True)),
            EventsAction(Events(pygame.K_s, pygame.K_d), WalkDownAction(is_loop=True)),
            EventsAction(Events(pygame.K_a, pygame.K_s), WalkLeftAction(is_loop=True)),
            EventsAction(Events(pygame.K_w, pygame.K_d), WalkRightAction(is_loop=True)),
            EventsAction(Events(pygame.K_w), WalkRightUpAction(is_loop=True)),
            EventsAction(Events(pygame.K_a), WalkLeftUpAction(is_loop=True)),
            EventsAction(Events(pygame.K_s), WalkLeftDownAction(is_loop=True)),
            EventsAction(Events(pygame.K_d), WalkRightDownAction(is_loop=True)),
        ),
    )
