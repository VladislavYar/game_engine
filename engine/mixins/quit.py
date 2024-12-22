import sys

import pygame
from pygame.event import Event


class QuitMixin:
    """Mixin выхода из игрового процесса."""

    def _quit(self) -> None:
        """Выход из игрового процесса."""

    def _check_quit(self, events: dict[int, Event]) -> None:
        """Проверка выхода из игрового процесса.

        Args:
            events (dict[int, Event]): словарь событий.
        """
        if events.get(pygame.QUIT):
            self._quit()
            pygame.quit()
            sys.exit()
