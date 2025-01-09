from engine.animations.constants import Flip, ScaleRect, ScaleImage
from engine.animations.frames import Frame


EMPTY_FRAME = Frame(Flip(), ScaleRect(), ScaleImage())
EMPTY_FRAME.after_init()
