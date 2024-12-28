import pygame

from engine.animations import EventsAnimationGroup
from engine.objects.base_object import BaseObject
from engine.animations import Animation, EventsAnimation
from engine.events.constants import DEFAULT_EVENT, COLLISION_MOS_EVENT, INACTIVE_EVENT, FOCUS_EVENT
from engine.events import Events


class TestObject(BaseObject):
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(Events(pygame.K_w, pygame.K_a), Animation('test3', is_loop=True)),
        EventsAnimation(Events(pygame.K_a), Animation('test2', is_loop=True)),
        EventsAnimation(COLLISION_MOS_EVENT, Animation('test3', is_loop=True)),
        EventsAnimation(INACTIVE_EVENT, Animation('test3', is_loop=True)),
        EventsAnimation(FOCUS_EVENT, Animation('test', is_loop=True)),
        EventsAnimation(DEFAULT_EVENT, Animation('test', is_loop=True)),
    )
