import pygame
from pygame import event, display

from engine.mixins import QuitMixin, SetSettingsMixin
from engine.settings import Settings
from engine.audio import Audio
from engine.metaclasses.engine import EngineMeta
from engine.objects.groups import AllObjectsGroup
from engine.time import GlobalClock


class Engine(QuitMixin, SetSettingsMixin, metaclass=EngineMeta):
    """Игровой движок.

    Attributes:
        _global_clock (GlobalClock): объект глобальных часов игрового процесса.
        _audio (Audio): объект для работы с аудио.
        _settings (Settings): объект настроек игрового процесса.
        _all_objects_group (AllObjectsGroup): группа всех игровых объектов.
    """

    _global_clock: GlobalClock = GlobalClock()
    _audio: Audio = Audio()
    _settings: Settings = Settings()
    _all_objects_group: AllObjectsGroup = AllObjectsGroup()

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
        """Вывод элемекнтов на дисплей."""
        self.display.fill(pygame.Color('black'))
        self._all_objects_group.draw(self.display)
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
