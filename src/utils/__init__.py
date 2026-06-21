import math

from .settings import *
from .timer import Timer


def get_quit(event):
    """Returns whether quit event was called or 'q' was pressed"""
    return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q)

def check_commands_pressed():
    """Returns the command combinations pressed"""
    keys0 = pg.key.get_pressed()
    keys1 = pg.key.get_just_pressed()
    if keys0[pg.K_F3]:
        if keys1[pg.K_g]:
            return 'draw-grid'
        elif keys1[pg.K_b]:
            return 'draw-border'
    return None