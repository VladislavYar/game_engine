import pygame

from engine.animations import Animation
from engine.animations.frames import Frame
from engine.actions import DynamicAction, Action
from engine.constants import Size


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
        pygame.display.set_caption(cls._settings['engine']['caption_title'])
        pygame.display.set_icon(pygame.image.load(cls._settings['engine']['path_icon']))

    @classmethod
    def _set_settings_audio(cls) -> None:
        """Устанавливает настройки аудио."""
        cls._audio.music_volume = cls._settings['audio']['music_volume']
        cls._audio.effects_volume = cls._settings['audio']['effects_volume']
        cls._audio.voices_volume = cls._settings['audio']['voices_volume']

    @classmethod
    def _set_settings_animations(cls) -> None:
        """Устанавливает настройки анимаций."""
        Frame.base_screen_size = Size(*cls._settings['engine']['base_screen_size_frame'])
        Animation.time_between = cls._settings['engine']['time_between_animation_frames']

    @classmethod
    def _set_settings_actions(cls) -> None:
        """Устанавливает настройки действий."""
        Action.time_between = cls._settings['engine']['time_between_animation_actions']
        DynamicAction.base_screen_size = Size(*cls._settings['engine']['base_screen_size_action'])

    @classmethod
    def _set_settings(cls) -> None:
        """Установка настроек игрового процесса."""
        cls._set_settings_display()
        cls._set_settings_audio()
        cls._set_settings_animations()
        cls._set_settings_actions()
