from pygame.time import Clock

from engine.metaclasses.singleton import SingletonMeta
from engine.settings import Settings


class GlobalClock(metaclass=SingletonMeta):
    """Класс глобальных часов игрового процесса."""

    def __init__(self) -> None:
        """Инициализация глобальных часов."""
        self._clock = Clock()
        settings: Settings = Settings()
        self.framerate = settings['graphics']['max_fps']
        self._coef_frame_time = settings['engine']['coef_frame_time']
        self.dt = 0
        self.frame_time = 0

    def tick(self) -> None:
        """Ограничивает FPS."""
        self.frame_time = self._clock.tick(self.framerate)
        self.dt = self.frame_time * self._coef_frame_time

    def get_fps(self) -> float:
        """Отдаёт текущий FPS.

        Returns:
            float: текущий FPS.
        """
        return self._clock.get_fps()
