import noise

from src.utils import *


class WorldGen:
    def __init__(self, size):
        self.size = size
        self.world = []

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
                    color = '#0f5e9c'
                elif noise_value <= -0.15:
                    color = '#1ca3ec'
                elif noise_value <= -0.1:
                    color = '#CBBD93'
                else: color = '#7CFC00'
                row.append(Tile((x, y), color, groups))
            self.world.append(row)

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, color, groups):
        super().__init__(groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_frect(topleft=pos)
        self.rect.x *= TILE_SIZE
        self.rect.y *= TILE_SIZE
        self.color = color

class Chunk(pg.sprite.Sprite):
    def __init__(self, tiles, pos, groups):
        super().__init__(groups)

        self.tiles = tiles
        self.origin = tiles[0].rect.topleft
        self.chunk_size = 16
        self.image = pg.Surface((self.chunk_size * TILE_SIZE, self.chunk_size * TILE_SIZE))
        blit_sequence = []
        for row in tiles:
            for tile in row:
                blit_sequence.append((tile.image, tile.rect.topleft))
        self.image.blits(blit_sequence)
        self.image.scroll(*self.origin)
