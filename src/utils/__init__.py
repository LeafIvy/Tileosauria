from .settings import *


def get_quit(event):
    """Returns whether quit event was called or 'q' was pressed"""
    return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q)