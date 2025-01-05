from pathlib import Path

import pygame

from engine.animations import EventsAnimationGroup, Animation, EventsAnimation
from engine.objects import DynamicObject, Speed, SolidObject
from engine.events.constants import DEFAULT_EVENT, FALL_EVENT
from engine.events import Events
from engine.physics import IsometryPhysics, PlatformerPhysics
from engine import Engine
from engine.objects.groups import DynamicObjectsGroup, SolidObjectsGroup


PATH_ISOMETRY = Path('isometry')
PATH_PLATFORMER = Path('platformer')


class TestObject(IsometryPhysics, DynamicObject):
    speed = Speed(3, 6)
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(Events(pygame.K_w, pygame.K_a), Animation(PATH_ISOMETRY / Path('walk_up'), is_loop=True)),
        EventsAnimation(Events(pygame.K_s, pygame.K_d), Animation(PATH_ISOMETRY / Path('walk_down'), is_loop=True)),
        EventsAnimation(Events(pygame.K_a, pygame.K_s), Animation(PATH_ISOMETRY / Path('walk_left'), is_loop=True)),
        EventsAnimation(Events(pygame.K_w, pygame.K_d), Animation(PATH_ISOMETRY / Path('walk_right'), is_loop=True)),
        EventsAnimation(Events(pygame.K_w), Animation(PATH_ISOMETRY / Path('walk_right_up'), is_loop=True)),
        EventsAnimation(Events(pygame.K_a), Animation(PATH_ISOMETRY / Path('walk_left_up'), is_loop=True)),
        EventsAnimation(Events(pygame.K_s), Animation(PATH_ISOMETRY / Path('walk_left_down'), is_loop=True)),
        EventsAnimation(Events(pygame.K_d), Animation(PATH_ISOMETRY / Path('walk_right_down'), is_loop=True)),
        EventsAnimation(DEFAULT_EVENT, Animation(PATH_ISOMETRY / Path('idle_down'), is_loop=True)),
    )


class TileObject(SolidObject):
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(DEFAULT_EVENT, Animation(PATH_ISOMETRY / Path('tile'), is_loop=True))
    )


class BoxObject(SolidObject):
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(DEFAULT_EVENT, Animation(PATH_PLATFORMER / Path('box'), is_loop=True))
    )


class TestObject1(PlatformerPhysics, DynamicObject):
    speed = Speed(2, 4, 5, 2.5)
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(
            FALL_EVENT,
            Animation(PATH_PLATFORMER / 'fall', flip_by_derection=True, is_loop=True, time_between=100),
        ),
        EventsAnimation(
            Events(pygame.K_a, pygame.K_LSHIFT),
            Animation(PATH_PLATFORMER / 'run', flip_by_derection=True, is_loop=True, time_between=50),
        ),
        EventsAnimation(
            Events(pygame.K_d, pygame.K_LSHIFT),
            Animation(PATH_PLATFORMER / 'run', flip_by_derection=True, is_loop=True, time_between=50),
        ),
        EventsAnimation(
            Events(pygame.K_a),
            Animation(PATH_PLATFORMER / 'run', is_loop=True, flip_by_derection=True, time_between=100),
        ),
        EventsAnimation(
            Events(pygame.K_d),
            Animation(PATH_PLATFORMER / 'run', is_loop=True, flip_by_derection=True, time_between=100),
        ),
        EventsAnimation(
            DEFAULT_EVENT, Animation(PATH_PLATFORMER / 'idle', is_loop=True, flip_by_derection=True, time_between=100)
        ),
    )


class Game(Engine):
    draw_groups = (DynamicObjectsGroup(), SolidObjectsGroup())

    def __init__(self) -> None:
        tile = TileObject()
        box = BoxObject()
        box1 = BoxObject()
        box2 = BoxObject()
        tile.rect.center = 700, 550
        # obj = TestObject()
        obj1 = TestObject1()
        obj1.rect.center = 600, 600
        box.rect.center = 2000, 2000
        box1.rect.center = 1000, 500
        box2.rect.center = 1500, 1500
        # obj.rect.center = 500, 500


if __name__ == '__main__':
    """Запуск игры."""
    Game().start()
