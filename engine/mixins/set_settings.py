import pygame


class SetSettingsMixin:
    """Mixin установки настроек игрового процесса."""

    @classmethod
    def _set_settings_display(cls) -> None:
        """Устанавливает настройки дисплея."""
        flags = pygame.FULLSCREEN if cls._settings['graphics']['fullscreen'] else pygame.SHOWN
        cls.display = pygame.display.set_mode(
            cls._settings['graphics']['screen_resolution'],
            flags,
        )
        cls.visible_map = pygame.Surface(cls._settings['engine']['base_visible_map_size'])
        pygame.display.set_caption(cls._settings['engine']['caption_title'])
        pygame.display.set_icon(pygame.image.load(cls._settings['engine']['path_icon']))

    @classmethod
    def _set_settings_audio(cls) -> None:
        """Устанавливает настройки аудио."""
        cls._audio.music_volume = cls._settings['audio']['music_volume']
        cls._audio.effects_volume = cls._settings['audio']['effects_volume']
        cls._audio.voices_volume = cls._settings['audio']['voices_volume']

    @classmethod
    def _set_settings(cls) -> None:
        """Установка настроек игрового процесса."""
        cls._set_settings_display()
        cls._set_settings_audio()
