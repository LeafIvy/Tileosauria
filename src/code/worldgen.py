import noise

from src.utils import *


class WorldGen:
    def __init__(self, size):
        self.size = size
        self.world = []
        self.chunks = []

        self.DEEP_WATER_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.DEEP_WATER_SURF.fill('#0f5e9c')

        self.SHALLOW_WATER_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.SHALLOW_WATER_SURF.fill('#1ca3ec')

        self.SAND_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.SAND_SURF.fill('#CBBD93')

        self.GRASS_SURF = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.GRASS_SURF.fill('#7CFC00')

    def __iter__(self):
        return iter(self.world)

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
                    surf = self.DEEP_WATER_SURF
                elif noise_value <= -0.15:
                    surf = self.SHALLOW_WATER_SURF
                elif noise_value <= -0.1:
                    surf = self.SAND_SURF
                else: surf = self.GRASS_SURF
                row.append(Tile(surf, (x, y), groups))
            self.world.append(row)

    def generate_chunks(self):
        chunk_size = 16
        current_x, current_y = 0, 0
        while current_y < self.size:
            while current_x < self.size:
                chunk = []
                counter_y = 0
                for row in self.world[current_y:]:
                    tiles = []
                    counter_x = 0
                    for tile in row[current_x:]:
                        tiles.append(tile)
                        counter_x += 1
                        if counter_x == chunk_size:
                            counter_x = 0
                            break
                    chunk.append(tiles)
                    counter_y += 1
                    if counter_y == chunk_size:
                        counter_y = 0
                        break
                self.chunks.append(Chunk(chunk))
                current_x += chunk_size
            current_x = 0
            current_y += chunk_size

class Tile(pg.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.rect.x *= TILE_SIZE
        self.rect.y *= TILE_SIZE

class Chunk(pg.sprite.Sprite):
    def __init__(self, chunk):
        pg.sprite.Sprite.__init__(self)

        self.chunk = chunk
        self.origin = chunk[0][0].rect.topleft
        self.chunk_size = 16
        self.image = pg.Surface((self.chunk_size * TILE_SIZE, self.chunk_size * TILE_SIZE))
        blit_sequence = []
        for row in chunk:
            for tile in row:
                blit_sequence.append((tile.image, tile.rect.topleft))
        self.image.blits(blit_sequence)
        self.image.scroll(*self.origin)
