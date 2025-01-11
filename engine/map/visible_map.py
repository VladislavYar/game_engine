from pygame import Surface

from engine.metaclasses.singleton import SingletonMeta
from engine.settings import Settings
from engine.constants import Size


class VisibleMap(Surface, metaclass=SingletonMeta):
    """Отображение видимой части карты."""

    def __init__(self) -> None:
        """Инициализация отображения видимой части карты."""
        settings: Settings = Settings()
        super().__init__(Size(*settings['engine']['base_visible_map_size']))
