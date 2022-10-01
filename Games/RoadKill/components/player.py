from pygame import K_RIGHT, K_LEFT, K_UP, K_DOWN
from pygame.math import Vector2
from pygame.key import get_pressed
from pygame.sprite import Sprite
from pygame.image import load
from pygame import Surface
from pygame.time import get_ticks
from os import walk
from pathlib import Path

class Player(Sprite):
	def __init__(self, pos, groups, collision_sprites):
		super().__init__(groups)
		
		self.lives = 3
		self.score = 0
		self.level = 1
		# image 
		self.animations = {}
		self.import_assets()
		self.frame_index = 0
		self.status = 'up'
		# self.image = self.animation[self.frame_index]
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		# float based movement 
		self.pos = Vector2(self.rect.center)
		self.y_start = self.pos.y
		self.direction = Vector2()
		self.speed = 200
		self.spawn_time = 0

		# collisions
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

	def import_assets(self): 
		for index, folder in enumerate(walk('./graphics/player')):
			if index > 0:
				path = Path(folder[0])
				key = path.name
				self.animations[key] = []
				for file_name in folder[2]:
					surf = load(path / file_name).convert_alpha()
					self.animations[key].append(surf)

	def collision(self,direction):
		if get_ticks() < self.spawn_time:
			return
		for sprite in self.collision_sprites.sprites():
			if sprite.hitbox.colliderect(self.hitbox):
				if hasattr(sprite,'name') and sprite.name == 'car':
					self.lives -= 1
					self.pos.y = self.y_start
					self.rect.centery = self.pos.y
					self.spawn_time = get_ticks() + 1000

				if direction == 'horizontal':
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					elif self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx
				else:		
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					elif self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def move(self,dt):

		# normalize a vector -> the length of a vector is going to be 1
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# horizontal movement + collision
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement + collision
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def input(self):
		keys = get_pressed()
		
		# horizontal input 
		if keys[K_RIGHT]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[K_LEFT]:
			self.direction.x = -1
			self.status = 'left'
		else:
			self.direction.x = 0

		# vertical input 
		if keys[K_UP]:
			self.direction.y = -1
			self.status = 'up'
		elif keys[K_DOWN]:
			self.direction.y = 1
			self.status = 'down'
		else:
			self.direction.y = 0

	def animate(self,dt):
		current_animation = self.animations[self.status]
		
		if self.direction.magnitude() != 0:
			self.frame_index += 8 * dt
			if self.frame_index >= len(current_animation):
				self.frame_index = 0
		else:
			self.frame_index = 0
		self.image = current_animation[int(self.frame_index)]

	def checkbounds(self):
		if self.rect.left < 640:
			self.pos.x = 640 + self.rect.width / 2
			self.hitbox.left = 640
			self.rect.left = 640
		if self.rect.right > 2560:
			self.pos.x = 2560 - self.rect.width / 2
			self.hitbox.right = 2560
			self.rect.right = 2560
		if self.rect.bottom > 3500:
			self.pos.y = 3500 - self.rect.height / 2
			self.rect.bottom = 3500
			self.hitbox.centery = self.rect.centery

	def update(self,dt):
		self.input()
		self.move(dt)
		self.animate(dt)
		self.checkbounds()