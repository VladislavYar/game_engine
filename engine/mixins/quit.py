import sys

import pygame
from pygame.event import Event


class QuitMixin:
    """Mixin выхода из игрового процесса."""

    def _quit(self) -> None:
        """Выход из игрового процесса."""

    def _check_quit(self, events: list[Event]) -> None:
        """Проверка выхода из игрового процесса.

        Args:
            events (list[Event]): список событий.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._quit()
                sys.exit()
