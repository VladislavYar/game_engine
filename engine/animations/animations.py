import os
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator

from pygame import surface, time, image, rect, mask, SRCALPHA

from engine.utils.file import validate_format_file
from engine.constants import BasePathEnum
from engine.audio import Audio
from engine.events.constants import DEFAULT_EVENT
from engine.events import Events, Pressed


@dataclass
class Frame:
    """Dataclass представляющий кадр анимации.

    Attributes:
        image (surface.Surface): изображение кадра анимации.
        rect (rect.Rect): rect кадра анимации.
        mask (mask.Mask): маска кадра анимации.
    """

    image: surface.Surface
    rect: rect.Rect
    mask: mask.Mask


class Animation:
    """Класс представляющий анимацию.

    Attributes:
        time_between_frames (int): время между кадрами.
        _audio (Audio): объект для работы с аудио.
        _no_frame (Frame): пустое отображение.
    """

    time_between_frames: int
    _audio: Audio = Audio()
    _no_frame: Frame = Frame(
        surface.Surface((0, 0), SRCALPHA),
        surface.Surface((0, 0), SRCALPHA).get_rect(),
        mask.from_surface(surface.Surface((0, 0), SRCALPHA)),
    )

    def __init__(self, dir: str | Path, is_loop: bool = False, sound: str | None = None) -> None:
        """Инициализация анимации.

        Args:
            dir (str): директорию анимации.
            is_loop (bool): зацикленная анимация. По дефолту False.
            sound (str | None): название файла аудио анимации. По дефолту None.
        """
        path = BasePathEnum.ANIMATIONS_PATH.value / dir
        images = self._get_full_path_images(path)
        self._frames = self._get_frames(images)
        self.is_loop = is_loop
        self._sound = self._audio.load_effect(sound) if sound else None
        self._count_frames = len(self._frames)
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

    def _get_frames(self, images: list[str]) -> tuple[Frame]:
        """Отдаёт список кадров.

        Args:
            images (list[str]): пути до изображений.

        Raises:
            ValueError: ошибка валидации при отсутвии кадров.

        Returns:
            tuple[Frame]: список кадров.
        """
        frames = []
        for img in images:
            img = image.load(img).convert_alpha()
            img_rect = img.get_rect()
            img_mask = mask.from_surface(img)
            frames.append(Frame(img, img_rect, img_mask))
        if not len(frames):
            raise ValueError('Анимация должна содержать хотя бы один кадр.')
        return tuple(frames)

    def _set_default_values(self) -> None:
        """Устанавливает дефолтные значения."""
        self._active_frame = 0
        self._elapsed = 0
        self._ticks = time.get_ticks()
        self.is_active = False
        if self._sound and self.is_loop:
            self._sound.stop()

    def restart(self) -> None:
        """Перезапускает анимацию."""
        self._set_default_values()
        self.is_active = True
        if self._sound:
            self._sound.play(loops=-1 if self.is_loop else 0)

    def start(self) -> None:
        """Запускает анимацию, если не активна."""
        if not self.is_active:
            self.restart()

    def stop(self) -> None:
        """Останавливает анимацию, если активна."""
        if self.is_active:
            self._set_default_values()

    @property
    def frame(self) -> surface.Surface:
        """Отдаёт следующий кадр анимации в зависимости от времени между кадрами.

        Returns:
            surface.Surface: кадр анимации.
        """
        if not self.is_active:
            return self._no_frame

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
                return self._no_frame
        return frame


@dataclass
class EventsAnimation:
    """Dataclass представляющий связь events и анимации."""

    events: Events
    animation: Animation

    def __eq__(self, other: Events) -> bool:
        """Проверка на равество объектов.

        Args:
            other (Events): сравниваемый объект.

        Raises:
            TypeError: ошибка не верного типа объекта.

        Returns:
            bool: результат сравнения.
        """
        if not isinstance(other, Events):
            raise TypeError('Сравниваемый объект должен быть типа Events')
        return self.events == other

    def __hash__(self) -> int:
        """Создаёт хэш из множества events.

        Returns:
            int: хэш.
        """
        return hash(self.events)


class EventsAnimationGroup:
    """Класс группы EventsAnimation."""

    def __init__(self, *arg: EventsAnimation) -> None:
        """Инициализирует группу EventsAnimation."""
        self._events_animations = {events_animation: events_animation for events_animation in arg}
        if not self._events_animations[DEFAULT_EVENT]:
            raise ValueError('Дефолтная анимация является обязательной.')

    def __getitem__(self, key: Events) -> EventsAnimation | None:
        """Отдаёт связь events и анимации по ключу.

        Args:
            key (Events): ключ events.

        Returns:
            EventsAnimation | None: связь events и анимации.
        """
        return self._events_animations.get(key)

    def __iter__(self) -> Iterator:
        """Итератор по объектам EventsAnimation.

        Yields:
            Iterator: итератор по объектам EventsAnimation.
        """
        return iter(self._events_animations.values())


class AnimationGroup:
    """Класс представляющий группу анимаций."""

    def __init__(
        self,
        events_animations: EventsAnimationGroup,
    ) -> None:
        """Инициализация группы анимаций.

        Args:
            events_animations (EventsAnimationGroup): группа объектов EventsAnimation.
        """
        self._events_animations = events_animations
        self._default_animation = self._events_animations[DEFAULT_EVENT]
        self._current_animation = self._old_current_animation = self._default_animation

    def _check_events(self, events: Events, pressed: Pressed) -> bool:
        """Проверка событий.

        Args:
            events (Events): события для проверки.
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.

        Returns:
            bool: флаг соответсвия событиям.
        """
        return events == DEFAULT_EVENT or all([pressed[event] for event in events])

    def _check_old_current_animation(self, pressed: Pressed) -> None:
        """Проверка актуальности старой анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        events = self._old_current_animation.events
        if events != DEFAULT_EVENT and not self._check_events(events, pressed):
            self._old_current_animation = self._default_animation

    def _check_current_animation(self, pressed: Pressed) -> None:
        """Проверка актуальности текущей анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        if not self._current_animation.animation.is_active or not self._check_events(
            self._current_animation.events, pressed
        ):
            self._current_animation.animation.stop()
            self._default_animation.animation.restart()
            self._old_current_animation, self._current_animation = self._current_animation, self._default_animation

    def _set_new_animations(self, events_animation: EventsAnimation) -> None:
        """Устанавливает новую анимацию.

        Args:
            events_animation (EventsAnimation): объект EventsAnimation.
        """
        animation = events_animation.animation
        old_animation = self._old_current_animation.animation
        if old_animation.is_loop and old_animation != animation:
            self._current_animation = events_animation
            animation.start()

    def _check_new_animation(self, pressed: Pressed) -> None:
        """Проверяет установку новой анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        for events_animation in self._events_animations:
            if self._check_events(events_animation.events, pressed):
                self._set_new_animations(events_animation)
                break

    def events(self, pressed: Pressed) -> None:
        """Проверка событий, совершённых пользователем.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        self._check_old_current_animation(pressed)
        self._check_current_animation(pressed)
        self._check_new_animation(pressed)

    @property
    def frame(self) -> Frame:
        """Отдаёт следующий кадр анимации.

        Returns:
            Frame: кадр анимации.
        """
        return self._current_animation.animation.frame
