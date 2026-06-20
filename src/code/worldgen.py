import noise

from src.utils import *


DEEP_WATER_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
DEEP_WATER_SURF.fill('#0f5e9c')

SHALLOW_WATER_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
SHALLOW_WATER_SURF.fill('#1ca3ec')

SAND_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
SAND_SURF.fill('#CBBD93')

GRASS_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
GRASS_SURF.fill('#7CFC00')

SURFS = (DEEP_WATER_SURF, SHALLOW_WATER_SURF, SAND_SURF, GRASS_SURF)


class WorldGen:
    def __init__(self, size):
        self.size = size
        self.tiles_grid = []
        self.chunks = []

    def __iter__(self):
        return iter(self.chunks)

    def generate_perlin_noise(self, groups, scale=100.0, octaves=6, persistance=0.3, lacunarity=2.0):
        for y in range(self.size):
            row = []
            for x in range(self.size):
                dx = x / scale
                dy = y /scale
                noise_value = noise.pnoise2(
                    dx,
                    dy,
                    octaves=octaves,
                    persistence=persistance,
                    lacunarity=lacunarity,
                    base=91
                )
                if noise_value <= -0.2:
                    tile_id = 0
                elif noise_value <= -0.15:
                    tile_id = 1
                elif noise_value <= -0.1:
                    tile_id = 2
                else: tile_id = 3
                row.append(tile_id)
            self.tiles_grid.append(row)

    def generate_chunks(self):
        for y in range(0, self.size, CHUNK_SIZE):
            for x in range(0, self.size, CHUNK_SIZE):
                chunk = [row[x:x+CHUNK_SIZE] for row in self.tiles_grid[y:y+CHUNK_SIZE]]
                origin = (x * TILE_SIZE, y * TILE_SIZE)
                self.chunks.append(Chunk(chunk, origin))

class Chunk:
    def __init__(self, chunk, origin):
        self.origin = origin
        self.image = pg.Surface((CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE))
        blit_sequence = []
        for y, row in enumerate(chunk):
            for x, tile_id in enumerate(row):
                blit_sequence.append((SURFS[tile_id], (x * TILE_SIZE, y * TILE_SIZE)))

        self.image.blits(blit_sequence)
