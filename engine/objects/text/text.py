from pathlib import Path

from pygame import font as ft, Surface

from engine.constants import Color
from engine.constants.path import BasePathEnum
from engine.settings import Settings
from engine.objects.base_object import BaseObject
from engine.objects.groups import TextObjectsGroup


class Text(BaseObject):
    """Класс представляющий текст.

    Attributes:
        _settings (Settings): объект настроек игрового процесса.
    """

    ft.init()
    _settings: Settings = Settings()
    group = (TextObjectsGroup,)

    def __init__(
        self,
        size: int = _settings['engine']['text']['text_size'],
        text: str = None,
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
        super().__init__()
        self._font = self._get_font(size, font)
        self._color = color if color else Color(*self._settings['engine']['text']['text_color'])
        self._text = text
        self.image = self._font.render(self._text, True, self._color)
        self.rect = self.image.get_frect()

    def _get_font(self, size: int, font: str | Path | None = None) -> ft.Font:
        """Отдаёт ширифт.

        Args:
            size (int): размер ширифта.
            font (str | Path | None, optional): название ширифта или путь до него. По дефолту None.

        Returns:
            ft.Font: ширифт.
        """
        if isinstance(font, str):
            return ft.SysFont(font, size)
        elif isinstance(font, Path):
            return ft.Font(BasePathEnum.FONTS_PATH.value / font, size)
        elif font := self._settings['engine']['text']['path_fount']:
            return ft.SysFont(font, size)
        return ft.SysFont(self._settings['engine']['text']['name_fount'], size)

    def _update_text(self) -> None:
        """Обновляет текст."""
        rect_center = self.rect.center
        self.image = self._font.render(self._text, True, self._color)
        self.rect = self.image.get_rect()
        self.rect.center = rect_center

    @property
    def text(self) -> Surface:
        """Возвращает отображение текста.

        Returns:
            Surface: отображение текста.
        """
        return self.image

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
