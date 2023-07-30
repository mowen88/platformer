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
		self.direction = pygame.math.Vector2(direction)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.dir = pygame.math.Vector2((self.direction))
		self.start_pos = pygame.math.Vector2(self.rect.center)
		
	def update(self, dt):

		self.pos += self.dir * dt

class CircularPlatform(Platform):
	def __init__(self, game, zone, groups, pos, surf, direction, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, direction, z)

	def update(self, dt):

		if self.rect.centery < self.start_pos.y:
			self.dir.y += 0.05 * dt
		else:
			self.dir.y -= 0.05 * dt

		if self.dir.y >= 0.01:
			self.dir.x += 0.05 * dt
		else:
			self.dir.x -= 0.05 * dt

		self.pos += self.dir * dt
		self.rect.topleft = round(self.pos)


class MovingPlatform(Platform):
	def __init__(self, game, zone, groups, pos, surf, direction, z = LAYERS['particles']):
		super().__init__(game, zone, groups, pos, surf, direction, z)

		self.range = pygame.math.Vector2(self.direction * TILESIZE * 5)
		self.limits = {'left': self.start_pos.x - self.range.x,
						'right': self.start_pos.x + self.range.x,
						'top': self.start_pos.y - self.range.y,
						'bottom': self.start_pos.y + self.range.y}

	def update(self, dt):

		if self.rect.centerx > self.start_pos.x:
			self.dir.x -= (self.direction.x/100) * dt
		else:
			self.dir.x += (self.direction.x/100) * dt

		if self.rect.centery < self.start_pos.y:
			self.dir.y += (self.direction.y/100) * dt
		else:
			self.dir.y -= (self.direction.y/100) * dt

		# set positional limits otherwise the velocity based movement creates difting
		if self.rect.left <= self.limits['left']: 
			self.dir.x = 0.01
		if self.rect.right >= self.limits['right']:
			self.dir.x = -0.01
		if self.rect.top <= self.limits['top']:
			self.dir.y = 0.01
		if self.rect.bottom >= self.limits['bottom']:
			self.dir.y = -0.01

		# move the platform
		if self.direction.x != 0:
			self.dir.y = 0
			self.pos.x += self.dir.x * dt
			self.rect.x = round(self.pos.x)
		if self.direction.y != 0:
			self.dir.x = 0
			self.pos.y += self.dir.y * dt
			self.rect.y = round(self.pos.y)



# moving platform vert xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# moving platform hor xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# disappearing platform
# timed platform with activator 
# moving crates
# escalator platform xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# bouncing thing
# breakable wall

# spikes
# arrows
# fire pits
# fire walls



