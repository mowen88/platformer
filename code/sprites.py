import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z	
		self.dir = 0

class Platform(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.zone = zone

		self.image = surf
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.dir = pygame.math.Vector2(1,0)
		self.start_pos = self.pos.copy()

	def update(self, dt):

		self.pos.x += self.dir.x * dt
		self.rect.x = round(self.pos.x)

		if self.rect.left >= self.start_pos.x + (5 * TILESIZE) or self.rect.left < self.start_pos.x:
			self.dir.x *= -1


# moving platform vert
# moving platform hor
# disappearing platform
# timed platform with activator
# moving crates
# escalator platform
# bouncing thing
# breakable wall

# spikes
# arrows
# fire pits
# fire walls



