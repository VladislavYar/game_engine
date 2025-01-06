class EngineMeta(type):
    """Метакласс Engine или его наследников."""

    def __new__(cls: 'EngineMeta', *args, **kwargs) -> type:
        """Вызывает метод класса установки настроек и инициализирует pygame.

        Args:
            cls (EngineMeta): метакласс Engine или его наследников.

        Returns:
            type: класс Engine или его наследник.
        """
        cls = super().__new__(cls, *args, **kwargs)
        cls._set_settings()
        return cls
