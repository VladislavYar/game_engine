from typing import Iterable

from pygame import event, display, Surface, transform, Color

from engine.mixins import QuitMixin, SetSettingsMixin
from engine.settings import Settings
from engine.audio import Audio
from engine.metaclasses.engine import EngineMeta
from engine.objects.groups import AllObjectsGroup, BaseGroup
from engine.time import GlobalClock
from engine.utils.screen import get_sreen_resolution
from engine.text import Text


class Engine(QuitMixin, SetSettingsMixin, metaclass=EngineMeta):
    """Игровой движок.

    Attributes:
        visible_map (Surface): отображение видимой части карты.
        draw_groups (Iterable[BaseGroup]): группы для вывода. Выводятся в порядке индекса.
        _global_clock (GlobalClock): объект глобальных часов игрового процесса.
        _audio (Audio): объект для работы с аудио.
        _settings (Settings): объект настроек игрового процесса.
        _all_objects_group (AllObjectsGroup): группа всех игровых объектов.
    """

    visible_map: Surface
    draw_groups: Iterable[BaseGroup]
    _global_clock: GlobalClock = GlobalClock()
    _audio: Audio = Audio()
    _settings: Settings = Settings()
    _all_objects_group: AllObjectsGroup = AllObjectsGroup()

    def _debug_mode(self) -> None:
        """Веbug mode."""
        if not self._settings['engine']['debug_mode']:
            return
        fps = Text(text=f'{int(self._global_clock.get_fps())}')
        self.visible_map.blit(fps.text, fps.rect)

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
        self._all_objects_group.events()

    def _update(self) -> None:
        """Обновление объектов."""
        self._all_objects_group.update()

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
