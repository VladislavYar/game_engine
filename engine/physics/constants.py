from engine.constants.direction import DirectionGroupEnum
from engine.settings import Settings


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

COEF_DROP_CHECK = Settings()['engine']['coef_drop_check']
