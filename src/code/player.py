from src.utils import *


class Player(pg.sprite.Sprite):
    """Base class for Player"""
    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        # base settings
        self.image = surf
        self.rect  = self.image.get_frect(topleft=pos)

        # movement attributes
        self.move_delay = Timer(250) # cover 1 tile every 250ms
        self.direction  = pg.Vector2()

    def input(self):
        """Get input from keyboard and alter direction vector"""
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])
        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])
        # slow down diagonal movement
        if self.direction.magnitude() > 1: self.move_delay.duration = 1.414 * 250
        else: self.move_delay.duration = 250

    def move(self, dt):
        """Alter position of player rect"""
        # moves player after timer's over
        if not self.move_delay:
            self.rect.x += TILE_SIZE * self.direction.x

            self.rect.y += TILE_SIZE * self.direction.y

            if self.direction: self.move_delay.activate() # reactivates timer

    def update(self, dt):
        """Call methods to update player data"""
        self.input()
        self.move_delay.update()
        self.move(dt)
