import pygame

from engine.settings import Settings


class SetSettingsMixin:
    """Mixin установки настроек игрового процесса."""

    def _set_settings_display(self) -> None:
        """Устанавливает настройки дисплея."""
        flags = pygame.OPENGL
        if self.settings['fullscreen']:
            flags |= pygame.FULLSCREEN
        self.display = pygame.display.set_mode(
            self.settings['screen_resolution'],
            flags,
        )
        pygame.display.set_caption(self.settings['caption_title'])
        try:
            icon = pygame.image.load(self.settings['path_icon'])
            pygame.display.set_icon(icon)
        except Exception:
            pass

    def _set_settings(self) -> None:
        """Установка настроек игрового процесса."""
        self.settings = Settings()
        self._set_settings_display()
