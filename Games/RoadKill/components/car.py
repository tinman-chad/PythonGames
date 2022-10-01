import pygame 
from pygame.math import Vector2
from pygame.transform import flip
from pygame.sprite import Sprite
from os import walk
from random import choice

class Car(Sprite):
	def __init__(self,pos,groups, facing_direction: int = 1, speed: int = 300):
		super().__init__(groups)
		self.name = 'car'
		
		for _, _, img_list in walk('./graphics/cars'):
			car_name = choice(img_list)
		self.facing_direction = facing_direction
		self.image = pygame.image.load('./graphics/cars/' + car_name).convert_alpha()
		if facing_direction != 1:
			self.image = flip(self.image,True, False)
		self.rect = self.image.get_rect(center = pos)

		# float based movement 
		self.pos = Vector2(self.rect.center)
		
		self.direction = Vector2(self.facing_direction,0)
		self.speed = speed

		# collision
		self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

	def update(self,dt):
		self.pos += self.direction * self.speed * dt
		self.hitbox.center = (round(self.pos.x), round(self.pos.y))
		self.rect.center = self.hitbox.center

		if not -200 < self.rect.x < 3400:
			self.kill()