import os
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator

from engine.utils.file import validate_format_file
from engine.constants.path import BasePathEnum
from engine.audio import Sound
from engine.events.constants import DEFAULT_EVENT
from engine.events import Events, Pressed
from engine.constants.empty import EMPTY_FRAME
from engine.animations.frames import Frame
from engine.utils.events import check_events
from engine.mixins.management import ManagementMixin
from engine.settings import Settings
from engine.animations.constants import Flip, ScaleRect, ScaleImage
from engine.time import GlobalClock


class Animation(ManagementMixin):
    """Класс представляющий анимацию.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        _global_clock (GlobalClock): объект глобальных часов игрового процесса.
        _empty_frame (Frame): пустое кадр.
        time_between (int): время между кадрами.
    """

    _settings: Settings = Settings()
    _global_clock: GlobalClock = GlobalClock()
    _empty_frame: Frame = EMPTY_FRAME
    time_between: int = _settings['engine']['time_between_animation_frames']

    def __init__(
        self,
        dir: str | Path,
        is_loop: bool = False,
        sound: Sound | None = None,
        time_between: int | None = None,
        flip: Flip = Flip(),
        scale_rect: ScaleRect = ScaleRect(),
        scale_image: ScaleImage = ScaleImage(_settings['engine']['scale_image'], _settings['engine']['scale_image']),
    ) -> None:
        """Инициализация анимации.

        Args:
            dir (str): директорию анимации.
            is_loop (bool, optional): зацикленная анимация. По дефолту False.
            sound (Sound | None, optional): аудио анимации. По дефолту None.
            time_between (int | None, optional): Время между кадрами фрейма. По дефолту None.
            flip (Flip, optional):
                Флаги отражения по вертикале, горизонтале и по направлению движения. Flip().
            scale_rect (ScaleRect, optional):
                scale rect. По дефолту ScaleRect().
            scale_image (ScaleImage, optional): scale image.
                По дефолту ScaleImage(_settings['engine']['scale_image'], _settings['engine']['scale_image']).
        """
        path = BasePathEnum.ANIMATIONS_PATH.value / dir
        path_images = self._get_full_path_images(path)
        self._frames = tuple(Frame(flip, scale_rect, scale_image, path_image) for path_image in path_images)
        self.is_loop = is_loop
        self.time_between = time_between if time_between else self.time_between
        self._sound = sound
        self._count_frames = len(self._frames)
        self._set_default_values()

    def _get_full_path_images(self, path: Path) -> list[str]:
        """Отдаёт список полных путей до изображений анимации.

        Args:
            path (Path): путь до папки с изображениямии анимации.

        Returns:
            list[str]: список полных путей до изображений.
        """
        path_images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if not os.path.isdir(full_path):
                validate_format_file(file, ('.png',))
                path_images.append(full_path)
        return path_images

    @property
    def frame(self) -> Frame:
        """Отдаёт следующий кадр анимации в зависимости от времени между кадрами.

        Returns:
            Frame: кадр анимации.
        """
        if not self.is_active or not len(self._frames):
            return self._empty_frame

        if self._count_frames == 1:
            return self._frames[0]

        frame_shift, self._elapsed = self._update_elapsed()
        self._active_frame += frame_shift
        if self._active_frame >= self._count_frames:
            self._active_frame = self._count_frames // self._active_frame - 1
            if not self.is_loop:
                self.stop()
        return self._frames[self._active_frame]


@dataclass
class EventsAnimation:
    """Dataclass представляющий связь events и анимации.

    Attributes:
        events (Events) events.
        animation (Animation): анимация.
    """

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

    def __init__(self, *args: EventsAnimation) -> None:
        """Инициализирует группу EventsAnimation."""
        self._events_animations = {events_animation: events_animation for events_animation in args}
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

    def __iter__(self) -> Iterator[EventsAnimation]:
        """Итератор по объектам EventsAnimation.

        Yields:
            Iterator: итератор по объектам EventsAnimation.
        """
        return iter(self._events_animations.values())


class AnimationGroup:
    """Класс представляющий группу анимаций."""

    def __init__(self, events_animations: EventsAnimationGroup) -> None:
        """Инициализация группы анимаций.

        Args:
            events_animations (EventsAnimationGroup): группа объектов EventsAnimation.
            obj (Object): игровой объект.
        """
        self._events_animations = events_animations
        self._default_animation = self._events_animations[DEFAULT_EVENT]
        self._current_animation = self._old_current_animation = self._default_animation

    def _check_old_current_animation(self, pressed: Pressed) -> None:
        """Проверка актуальности старой анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        events = self._old_current_animation.events
        if events != DEFAULT_EVENT and not check_events(events, pressed):
            self._old_current_animation.animation.stop()
            self._old_current_animation = self._default_animation

    def _check_current_animation(self, pressed: Pressed) -> None:
        """Проверка актуальности текущей анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        if not self._current_animation.animation.is_active or not check_events(
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
        if old_animation.is_loop and self._current_animation.animation != animation:
            self._current_animation.animation.stop()
            self._current_animation = events_animation
            animation.start()

    def _check_new_animation(self, pressed: Pressed) -> None:
        """Проверяет установку новой анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        for events_animation in self._events_animations:
            if check_events(events_animation.events, pressed):
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
