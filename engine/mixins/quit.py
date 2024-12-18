import sys

import pygame


class QuitMixin:
    """Mixin выхода из игрового процесса."""

    def _quit(self) -> None:
        """Выход из игрового процесса."""

    def _check_quit(self) -> None:
        """Проверка выхода из игрового процесса."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
                sys.exit()
