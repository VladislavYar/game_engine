from pathlib import Path

import pygame

from engine.animations import EventsAnimationGroup, Animation, EventsAnimation
from engine.objects import DynamicObject, Speed, SolidObject
from engine.events.constants import DEFAULT_EVENT, FALL_EVENT
from engine.events import Events
from engine.physics import PlatformerPhysics
from engine import Engine
from engine.objects.groups import DynamicObjectsGroup, SolidObjectsGroup, TextObjectsGroup
from engine.camera import Camera


PATH_ISOMETRY = Path('isometry')
PATH_PLATFORMER = Path('platformer')


class TileObject(SolidObject):
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(DEFAULT_EVENT, Animation(PATH_ISOMETRY / Path('tile'), is_loop=True))
    )


class RockHeadObject(SolidObject):
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(DEFAULT_EVENT, Animation(PATH_PLATFORMER / Path('rock_head', 'idle'), is_loop=True))
    )


class BoxObject(SolidObject):
    events_animation_group = EventsAnimationGroup(
        EventsAnimation(DEFAULT_EVENT, Animation(PATH_PLATFORMER / Path('box'), is_loop=True))
    )


class TestObject1(PlatformerPhysics, DynamicObject):
    speed = Speed(2, 4, 5, 3, fall_boost=0.05)
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
    draw_groups = (DynamicObjectsGroup(), SolidObjectsGroup(), TextObjectsGroup())
    events_groups = (DynamicObjectsGroup(), SolidObjectsGroup())
    update_groups = (DynamicObjectsGroup(),)

    def __init__(self) -> None:
        tile = TileObject()
        box = BoxObject()
        box1 = BoxObject()
        box2 = BoxObject()
        obj1 = TestObject1()
        rock1 = RockHeadObject()
        rock2 = RockHeadObject()
        self.camera = Camera(obj1, self.draw_groups)
        obj1.set_rect_for_tile_grid(54, 55, 'center')
        rock1.set_rect_for_tile_grid(53, 55)
        tile.set_rect_for_tile_grid(3, 4, 'center')
        box.set_rect_for_tile_grid(4, 6, 'center')
        box1.set_rect_for_tile_grid(5, 10, 'center')
        rock2.set_rect_for_tile_grid(55, 55, 'center')
        box2.set_rect_for_tile_grid(3, 2, 'center')


if __name__ == '__main__':
    """Запуск игры."""
    Game().start()
