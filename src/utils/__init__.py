import math

from .settings import *
from .timer import Timer


def get_quit(event):
    """Returns whether quit event was called or 'q' was pressed"""
    return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q)

def check_commands_pressed(event):
    keys = pg.key.get_just_pressed()
    if keys[pg.K_F3]:
        if keys[pg.K_g]:
            return 'draw-grid'
        elif keys[pg.K_b]:
            return 'draw-border'
    return None