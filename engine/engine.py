import pygame

from engine.mixins import QuitMixin, SetSettingsMixin
from engine.settings import Settings
from engine.audio import Audio


class Engine(QuitMixin, SetSettingsMixin):
    """Игровой движок."""

    def __init__(self) -> None:
        """Инициализация игрового движка."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.audio = Audio()
        self.settings = Settings()
        self._set_settings()

    def _check_event(self) -> None:
        """Проверка событий."""
        events = pygame.event.get()
        self._check_quit(events)

    def _display_screen(self) -> None:
        """Вывод экрана."""
        pygame.display.flip()

    def _main_loop(self) -> None:
        """Основной цикл игрового процесса."""
        while True:
            self.clock.tick(self.settings['graphics']['max_fps'])
            self._check_event()
            self._display_screen()

    def start(self) -> None:
        """Запуск игрового процесса."""
        self._main_loop()
