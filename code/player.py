import pygame
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, z, block_sprites):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.z = z
		self.block_sprites = block_sprites

		# animation
		self.char = 'player'
		self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
		self.animation_type = ''
		self.import_images(self.animations)
		self.state = 'idle'
		self.frame_index = 0
		self.original_image = self.animations[self.state][self.frame_index]
		self.image = self.original_image

		# self.image = pygame.Surface((TILESIZE * 2, TILESIZE * 3))
		# self.image.fill(RED)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.2)
		self.old_hitbox = self.hitbox.copy()

		# physics
		self.angle = 0
		self.target_angle = 0
		self.gravity = 0.3
		self.fric = -0.15
		self.acc = pygame.math.Vector2(0, self.gravity)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.dir = pygame.math.Vector2()
		self.on_platform = False
		self.platform_speed = pygame.math.Vector2()

		# jumping
		self.jump_height = 7
		self.max_fall_speed = 12
		self.jump_counter = 0
		self.cyote_timer = 0
		self.cyote_timer_threshold = 6
		self.jump_buffer_active = False
		self.jump_buffer = 0
		self.jump_buffer_threshold = 6

		# player collide type
		self.on_ground = False
		self.on_ceiling = False

	def import_images(self, animation_states):

		char_path = f'../assets/{self.char}/'

		for animation in animation_states.keys():
			full_path = char_path + animation
			animation_states[animation] = self.game.get_folder_images(full_path)

	def animate(self, dt):

		self.frame_index += 0.15 * dt
		self.frame_index = self.frame_index % len(self.animations[self.state])	
		self.angle += (-(self.dir.x * 3) - self.angle)/10
		self.image = pygame.transform.rotate(self.animations[self.state][int(self.frame_index)], self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)

	def input(self):
		keys = pygame.key.get_pressed()

		if ACTIONS['up']:
			ACTIONS['up'] = False
			self.jump(self.jump_height)
			if not self.on_ground:
				self.jump_buffer_active = True

		if ACTIONS['right']:
			self.acc.x += 0.5
			self.target_angle = -10
		elif ACTIONS['left']:
			self.acc.x -= 0.5
			self.target_angle = 10
		else:
			ACTIONS['right'], ACTIONS['left'] = False, False
			self.target_angle = 0



	def platforms(self, dt):
		for platform in self.zone.platform_sprites:
			platform_raycast = pygame.Rect(platform.rect.x, platform.rect.y - platform.rect.height * 0.2, platform.rect.width, platform.rect.height)
			if self.hitbox.colliderect(platform.rect) or self.hitbox.colliderect(platform_raycast): 
				if self.hitbox.bottom <= platform.rect.top + 4 and self.dir.y >= 0:
					self.on_platform = True	
			else:
				self.on_platform = False

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

	def collisions(self, direction):

		for sprite in self.block_sprites:
			if sprite.rect.colliderect(self.hitbox):

				if direction == 'x':
					if self.hitbox.right >= sprite.rect.left and self.old_hitbox.right <= sprite.old_rect.left:
						self.hitbox.right = sprite.rect.left
					
					elif self.hitbox.left <= sprite.rect.right and self.old_hitbox.left >= sprite.old_rect.right:
						self.hitbox.left = sprite.rect.right

					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

				if direction == 'y':
					if self.hitbox.bottom >= sprite.rect.top and self.old_hitbox.bottom <= sprite.old_rect.top:
						self.hitbox.bottom = sprite.rect.top
						self.on_ground = True
						self.dir.y = 0
			
					elif self.hitbox.top <= sprite.rect.bottom and self.old_hitbox.top >= sprite.old_rect.bottom:
						self.hitbox.top = sprite.rect.bottom
						self.on_ceiling = True
						self.dir.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def jump(self, height):
		if self.cyote_timer < self.cyote_timer_threshold:
			self.dir.y = -height
			if self.on_ground:
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

		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		
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
		if self.dir.y >= self.max_fall_speed: 
			self.dir.y = self.max_fall_speed

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
		self.animate(dt)
		self.input()
		self.physics_x(dt)
		# platforms must go after x and before y so blocks take priority
		self.platforms(dt)
		self.physics_y(dt)
		self.handle_jumping(dt)



		


		
		