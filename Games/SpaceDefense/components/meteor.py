from pygame.sprite import Sprite, Group, spritecollide, collide_mask
from pygame import Surface
from pygame.math import Vector2
from pygame.mask import from_surface
from pygame.transform import scale, rotozoom
from pygame.time import get_ticks
from pygame.event import custom_type
from random import uniform, randint

meteor_death_event = custom_type()

class Meteor(Sprite):
    def __init__(self, groups : Group, pos, image : Surface, speed : int, direction : float, size : int, rotation_speed : int, max_y : int):
		# basic setup
        super().__init__(groups)
        self.meteor_surf = image
        meteor_size = Vector2(self.meteor_surf.get_size()) * (size * 0.5) # number of hits to distroy 1 will be small, 2 will be medium size, 3 will be large
        self.scaled_surf = scale(self.meteor_surf,meteor_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center = pos)
        self.mask = from_surface(self.image)
        self.hits = size
        self.max_y = max_y
        self.dt = get_ticks()/1000

		# float based positioning
        self.pos = Vector2(self.rect.topleft)
        self.direction = Vector2(direction,1)
        self.speed = speed

		# rotation logic
        self.rotation = 0
        self.rotation_speed = rotation_speed
    
    def spawn(self):
        groups = self.groups()
        for i in range(1, self.hits+1):
            Meteor(groups = groups[0], pos = self.pos, image = self.meteor_surf, speed = randint(400, 600), direction = uniform(-0.5, 0.5), size = self.hits-1, rotation_speed = randint(20, 50), max_y = self.max_y)

    def rotate(self, dt :float):
        self.rotation += self.rotation_speed * (dt - self.dt)
        rotated_surf = rotozoom(self.scaled_surf,self.rotation,1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = from_surface(self.image)

    def update(self):
        ct = get_ticks()/1000
        self.pos += self.direction * self.speed * (ct - self.dt)
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.rotate(ct)
        self.dt = ct

        if self.rect.top > self.max_y:
            self.kill()
