from pathlib import Path
from functools import lru_cache

from pygame import font as ft, Surface

from engine.constants import Color, Size
from engine.constants.path import BasePathEnum
from engine.settings import Settings


class Text:
    """Класс представляющий текст.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
        base_screen_size (Size): базовый размер экрана для вычисления размера текста.
        base_visible_map_size (Size): базовый размер видимой карты.
    """

    _settings = Settings()
    base_screen_size: Size = Size(*_settings['engine']['base_screen_size_text'])
    base_visible_map_size: Size = Size(*_settings['engine']['base_visible_map_size'])

    def __init__(
        self,
        size: int = _settings['engine']['text_size'],
        text: str | None = None,
        color: Color | None = None,
        font: str | Path | None = None,
    ) -> None:
        """Инициализация текста.

        Args:
            size (int, optional): размер текста. По дефолту _settings['engine']['text_size'].
            text (str | None, optional): текст. По дефолту None.
            color (Color | None, optional): цвет текста. По дефолту None.
            font (str | font | None, optional): ширифт текста или путь до него в папке resources/fonts. По дефолту None.
        """
        self._font = self._get_font(size, font)
        self._color = color if color else Color(*self._settings['engine']['text_color'])
        self._text = text
        self._surface = self._font.render(self._text, True, self._color)
        self.rect = self._surface.get_frect()

    @classmethod
    @lru_cache
    def _get_coef(cls, width: int, height: int) -> tuple[float, float]:
        """Отдаёт коэффициент разности разрешения экрана от базового.

        Args:
            width (int): ширина разрешения экрана.
            height (int): высота разрешения экрана.
        Returns:
            tuple[float, float]: коэффициент разности разрешения экрана от базового.
        """
        return width / cls.base_screen_size.width, height / cls.base_screen_size.height

    def _get_font(self, size: int, font: str | Path | None = None) -> ft.Font:
        """Отдаёт ширифт.

        Args:
            size (int): размер ширифта.
            font (str | Path | None, optional): название ширифта или путь до него. По дефолту None.

        Returns:
            ft.Font: ширифт.
        """
        _, coef_height = self._get_coef(*self.base_visible_map_size)
        if isinstance(font, str):
            return ft.SysFont(font, int(size * coef_height))
        elif isinstance(font, Path):
            return ft.Font(BasePathEnum.FONTS_PATH.value / font, int(size * coef_height))
        elif font := self._settings['engine']['path_fount']:
            return ft.SysFont(font, int(size * coef_height))
        return ft.SysFont(self._settings['engine']['name_fount'], int(size * coef_height))

    def _update_text(self) -> None:
        """Обновляет текст."""
        rect_center = self.rect.center
        self._surface = self._font.render(self._text, True, self._color)
        self.rect = self._surface
        self.rect.center = rect_center

    @property
    def text(self) -> Surface:
        """Возвращает отображение текста.

        Returns:
            Surface: отображение текста.
        """
        return self._surface

    @text.setter
    def text(self, value: str) -> None:
        """Устанавливает новый текст.

        Args:
            value (str): текст.
        """
        self._text = value
        self._update_text()

    @property
    def color(self) -> Color:
        """Возвращает цвет текста.

        Returns:
            Color: цвет текста.
        """
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        """Устанавливает новый цвет текста.

        Args:
            value (Color): новый цвет текста.
        """
        self._color = value
        self._update_text()
