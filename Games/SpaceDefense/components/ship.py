from pygame.sprite import Sprite, Group, spritecollide, collide_mask
from pygame.mixer import Sound
from pygame import Surface
from pygame.mask import from_surface
from pygame.time import get_ticks
from pygame.mouse import get_pos, get_pressed
from components.laser import Laser


class Ship(Sprite):
    def __init__(self, group : Group, image : Surface, pos, laser_image : Surface, bulletSound : Sound, explosionSound : Sound, laser_group : Group, meteor_group : Group):
        super().__init__(group)  
		
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.mask = from_surface(self.image)
        #Config values
        self.lives = 3
        self.score = 0
        self.starting_pos = pos
        self.time_to_life = 0

		# timer
        self.can_shoot = True
        self.shoot_time = None

		# sound 
        self.laser_sound = bulletSound
        self.explosion_sound = explosionSound

        #laser
        self.laser_image = laser_image
        self.laser_group = laser_group
        self.meteor_group = meteor_group

    def reset(self):
        self.lives -= 1
        self.time_to_life = get_ticks() + 1000

    def laser_timer(self):
        if not self.can_shoot or self.time_to_life > 0:
            current_time = get_ticks()
            if not self.can_shoot and current_time - self.shoot_time > 125:
                self.can_shoot = True
            if self.time_to_life > 0 and self.time_to_life <= current_time:
                self.time_to_life = 0

    def input_position(self):
        if self.time_to_life <= 0:
            pos = get_pos()
            self.rect.center = pos

    def laser_shoot(self, laser_group):
        if get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = get_ticks()
            Laser(laser_group, self.rect.midtop, self.laser_image, self.laser_sound, self.explosion_sound, 600, self.meteor_group)

    def meteor_collision(self, meteor_group):
        if spritecollide(self, meteor_group, True, collide_mask) and self.lives >= 0:
            self.explosion_sound.play()
            self.reset()

    def update(self):
        self.laser_timer()
        self.input_position()
                
        if self.time_to_life <= 0:
            self.laser_shoot(self.laser_group)
            self.meteor_collision(self.meteor_group)