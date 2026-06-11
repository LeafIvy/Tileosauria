from src.utils import *
from .creature import Creature


class Tileosaur(Creature):
    """Base class for fauna"""
    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)
        self.set_move_delay_timer(3)

        self.direction = pg.Vector2()

    def set_move_delay_timer(self, speed):
        """Creates the move_delay Timer by calculating delay based on tiles per second as given

            speed = tiles per second
        """
        self.move_delay = Timer(1000/speed)
        pass

    def move(self, target):
        """Uses A* to pathfind to target

        target = position of center of tile
        """
        target_centerx, target_centery = target

