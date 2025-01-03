from pygame.time import Clock

from engine.metaclasses.singleton import SingletonMeta


class GlobalClock(metaclass=SingletonMeta):
    """Класс глобальных часов игрового процесса."""

    def __init__(self) -> None:
        """Инициализация глобальных часов."""
        self._clock = Clock()

    def tick(self, framerate: float = 0) -> None:
        """Ограничивает FPS.

        Args:
            framerate (float, optional): количество FPS. По дефолту 0.
        """
        self._clock.tick(framerate)

    def get_fps(self) -> float:
        """Отдаёт текущий FPS.

        Returns:
            float: текущий FPS.
        """
        return self._clock.get_fps()
