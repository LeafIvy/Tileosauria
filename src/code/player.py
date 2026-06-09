from src.utils import *


class Player(pg.sprite.Sprite):
    """Base class for Player"""
    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        # base settings
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

        # movement attributes
        move_delay_time = 250 # milliseconds
        self.speed = 0.5 # tiles per {move_delay_time}
        self.direction = pg.Vector2()
        self.move_delay = Timer(move_delay_time)

    def input(self):
        """Get input from keyboard and alter direction vector"""
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])
        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])

    def move(self, dt):
        """Alter position of player rect"""
        if not self.move_delay:
            self.rect.x += self.speed * TILE_SIZE * self.direction.x

            self.rect.y += self.speed * TILE_SIZE * self.direction.y

            if self.direction: self.move_delay.activate()

    def update(self, dt):
        """Call methods to update player data"""
        self.input()
        self.move_delay.update()
        self.move(dt)
