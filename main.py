from engine import Engine

from engine.objects.test import TestObject


class Game(Engine):
    def __init__(self) -> None:
        TestObject()


if __name__ == '__main__':
    """Запуск игры."""
    Game().start()
