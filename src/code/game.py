from src.utils import *
from .player import Player
from .tileosaur import Tileosaur
from .tileopodium import Tileopodium
from src.utils.groups import AllSprites
from .worldgen import WorldGen
from random import randint


class Game:
    """Game class to run the game"""
    def __init__(self):
        pg.init()

        # game setup
        self.screen     = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock      = pg.time.Clock()
        self.running    = True
        self.world = WorldGen(WORLD_SIZE)
        self.world.generate_perlin_noise(base=randint(0, 169))
        self.world.generate_chunks()
        pg.display.set_caption(TITLE)

        # sprite groups
        self.all_sprites = AllSprites()
        self.collision_sprites = set()

        # player setup
        self.player = Player(pg.Surface((TILE_SIZE, TILE_SIZE)), (100 * TILE_SIZE, 105 * TILE_SIZE), self.collision_sprites)
        self.all_sprites.add(self.player, layer=1)

        saur_surf = pg.image.load(join('src', 'images', 'tileosaurs', 'Palitiles.png')).convert_alpha()
        saur_surf = pg.transform.scale_by(saur_surf, TILE_SIZE / saur_surf.get_width())
        self.saur = Tileosaur(saur_surf, (100*TILE_SIZE, 100*TILE_SIZE), self.player, self.collision_sprites)
        self.all_sprites.add(self.saur, layer=1)
        self.collision_sprites.add(self.saur)

        podia_surf = pg.image.load(join('src', 'images', 'tileopodiums', 'Tonyveils.png')).convert_alpha()
        podia_surf = pg.transform.scale_by(podia_surf, TILE_SIZE / podia_surf.get_width())
        self.podia = Tileopodium(podia_surf, (100*TILE_SIZE, 104*TILE_SIZE))
        self.all_sprites.add(self.podia, layer=1)
        self.collision_sprites.add(self.podia)

        # grid
        self.vertical_lines     = [[(i, 0), (i, WINDOW_HEIGHT)] for i in
                                   range(int(WINDOW_WIDTH/2 - TILE_SIZE/2 - TILE_SIZE * 10), WINDOW_WIDTH, TILE_SIZE)]
        self.horizontal_lines   = [[(0, i), (WINDOW_WIDTH, i)] for i in
                                   range(int(WINDOW_HEIGHT/2 - TILE_SIZE/2 - TILE_SIZE * 10), WINDOW_HEIGHT, TILE_SIZE)]
        self.grid               = self.vertical_lines + self.horizontal_lines

    def draw_chunks(self):
        """Draw only those chunks which are near the player/visible onscreen"""
        visible_chunks = []
        for chunk in self.world:
            if (self.player.view_left - TILE_SIZE * CHUNK_SIZE - TILE_SIZE <= chunk.origin[0] <= self.player.view_right + TILE_SIZE
            and self.player.view_top - TILE_SIZE * CHUNK_SIZE - TILE_SIZE <= chunk.origin[1] <= self.player.view_bottom + TILE_SIZE * CHUNK_SIZE):
                visible_chunks.append((chunk.image, chunk.origin + self.all_sprites.offset))
        self.screen.blits(visible_chunks)

    def run(self):
        """Starts the game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pg.event.get():
                if get_quit(event):
                    self.running = False

            # draw calls
            self.screen.fill(BG_COLOR)
            self.draw_chunks()
            self.all_sprites.draw(self.player.rect.center)

            # draw grid
            # for line in self.grid: pg.draw.aaline(self.screen, 'black', line[0], line[1])

            # update calls
            self.all_sprites.update(dt)
            pg.display.update()

        pg.quit()
