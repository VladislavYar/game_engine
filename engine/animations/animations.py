import os
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator, TYPE_CHECKING

from pygame import image, transform

from engine.utils.file import validate_format_file
from engine.constants.path import BasePathEnum
from engine.audio import Audio
from engine.events.constants import DEFAULT_EVENT
from engine.events import Events, Pressed
from engine.constants.empty import EMPTY_FRAME
from engine.animations.frames import Frame
from engine.utils.events import check_events
from engine.mixins.management import ManagementMixin
from engine.animations.constants import OBJ_WRITING_ONLY

if TYPE_CHECKING:
    from engine.objects import BaseObject


class Animation(ManagementMixin):
    """Класс представляющий анимацию.

    Attributes:
        time_between (int): время между кадрами.
        _audio (Audio): объект для работы с аудио.
        _empty_frame (Frame): пустое кадр.
    """

    time_between: int
    _audio: Audio = Audio()
    _empty_frame: Frame = EMPTY_FRAME

    def __init__(
        self,
        dir: str | Path,
        is_loop: bool = False,
        sound: str | None = None,
        time_between: int | None = None,
        flip_x: bool = False,
        flip_y: bool = False,
        flip_by_derection: bool = False,
    ) -> None:
        """Инициализация анимации.

        Args:
            dir (str): директорию анимации.
            is_loop (bool, optional): зацикленная анимация. По дефолту False.
            sound (str | None, optional): название файла аудио анимации. По дефолту None.
            time_between (int | None, optional): Время между кадрами фрейма. По дефолту None.
            flip_x (bool, optional): Флаг отражения по горизонтале. По дефолту False.
            flip_y (bool, optional): Флаг отражения по вертикале. По дефолту False.
            flip_by_derection (bool, optional): Флаг поворота анимации по направлению движения. По дефолту False.
        """
        path = BasePathEnum.ANIMATIONS_PATH.value / dir
        images = self._get_full_path_images(path)
        self._frames = self._get_frames(images, flip_x, flip_y)
        self.is_loop = is_loop
        self._flip_by_derection = flip_by_derection
        self.time_between = time_between if time_between else self.time_between
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

    def _get_frames(self, images: list[str], flip_x: bool, flip_y: bool) -> tuple[Frame]:
        """Отдаёт список кадров.

        Args:
            images (list[str]): пути до изображений.
            flip_x (bool): Флаг отражения по горизонтале.
            flip_y (bool): Флаг отражения по вертикале.

        Raises:
            ValueError: ошибка валидации при отсутвии кадров.

        Returns:
            tuple[Frame]: список кадров.
        """
        frames = []
        for img in images:
            img = transform.flip(image.load(img).convert_alpha(), flip_x, flip_y)
            frames.append(Frame(img))
        return tuple(frames)

    def scale(self) -> None:
        """Изменяет размер кадров анимации под текущий размер экрана."""
        for frame in self._frames:
            frame.scale()

    def _get_rotation_frame(self, index: int) -> Frame:
        """Отдаёт frame анимации с проверкой на поворот.

        Args:
            images (int): индекс frame.

        Returns:
            Frame: frame анимации.
        """
        frame = self._frames[index]
        if self._flip_by_derection:
            frame.direction = self._obj.direction
        return frame

    @property
    def frame(self) -> Frame:
        """Отдаёт следующий кадр анимации в зависимости от времени между кадрами.

        Args:
            obj (BaseObject): игровой объект.

        Returns:
            Frame: кадр анимации.
        """
        if not self.is_active or not len(self._frames):
            return self._empty_frame

        if self._count_frames == 1:
            return self._get_rotation_frame(0)

        frame_shift, self._elapsed = self._update_elapsed()
        self._active_frame += frame_shift
        if self._active_frame >= self._count_frames:
            self._active_frame = self._count_frames // self._active_frame - 1
            if not self.is_loop:
                self.stop()
                return self._empty_frame
        return self._get_rotation_frame(self._active_frame)

    @property
    def obj(self) -> None:
        raise OBJ_WRITING_ONLY

    @obj.setter
    def obj(self, obj: 'BaseObject') -> None:
        """Добавляет игровой объект анимации.
        Args:
            obj (BaseObject): игровой объект.
        """
        self._obj = obj


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

    def __iter__(self) -> Iterator[EventsAnimation]:
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
        obj: 'BaseObject',
    ) -> None:
        """Инициализация группы анимаций.

        Args:
            events_animations (EventsAnimationGroup): группа объектов EventsAnimation.
            obj (BaseObject): игровой объект.
        """
        self._events_animations = events_animations
        self._default_animation = self._events_animations[DEFAULT_EVENT]
        self._current_animation = self._old_current_animation = self._default_animation
        for events_animation in self._events_animations:
            events_animation.animation.obj = obj

    def _check_old_current_animation(self, pressed: Pressed) -> None:
        """Проверка актуальности старой анимации.

        Args:
            pressed (Pressed): объект состояния кнопок, коллизии и активности объекта.
        """
        events = self._old_current_animation.events
        if events != DEFAULT_EVENT and not check_events(events, pressed):
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
        if old_animation.is_loop and old_animation != animation:
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

    def scale(self) -> None:
        """Изменяет размер кадров анимаций под текущий размер экрана."""
        for events_animation in self._events_animations:
            events_animation.animation.scale()

    @property
    def frame(self) -> Frame:
        """Отдаёт следующий кадр анимации.

        Returns:
            Frame: кадр анимации.
        """
        return self._current_animation.animation.frame
