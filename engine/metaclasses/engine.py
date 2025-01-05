from pygame import init


class EngineMeta(type):
    """Метакласс Engine или его наследников."""

    def __new__(cls: 'EngineMeta', *arg, **kwarg) -> type:
        """Вызывает метод класса установки настроек и инициализирует pygame.

        Args:
            cls (EngineMeta): метакласс Engine или его наследников.

        Returns:
            type: класс Engine или его наследник.
        """
        cls = super().__new__(cls, *arg, **kwarg)
        init()
        cls._set_settings()
        return cls
