import pygame
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, block_sprites):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.block_sprites = block_sprites

		self.image = pygame.Surface((TILESIZE, TILESIZE * 1.5))
		self.image.fill(RED)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.2)
		self.old_hitbox = self.hitbox.copy()

		# physics
		self.gravity = 0.3
		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, self.gravity)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.dir = pygame.math.Vector2()
		self.idle_speed = 0
		self.on_platform = False
		self.platform_speed = pygame.math.Vector2()

		# jumping
		self.jump_height = 7
		self.jump_counter = 0
		self.cyote_timer = 0
		self.cyote_timer_threshold = 10
		self.jump_buffer_active = False
		self.jump_buffer = 0
		self.jump_buffer_threshold = 10

		# player collide type
		self.on_ground = False
		self.on_ceiling = False

	def input(self):
		keys = pygame.key.get_pressed()

		if ACTIONS['up']:
			self.jump(self.jump_height)
			if not self.on_ground:
				self.jump_buffer_active = True

		if keys[pygame.K_RIGHT]:
			self.acc.x += 0.6
		elif keys[pygame.K_LEFT]:
			self.acc.x -= 0.6

		self.game.reset_keys()

	def platforms(self, dt):
		for platform in self.zone.platform_sprites:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.dir.y >= 0:
					self.on_platform = True
					self.platform_speed.x = platform.dir.x
					self.cyote_timer = 0
					self.hitbox.bottom = platform.rect.top
					self.on_ground = True
					self.dir.y = 0
					
					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery
			else:
				self.on_platform = False

	def collisions(self, direction):

		for sprite in self.block_sprites:
			if sprite.rect.colliderect(self.hitbox):

				if direction == 'x':
					if self.dir.x > 0:
						self.hitbox.right = sprite.rect.left

					elif self.dir.x < 0:
						self.hitbox.left = sprite.rect.right

					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

				if direction == 'y':
					if self.dir.y > 0:
						self.hitbox.bottom = sprite.rect.top
						self.on_ground = True
						self.dir.y = 0
			
					elif self.dir.y < 0:
						self.hitbox.top = sprite.rect.bottom
						self.on_ceiling = True
						self.dir.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def jump(self, height):
		if self.cyote_timer < self.cyote_timer_threshold:
			self.dir.y = -height
			self.jump_counter = 1
		elif self.jump_counter == 1:
			self.dir.y = -height
			self.jump_counter = 0

	def physics_x(self, dt):

		self.old_hitbox = self.hitbox.copy()

		self.acc.x += self.dir.x * self.fric
		self.dir.x += self.acc.x * dt
		
		if self.on_platform:
			self.pos.x += (self.dir.x + self.platform_speed.x) * dt + (0.5 * self.acc.x) * dt
		else:
			self.pos.x += self.dir.x * dt + (0.5 * self.acc.x) * dt

		self.hitbox.x = round(self.pos.x)
		self.rect.x = self.hitbox.x
		
		self.collisions('x')

		# if player is going slow enough, make the player stand still
		#if abs(self.dir.x) < 0.1: self.dir.x = 0

	def physics_y(self, dt):

		
		# Double the gravity if not holding jump key to allow variale jump height
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.dir.y < 0: 
			self.dir.y += (self.acc.y * 2) * dt
		else:
			self.dir.y += self.acc.y * dt

		self.pos.y += self.dir.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y') 
		self.rect.centery = self.hitbox.centery

		# limit max fall speed
		if self.dir.y >= 8: 
			self.dir.y = 8

		# Make the player off ground if moving in y direction
		if abs(self.dir.y) >= 0.5: 
			self.on_ground = False

	def handle_jumping(self, dt):
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.dir.y < 0:
			self.gravity += self.gravity

		# incrememnt cyote timer when not on ground
		if not self.on_ground: self.cyote_timer += dt
		else: self.cyote_timer = 0

		# if falling, this gives the player one jump if they have double jump
		if self.jump_counter == 0 and self.cyote_timer < self.cyote_timer_threshold:
			self.jump_counter = 1

		# jump buffer activated if pressing jump in air
		if self.jump_buffer_active:
			self.jump_buffer += dt
			if self.jump_buffer > 0 and self.on_ground:
				self.jump(self.jump_height)
			if self.jump_buffer >= self.jump_buffer_threshold:
				self.jump_buffer = 0
				self.jump_buffer_active = False

	def update(self, dt):
		
		self.acc.x = 0
		self.input()
		self.platforms(dt)
		self.physics_x(dt)
		self.physics_y(dt)
		self.handle_jumping(dt)
		



		


		
		