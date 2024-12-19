import pygame


class SetSettingsMixin:
    """Mixin установки настроек игрового процесса."""

    def _set_settings_display(self) -> None:
        """Устанавливает настройки дисплея."""
        flags = pygame.OPENGL
        if self.settings['graphics']['fullscreen']:
            flags |= pygame.FULLSCREEN
        self.display = pygame.display.set_mode(
            self.settings['graphics']['screen_resolution'],
            flags,
        )
        pygame.display.set_caption(self.settings['engine']['caption_title'])
        icon = pygame.image.load(self.settings['engine']['path_icon'])
        pygame.display.set_icon(icon)

    def _set_settings_audio(self) -> None:
        """Устанавливает настройки аудио."""
        self.audio.music_volume = self.settings['audio']['music_volume']
        self.audio.effects_volume = self.settings['audio']['effects_volume']
        self.audio.voices_volume = self.settings['audio']['voices_volume']

    def _set_settings(self) -> None:
        """Установка настроек игрового процесса."""
        self._set_settings_display()
        self._set_settings_audio()
