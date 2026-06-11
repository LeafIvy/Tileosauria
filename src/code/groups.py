from src.utils import *


class AllSprites(pg.sprite.Group):
    """Class for containing all sprites and for camera implementation"""
    def __init__(self):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.offset = pg.Vector2()

    def draw(self, target):
        """Draw sprites onto the screen relative to the player"""
        # Gets relative distance to player
        self.offset.x = -target[0] + WINDOW_WIDTH/2
        self.offset.y = -target[1] + WINDOW_HEIGHT/2

        for sprite in self:
            # Sprites are drawn relative to the player
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
