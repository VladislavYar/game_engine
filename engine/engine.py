from typing import Iterable

from pygame import event, display, Surface, transform, Color

from engine.mixins import QuitMixin, SetSettingsMixin
from engine.settings import Settings
from engine.audio import Audio
from engine.metaclasses.engine import EngineMeta
from engine.objects.groups import AllObjectsGroup, BaseGroup
from engine.time import GlobalClock
from engine.utils.screen import get_sreen_resolution
from engine.objects.text import Text
from engine.tile_grid import TileGrid
from engine.constants import Coordinate
from engine.camera import Camera


class Engine(QuitMixin, SetSettingsMixin, metaclass=EngineMeta):
    """Игровой движок.

    Attributes:
        visible_map (Surface): отображение видимой части карты.
        events_groups (Iterable[BaseGroup]): группы для проверки событий. Проверяются в порядке индекса.
        update_groups (Iterable[BaseGroup]): группы для обновления. Обновляются в порядке индекса.
        draw_groups (Iterable[BaseGroup]): группы для вывода. Выводятся в порядке индекса.
        camera: (Camera | None, optional): игровая камера. По дефолту None.
        _global_clock (GlobalClock): объект глобальных часов игрового процесса.
        _audio (Audio): объект для работы с аудио.
        _settings (Settings): объект настроек игрового процесса.
        _all_objects_group (AllObjectsGroup): группа всех игровых объектов.
        _tile_grid (TileGrid): сетка тайтлов.
        _debug (bool): флаг debug-a.
        _display_fps (Surface): отображение fps.
    """

    visible_map: Surface
    events_groups: Iterable[BaseGroup]
    update_groups: Iterable[BaseGroup]
    draw_groups: Iterable[BaseGroup]
    camera: Camera | None = None
    _global_clock: GlobalClock = GlobalClock()
    _audio: Audio = Audio()
    _settings: Settings = Settings()
    _all_objects_group: AllObjectsGroup = AllObjectsGroup()
    _tile_grid: TileGrid = TileGrid()
    _debug: bool = _settings['engine']['debug']['debug_mode']
    _display_fps = Text()
    _display_fps.rect.center = Coordinate(*_settings['engine']['debug']['display_fps_coordinate'])

    def _debug_mode(self) -> None:
        """Веbug mode."""
        if not self._debug:
            return
        self._display_fps.text = f'{int(self._global_clock.get_fps())}'
        self.visible_map.blit(self._display_fps.text, self._display_fps.rect)
        self.visible_map.blit(self._tile_grid.surface, self._tile_grid.rect)

    def _get_events(self) -> dict[int, event.Event]:
        """Отдаёт события в виде словаря.

        Returns:
            dict[int, Event]: события в виде словаря(ключ: тип события, значение: событие).
        """
        return {event.type: event for event in event.get()}

    def _events(self) -> None:
        """Проверка событий, совершённых пользователем."""
        events = self._get_events()
        self._check_quit(events)
        for group in self.events_groups:
            group.events()

    def _update(self) -> None:
        """Обновление объектов."""
        for group in self.update_groups:
            group.update()
        if self.camera:
            self.camera.update()

    def _draw(self) -> None:
        """Вывод элементов на дисплей."""
        self.visible_map.fill(Color('black'))
        self._debug_mode()
        for group in self.draw_groups:
            group.draw(self.visible_map)
        frame = transform.scale(self.visible_map, get_sreen_resolution())
        self.display.blit(frame, frame.get_frect())
        display.flip()

    def _main_loop(self) -> None:
        """Основной цикл игрового процесса."""
        while True:
            self._events()
            self._update()
            self._draw()
            self._global_clock.tick(self._settings['graphics']['max_fps'])

    def start(self) -> None:
        """Запуск игрового процесса."""
        self._main_loop()
