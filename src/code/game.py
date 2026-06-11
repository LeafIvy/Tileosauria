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
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        # sprite groups
        self.all_sprites = AllSprites()

        # player setup
        self.player = Player(pg.Surface((64, 64)), (0, 0), (self.all_sprites,))

        saur_surf = pg.image.load(join('src', 'images', 'tileosaurs', 'Palitiles.png')).convert_alpha()
        saur_surf = pg.transform.scale2x(saur_surf)
        self.saur = Tileosaur(saur_surf, (5*64, 64), (self.all_sprites,))

        podia_surf = pg.image.load(join('src', 'images', 'tileopodiums', 'Tonyveils.png')).convert_alpha()
        podia_surf = pg.transform.scale2x(podia_surf)
        self.podia = Tileopodium(podia_surf, (-5*64, 3*64), (self.all_sprites,))

        # grid
        self.vertical_lines = [[(i, 0), (i, WINDOW_HEIGHT)] for i in range(-32, WINDOW_WIDTH, 64)]
        self.horizontal_lines = [[(0, i), (WINDOW_WIDTH, i)] for i in range(7, WINDOW_HEIGHT, 64)]
        self.grid = self.vertical_lines + self.horizontal_lines

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
