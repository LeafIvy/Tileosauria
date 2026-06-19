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
                    lacunarity=lacunarity,
                    base=69
                )
                if noise_value < -0.5:
                    color = 'blue'
                else: color = 'black'
                self.world[(x, y)] = Tile((x, y), color)

class Tile:
    def __init__(self, pos, color):
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_frect(topleft=pos)
        self.rect.centerx *= TILE_SIZE
        self.rect.centery *= TILE_SIZE
        self.color = color
