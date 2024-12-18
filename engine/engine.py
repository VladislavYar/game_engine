import pygame

from engine.mixins import QuitMixin, SetSettingsMixin


class Engine(QuitMixin, SetSettingsMixin):
    """Игровой движок."""

    def __init__(self) -> None:
        """Инициализация игрового движка."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self._set_settings()

    def _check_event(self) -> None:
        """Проверка событий."""
        self._check_quit()

    def _display_screen(self) -> None:
        """Вывод экрана."""
        pygame.display.flip()

    def _main_cycle(self) -> None:
        """Основной цикл игрового процесса."""
        while True:
            self.clock.tick(self.settings['max_fps'])
            self._check_event()
            self._display_screen()
            print(self.clock.get_fps())

    def start(self) -> None:
        """Запуск игрового процесса."""
        self._main_cycle()
