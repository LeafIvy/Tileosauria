from src.utils import *
from .player import Player
from .tileosaur import Tileosaur
from .tileopodium import Tileopodium
from src.utils.groups import AllSprites


class Game:
    """Game class to run the game"""
    def __init__(self):
        pg.init()

        # game setup
        self.screen     = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock      = pg.time.Clock()
        self.running    = True
        pg.display.set_caption(TITLE)

        # sprite groups
        self.all_sprites = AllSprites()
        self.collision_sprites = set()

        # player setup
        self.player = Player(pg.Surface((TILE_SIZE, TILE_SIZE)), (0, 0), (self.all_sprites,), self.collision_sprites)

        saur_surf = pg.image.load(join('src', 'images', 'tileosaurs', 'Palitiles.png')).convert_alpha()
        saur_surf = pg.transform.scale_by(saur_surf, TILE_SIZE / saur_surf.get_width())
        self.saur = Tileosaur(saur_surf, (3*TILE_SIZE, 2*TILE_SIZE), (self.all_sprites,), self.player, self.collision_sprites)
        self.collision_sprites.add(self.saur)

        podia_surf = pg.image.load(join('src', 'images', 'tileopodiums', 'Tonyveils.png')).convert_alpha()
        podia_surf = pg.transform.scale_by(podia_surf, TILE_SIZE / podia_surf.get_width())
        self.podia = Tileopodium(podia_surf, (-5*TILE_SIZE, 3*TILE_SIZE), (self.all_sprites,))
        self.podia.is_passable = True
        self.podia.tile_cost = 4123 # magic number at which tileosaur starts avoiding the sprite
        self.podia.tile_cost = math.inf
        self.collision_sprites.add(self.podia)

        # grid
        self.vertical_lines     = [[(i, 0), (i, WINDOW_HEIGHT)] for i in range(-32, WINDOW_WIDTH, TILE_SIZE)]
        self.horizontal_lines   = [[(0, i), (WINDOW_WIDTH, i)] for i in range(7, WINDOW_HEIGHT, TILE_SIZE)]
        self.grid               = self.vertical_lines + self.horizontal_lines

    def run(self):
        """Starts the game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pg.event.get():
                if get_quit(event):
                    self.running = False

            # draw calls
            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)

            # draw grid
            for line in self.grid: pg.draw.aaline(self.screen, 'black', line[0], line[1])

            # update calls
            self.all_sprites.update(dt)
            pg.display.update()

        pg.quit()
