from .settings import *
from .timer import Timer
import math

class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


def get_quit(event):
    """Returns whether quit event was called or 'q' was pressed"""
    return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q)