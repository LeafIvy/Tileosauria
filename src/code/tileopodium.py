from src.utils import *
from .creature import Creature


class Tileopodium(Creature):
    """Base class for flora"""

    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)
