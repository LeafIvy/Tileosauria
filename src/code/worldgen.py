import noise

from src.utils import *


class WorldGen:
    def __init__(self, size):
        self.size = size
        self.world = {}

    def generate_perlin_noise(self, scale=100.0, octaves=6, persistance=0.3, lacunarity=2.0):
        for y in WINDOW_HEIGHT:
            for x in WINDOW_WIDTH:
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
                    tile = 'water'
                else: tile = 'ground'
                self.world[(x, y)] = tile
