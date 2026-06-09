from src.utils import *
from .creature import Creature


class Tileosaur(Creature):
    """Base class for fauna"""
    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)

