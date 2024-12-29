from functools import lru_cache

from pygame import display, transform, Surface, mask

from engine.constants import Size


class BaseFrame:
    """Класс представляющий базовый кадр."""

    def __init__(self, image: Surface) -> None:
        """Инициализация базового кадра.

        Args:
            image (Surface): изображение кадра анимации.
        """
        self._set_data_frame(image)
        self._original_image = image
        self._original_size = Size(self.rect.size[0], self.rect.size[1])
        self.scale()

    def _set_data_frame(self, image: Surface) -> None:
        """Устанавливает данные по кадру анимации.

        Args:
            image (Surface): изображение кадра анимации.
        """
        self.image = image
        self.rect = image.get_rect()
        self.mask = mask.from_surface(image)

    def scale(self) -> None:
        """Изменяет размер кадра анимации под текущий размер экрана."""


class EmptyFrame(BaseFrame):
    """Класс представляющий пустой кадр."""


class Frame(BaseFrame):
    """Класс представляющий кадр анимации.

    Attributes:
        base_screen_size Size: базовый размер экрана для вычисления размера кадра.
    """

    base_screen_size: Size

    def _get_sreen_resolution(self) -> tuple[int, int]:
        """Отдаёт текущее разрешение экрана.

        Returns:
            tuple[int, int]: ширина и высота разрешения экрана.
        """
        display_info = display.Info()
        return display_info.current_w, display_info.current_h

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

    def scale(self) -> None:
        """Изменяет размер кадра анимации под текущий размер экрана."""
        coef_width, coef_height = self._get_coef(*self._get_sreen_resolution())
        size = Size(self._original_size.width * coef_width, self._original_size.height * coef_height)
        self._set_data_frame(transform.scale(self._original_image.copy(), size))
