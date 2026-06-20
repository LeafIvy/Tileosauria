from src.utils import *


class Player(pg.sprite.Sprite):
    """Base class for Player"""
    def __init__(self, surf, pos, groups, collision_sprites):
        super().__init__(groups)

        # base settings
        self.image   = surf
        self.image.fill('purple')
        self.rect    = self.image.get_frect(topleft=pos)
        self.old_pos = self.rect.center

        # movement attributes
        self.speed          = 4 # tiles per second
        self.movement_timer = Timer(1000 / self.speed) # cover 1 tile every 250ms
        self.direction      = pg.Vector2()

        # collision
        self.collision_sprites = collision_sprites

        # position of screen edges in actual pixel coordinates
        self.view_right = self.rect.centerx + WINDOW_WIDTH / 2
        self.view_left = self.rect.centerx - WINDOW_WIDTH / 2
        self.view_top = self.rect.centery - WINDOW_HEIGHT / 2
        self.view_bottom = self.rect.centery + WINDOW_HEIGHT / 2

    def input(self):
        """Get input from keyboard and alter direction vector"""
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])
        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])
        # slow down diagonal movement
        if self.direction.magnitude() > 1: self.movement_timer.duration = 1.414 * 250
        else: self.movement_timer.duration = 250

    def move(self, dt):
        """Alter position of player rect"""
        # moves player after timer's over
        if not self.movement_timer:
            self.rect.center += TILE_SIZE * self.direction
            self.collision()
            self.old_pos = self.rect.center
            if self.direction: self.movement_timer.activate() # reactivates timer

    def collision(self):
        """Move back to original position if collision occurs"""
        for sprite in self.collision_sprites:
            if sprite.rect.center == self.rect.center:
                self.rect.center = self.old_pos

    def update(self, dt):
        """Call methods to update player data"""
        self.input()
        self.movement_timer.update()
        self.move(dt)
