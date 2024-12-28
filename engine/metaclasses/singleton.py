from pygame import key


class SingletonMeta(type):
    """Метакласс, реализующий функционал паттерна синглтон.

    Attributes:
        _instances (dict[type: object]): словарь для хранения уже созданных объектов классов.
    """

    _instances: dict[type, object] = {}

    def __call__(cls: type, *args, **kwargs) -> object:
        """Создаёт объект класса или отдаёт уже созданный.

        Args:
            cls (type): класс создаваемого или созданного объекта.

        Returns:
            object: созданный объект.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class PressedSingletonMeta(SingletonMeta):
    """Метакласс, реализующий функционал паттерна синглтон для класса Pressed."""

    def __call__(cls: type, *args, **kwargs) -> object:
        """Создаёт объект класса или отдаёт уже созданный.
        А так же обновляет переменную _pressed объекта.

        Args:
            cls (type): класс создаваемого или созданного объекта.

        Returns:
            object: созданный объект.
        """
        obj = super().__call__(*args, **kwargs)
        obj._pressed = key.get_pressed()
        return obj
