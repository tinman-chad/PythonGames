from pygame.sprite import Sprite

class SimpleSprite(Sprite):
	def __init__(self,surf,pos,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

class LongSprite(SimpleSprite):
	def __init__(self,surf,pos,groups):
		super().__init__(surf,pos,groups)
		self.hitbox = self.rect.inflate(-self.rect.width * 0.8,-self.rect.height / 2)
		self.hitbox.bottom = self.rect.bottom - 10