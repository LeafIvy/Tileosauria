from src.utils import *
from .creature import Creature


class Tileopodium(Creature):
    """Base class for flora"""

    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)

        self.is_passable = False     # Plants can be passed through, but not trees, default False
        self.tile_cost   = math.inf  # Cost to walk through it for A*, trees are impassable