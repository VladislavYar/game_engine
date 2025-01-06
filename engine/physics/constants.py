from engine.constants.direction import DirectionGroupEnum


SING_X_Y = {
    DirectionGroupEnum.UP: (0, -1),
    DirectionGroupEnum.DOWN: (0, 1),
    DirectionGroupEnum.LEFT: (-1, 0),
    DirectionGroupEnum.RIGHT: (1, 0),
    DirectionGroupEnum.UP_RIGHT: (1, -1),
    DirectionGroupEnum.UP_LEFT: (-1, -1),
    DirectionGroupEnum.DOWN_LEFT: (-1, 1),
    DirectionGroupEnum.DOWN_RIGHT: (1, 1),
}
