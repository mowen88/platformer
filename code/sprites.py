import pygame, math
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z	
		self.old_rect = self.rect.copy()

class Platform(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, direction, z = LAYERS['particles']):
		super().__init__(groups)

		self.zone = zone
		self.direction = direction
		self.image = surf
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.dir = pygame.math.Vector2((self.direction))
		self.start_pos = pygame.math.Vector2(self.rect.center)

	def update(self, dt):

		self.pos += self.dir * dt
		

class MovingPlatform(Platform):
	def __init__(self, game, zone, groups, pos, surf, direction, move_range, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, direction, z)

		self.range = move_range
		self.image.fill(PINK)

	def update(self, dt):

		if self.rect.right > self.start_pos.x + self.range:
			self.rect.right = self.start_pos.x + self.range
			self.pos.x = self.rect.x
			self.dir.x *= -1
		if self.rect.left < self.start_pos.x - self.range:
			self.rect.left = self.start_pos.x - self.range
			self.pos.x = self.rect.x
			self.dir.x *= -1
		if self.rect.bottom > self.start_pos.y + self.range:
			self.rect.bottom = self.start_pos.y + self.range
			self.pos.y = self.rect.y
			self.dir.y *= -1
		if self.rect.top < self.start_pos.y - self.range:
			self.rect.top = self.start_pos.y - self.range
			self.pos.y = self.rect.y
			self.dir.y *= -1

		self.pos += self.dir * dt
		self.rect.topleft = round(self.pos)

		# frequency = 0.1
		# amplitude = 50
		# self.pos.x += self.dir.x * dt
		# self.rect.x = round(self.start_pos.x + amplitude * math.sin(self.pos.x * frequency))

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



