from src.utils import *
from .creature import Creature


class Tileosaur(Creature):
    """Base class for fauna"""
    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)
        self.set_move_delay_timer(3)

        self.direction = pg.Vector2()
        self.range = 5
        self.nodes = []

    def set_move_delay_timer(self, speed):
        """
        Creates the move_delay Timer by calculating delay based on tiles per second as given

        speed = tiles per second
        """
        self.move_delay = Timer(1000/speed)

    def create_nodes(self):
        """Create TileNodes used for pathfinding around the sprite"""
        centerx = [x for x in range(int(self.rect.centerx - self.range * TILE_SIZE),
                                    int(self.rect.centerx + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centery = [y for y in range(int(self.rect.centery - self.range * TILE_SIZE),
                                    int(self.rect.centery + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centers = [(x, y) for x in centerx for y in centery]
        for pos in centers: self.nodes.append(TileNode(pos, math.inf))

    def move(self, target):
        """Uses A* to pathfind to target

        target = position of center of tile
        """
        target_centerx, target_centery = target

class TileNode(pg.FRect):
    def __init__(self, pos, cost):
        super().__init__(pos, (TILE_SIZE + 5,) * 2)
        self.parent = None
        self.cost = cost    # cost to target, i.e, h(n)
        self.adjacent_tiles = {}    # dictionary of form {TileNode: heuristic} where heuristic is g(n)
