import pygame

from engine.animations import Animation


class SetSettingsMixin:
    """Mixin установки настроек игрового процесса."""

    def _set_settings_display(self) -> None:
        """Устанавливает настройки дисплея."""
        flags = pygame.FULLSCREEN if self.settings['graphics']['fullscreen'] else pygame.SHOWN
        self.display = pygame.display.set_mode(
            self.settings['graphics']['screen_resolution'],
            flags,
        )
        pygame.display.set_caption(self.settings['engine']['caption_title'])
        pygame.display.set_icon(pygame.image.load(self.settings['engine']['path_icon']))

    def _set_settings_audio(self) -> None:
        """Устанавливает настройки аудио."""
        self.audio.music_volume = self.settings['audio']['music_volume']
        self.audio.effects_volume = self.settings['audio']['effects_volume']
        self.audio.voices_volume = self.settings['audio']['voices_volume']

    def _set_settings_animations(self) -> None:
        """Устанавливает настройки анимаций."""
        Animation.time_between_frames = self.settings['engine']['time_between_animation_frames']
        Animation.audio_engine = self.audio

    def _set_settings(self) -> None:
        """Установка настроек игрового процесса."""
        self._set_settings_display()
        self._set_settings_audio()
        self._set_settings_animations()
