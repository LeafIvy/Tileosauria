from src.utils import *
from .player import Player


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
        self.all_sprites = pg.sprite.Group()

        # player setup
        self.player = Player(pg.Surface((32, 32)), (0, 0), (self.all_sprites,))

    def run(self):
        """Starts the game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pg.event.get():
                if get_quit(event):
                    self.running = False

            # draw calls
            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.screen)

            # update calls
            self.all_sprites.update(dt)
            pg.display.update()

        pg.quit()
