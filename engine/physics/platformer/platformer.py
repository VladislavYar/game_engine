import pygame
from engine.events import Events

from engine.actions import EventsAction, EventsActionGroup
from engine.physics.platformer.actions import Test1, Test2, Test3, Test4


class PlatformerPhysics:
    """Физический движок платформера.

    Attributes:
        events_animation_group (EventsAnimationGroup): группа событий и связанных с ними анимаций.
    """

    events_action_group = EventsActionGroup(
        EventsAction(Events(pygame.K_a), Test2()),
        EventsAction(Events(pygame.K_d), Test1()),
        EventsAction(Events(pygame.K_w), Test3()),
        EventsAction(Events(pygame.K_s), Test4()),
    )
