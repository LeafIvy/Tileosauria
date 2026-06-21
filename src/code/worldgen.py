import noise

from src.utils import *


# Creating surfaces once to be used many times
WATER_0_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
WATER_0_SURF.fill('#0f5e9c')

WATER_1_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
WATER_1_SURF.fill('#2389da')

WATER_2_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
WATER_2_SURF.fill('#1ca3ec')

SAND_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
SAND_SURF.fill('#CBBD93')

GRASS_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
GRASS_SURF.fill('#7CFC00')

SURFS = (WATER_0_SURF, WATER_1_SURF, WATER_2_SURF, SAND_SURF, GRASS_SURF)


class WorldGen:
    """Manages generating terrain"""
    def __init__(self):
        self.tiles_grid = []
        self.chunks = []

    def __iter__(self):
        return iter(self.chunks)

    def generate_perlin_noise(self, scale=100.0, octaves=6, persistance=0.3, lacunarity=2.0, base=91):
        """Generates noise map"""
        for y in range(WORLD_SIZE):
            row = []
            for x in range(WORLD_SIZE):
                dx = x / scale
                dy = y /scale
                noise_value = noise.pnoise2(
                    dx,
                    dy,
                    octaves=octaves,
                    persistence=persistance,
                    lacunarity=lacunarity,
                    repeatx=WORLD_SIZE,
                    repeaty=WORLD_SIZE,
                    base=base
                )
                if noise_value <= -0.35:
                    tile_id = 0             # deep water
                elif noise_value <= -0.2:
                    tile_id = 1             # water water
                elif noise_value <= -0.15:
                    tile_id = 2             # shallow water
                elif noise_value <= -0.1:
                    tile_id = 3             # sand
                else: tile_id = 4           # grass
                row.append(tile_id)
            self.tiles_grid.append(row)

    def generate_chunks(self):
        """Splits the noise map grid into chunks"""
        for y in range(0, WORLD_SIZE, CHUNK_SIZE):
            for x in range(0, WORLD_SIZE, CHUNK_SIZE):
                chunk = [row[x:x+CHUNK_SIZE] for row in self.tiles_grid[y:y+CHUNK_SIZE]]
                origin = (x * TILE_SIZE, y * TILE_SIZE) # to draw chunk in correct position later
                self.chunks.append(Chunk(chunk, origin))

class Chunk:
    """Chunks to be used to group together tiles for easier drawing"""
    def __init__(self, chunk, origin):
        self.origin = origin
        self.image = pg.Surface((CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE))
        self.rect = self.image.get_frect()
        blit_sequence = []
        for y, row in enumerate(chunk):
            for x, tile_id in enumerate(row):
                blit_sequence.append((SURFS[tile_id], (x * TILE_SIZE, y * TILE_SIZE)))

        self.image.blits(blit_sequence)

    def draw_border(self):
        """Draws chunk's borders"""
        pg.draw.rect(self.image, 'darkblue', self.rect, 1)

