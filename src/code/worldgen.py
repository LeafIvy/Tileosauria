import noise

from src.utils import *


class WorldGen:
    def __init__(self, size):
        self.size = size
        self.world = {}

    def __iter__(self):
        return iter(self.world.items())

    def generate_perlin_noise(self, scale=100.0, octaves=6, persistance=0.3, lacunarity=2.0):
        for y in range(self.size):
            for x in range(self.size):
                dx = x / scale
                dy = y /scale
                noise_value = noise.pnoise2(
                    dx,
                    dy,
                    octaves=octaves,
                    persistence=persistance,
                    lacunarity=lacunarity
                )
                if noise_value < -0.5:
                    color = 'blue'
                else: color = 'green'
                self.world[(x, y)] = Tile((x, y), (TILE_SIZE, TILE_SIZE), color)

class Tile(pg.FRect):
    def __init__(self, pos, size, color):
        super().__init__(pos, size)
        self.color = color
