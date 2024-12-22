import pygame
from pygame import event, display

from engine.mixins import QuitMixin, SetSettingsMixin
from engine.settings import Settings
from engine.audio import Audio


class Engine(QuitMixin, SetSettingsMixin):
    """Игровой движок."""

    def __init__(self) -> None:
        """Инициализация игрового движка."""
        self.clock = pygame.time.Clock()
        self.audio = Audio()
        self.settings = Settings()
        self._set_settings()

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

    def _update(self) -> None:
        """Обновление объектов."""
        self.base._all_sprites.update()

    def _draw(self) -> None:
        """Вывод элемекнтов на дисплей."""
        self.display.fill(pygame.Color('black'))

        self.base._all_sprites.draw(self.display)

        display.flip()

    def _main_loop(self) -> None:
        """Основной цикл игрового процесса."""
        from engine.objects.base_object import BaseObject

        self.base = BaseObject()

        while True:
            self._events()
            self._update()
            self._draw()
            self.clock.tick(self.settings['graphics']['max_fps'])

    def start(self) -> None:
        """Запуск игрового процесса."""
        self._main_loop()
