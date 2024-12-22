import os
from pathlib import Path
from dataclasses import dataclass

from pygame import key, surface, time, image as img

from engine.utils.file import validate_format_file
from engine.constants import BasePathEnum
from engine.audio import Audio
from engine.animations.constants import DEFAULT_EVENT_ANIMATION


class Animation:
    """Класс представляющий анимацию.

    Attributes:
        time_between_frames (int): время между кадрами.
    """

    time_between_frames: int
    audio_engine: Audio

    def __init__(self, dir: str | Path, is_loop: bool = False, audio: str | None = None) -> None:
        """Инициализация анимации.

        Args:
            dir (str): директорию анимации.
            is_loop (bool): зацикленная анимация. По дефолту False.
            audio (str | None): название файла аудио анимации. По дефолту None.
        """
        path = BasePathEnum.ANIMATIONS_PATH.value / dir
        images = self._get_full_path_images(path)
        self._frames = self._get_frames(images)
        self.is_loop = is_loop
        self._audio = self.audio_engine.load_effect(audio) if audio else None
        self._count_frames = len(self._frames)
        self._set_default_values()

    def _set_default_values(self) -> None:
        """Устанавливает дефолтные значения."""
        self._active_frame = 0
        self._elapsed = 0
        self._ticks = time.get_ticks()
        self.is_active = False
        if self._audio and self.is_loop:
            self._audio.stop()

    def start(self) -> None:
        """Запускает анимацию."""
        self._set_default_values()
        self.is_active = True
        if self._audio:
            self._audio.play(loops=-1 if self.is_loop else 0)

    def stop(self) -> None:
        """Останавливает анимацию."""
        self._set_default_values()

    def _get_full_path_images(self, path: Path) -> list[str]:
        """Отдаёт список полных путей до изображений анимации.

        Args:
            path (Path): путь до папки с изображениямии анимации.

        Returns:
            list[str]: список полных путей до изображений.
        """
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if not os.path.isdir(full_path):
                validate_format_file(file, ('png',))
                images.append(full_path)
        return images

    def _get_frames(self, images: list[str]) -> list[surface.Surface]:
        """Отдаёт список кадров.

        Args:
            images (list[str]): пути до изображений.

        Raises:
            ValueError: ошибка валидации при отсутвии кадров.

        Returns:
            list[surface.Surface]: список кадров.
        """
        frames = []
        for image in images:
            frame = img.load(image).convert_alpha()
            frames.append(frame)
        if not len(frames):
            raise ValueError('Анимация должна содержать хотя бы один кадр.')
        return frames

    @property
    def frame(self) -> surface.Surface:
        """Отдаёт следующий кадр анимации в зависимости от времени между кадрами.

        Returns:
            surface.Surface: кадр анимации.
        """
        if not self.is_active:
            return surface.Surface((0, 0))

        if self._count_frames == 1:
            return self._frames[0]

        frame = self._frames[self._active_frame]
        self._elapsed += time.get_ticks() - self._ticks
        self._ticks = time.get_ticks()
        if self._elapsed < self.time_between_frames:
            return frame
        self._active_frame += self._elapsed // self.time_between_frames
        self._elapsed = self._elapsed % self.time_between_frames
        if self._active_frame >= self._count_frames:
            self._active_frame = self._count_frames // self._active_frame - 1
            if not self.is_loop:
                self.stop()
                return surface.Surface((0, 0))
        return frame


@dataclass
class EventsAnimation:
    """Dataclass представляющий связь кортежа events и анимации."""

    events: tuple[int, ...]
    animation: Animation


class AnimationGroup:
    """Класс представляющий группу анимаций."""

    def __init__(
        self,
        events_animations: list[EventsAnimation],
        default_animation: Animation,
    ) -> None:
        """Инициализация группы анимаций.

        Args:
            events_animations (list[EventsAnimation]): список объектов EventsAnimation.
            default_animation (Animation): дефолтная анимация.
        """
        self._events_animations = events_animations
        self._default_animation = EventsAnimation(DEFAULT_EVENT_ANIMATION, default_animation)
        self._current_animation: EventsAnimation = self._default_animation
        self._old_current_animation: EventsAnimation = self._default_animation

    def _check_events(self, events: tuple[int, ...]) -> bool:
        """Проверка событий.

        Args:
            events (tuple[int, ...]): события для проверки.

        Returns:
            bool: флаг соответсвия событиям.
        """
        if events == DEFAULT_EVENT_ANIMATION:
            return True
        pressed = key.get_pressed()
        return all([pressed[event] for event in events])

    def _check_old_current_animation(self) -> None:
        """Проверка актуальности старой анимации."""
        events = self._old_current_animation.events
        if events == DEFAULT_EVENT_ANIMATION:
            return
        if not self._check_events(events):
            self._old_current_animation = self._default_animation

    def _check_current_animation(self) -> None:
        """Проверка актуальности текущей анимации."""
        if not self._current_animation.animation.is_active or not self._check_events(self._current_animation.events):
            self._old_current_animation = self._current_animation
            self._current_animation.animation.stop()
            self._default_animation.animation.start()
            self._current_animation = self._default_animation

    def _set_new_animations(self, events_animation: EventsAnimation) -> None:
        """Устанавливает новую анимацию.

        Args:
            events_animation (EventsAnimation): объект EventsAnimation.
        """
        animation = events_animation.animation
        old_animation = self._old_current_animation.animation
        if not old_animation.is_loop and old_animation == animation:
            return
        self._current_animation = events_animation
        if not animation.is_active:
            animation.start()

    def events(self) -> None:
        """Проверка событий, совершённых пользователем."""
        self._check_old_current_animation()
        self._check_current_animation()
        for events_animation in self._events_animations:
            if self._check_events(events_animation.events):
                self._set_new_animations(events_animation)
                break

    @property
    def frame(self) -> surface.Surface:
        """Отдаёт следующий кадр анимации.

        Returns:
            surface.Surface: кадр анимации.
        """
        return self._current_animation.animation.frame