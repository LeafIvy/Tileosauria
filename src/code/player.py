from src.utils import *


class Player(pg.sprite.Sprite):
    """Base class for Player"""
    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        # base settings
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

        # movement attributes
        self.speed = 3 # tiles per second
        self.direction = pg.Vector2()

    def input(self):
        """Get input from keyboard and alter direction vector"""
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])

        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])

    def move(self, dt):
        """Alter position of player rect"""
        self.rect.x += self.speed * TILE_SIZE * self.direction.x * dt

        self.rect.y += self.speed * TILE_SIZE * self.direction.y * dt

    def update(self, dt):
        """Call methods to update player data"""
        self.input()
        self.move(dt)
