from pygame.sprite import Sprite, Group, spritecollide, collide_mask
from pygame.mixer import Sound
from pygame import Surface
from pygame.math import Vector2
from pygame.mask import from_surface
from pygame.time import get_ticks
from pygame.event import post, Event
from components.meteor import meteor_death_event

class Laser(Sprite):
    def __init__(self, group, pos, image : Surface, shoot_sound : Sound, hit_sound : Sound, speed : int, meteor_group : Group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = from_surface(self.image)

		# float based position 
        self.pos = Vector2(self.rect.topleft)
        self.direction = Vector2(0,-1)
        self.speed = speed
        self.dt = get_ticks()/1000

		# sound
        self.explosion_sound = hit_sound
        self.shoot_sound = shoot_sound

        self.meteor_group = meteor_group

    def meteor_collision(self, meteor_group : Group):
        killed_meteors = spritecollide(self, meteor_group, False, collide_mask)
        if killed_meteors:
            self.kill()
            self.explosion_sound.play()
            for meteor in killed_meteors:
                post(Event(meteor_death_event))
                if meteor.hits > 1:
                    meteor.spawn()
                meteor.kill()


    def update(self):
        ct = get_ticks()/1000
        #print(f'speed: {ct - self.dt}')
        self.pos += self.direction * self.speed * (ct - self.dt)
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.dt = ct
        if self.rect.bottom < 0:
            self.kill()

        self.meteor_collision(self.meteor_group)