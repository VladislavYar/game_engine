from dataclasses import dataclass


@dataclass
class Speed:
    """Dataclass скорости динамического объекта.

    Attributes:
        walk (int, optional): скорость ходьбы. По дефолту 0.
        run (int, optional): скорость бега. По дефолту 0.
        squat (int, optional): скорость в присяде. По дефолту 0.
    """

    walk: int = 0
    run: int = 0
    squat: int = 0


@dataclass
class Status:
    """Cтатусы объекта.

    Attributes:
        inactive (bool): статус неактивности.
        focus (bool): статус фокуса.
        jump (bool): статус прыжка.
        fall (bool): статус падения.
    """

    inactive: bool = False
    focus: bool = False
    jump: bool = False
    fall: bool = False
