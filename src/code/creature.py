from src.utils import *


class Creature(pg.sprite.Sprite):
    """Base class for all creatures (flora and fauna)"""
    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        # base settings
        self.image = surf
        self.rect  = self.image.get_frect(topleft=pos)

        # base attributes
        self.health      = 100
        self.comfort_lvl = 100
        self.hungry_lvl  = 0
        self.thirst_lvl  = 0
        self.age         = 0
