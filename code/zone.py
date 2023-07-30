import pygame
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from state import State
from dialogue import Dialogue
from sprites import Tile, Platform, CircularPlatform, MovingPlatform
from player import Player

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()

		self.create_map()

		self.dialogue = Dialogue(self.game, self, self.target)

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		for obj in tmx_data.get_layer_by_name('platforms'):
			if obj.name == 'horizontal': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(2,0))
			if obj.name == 'vertical': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,3))
			if obj.name == 'vertical_2': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,2))
			if obj.name == 'vertical_3': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,2))
			if obj.name == 'vertical_4': MovingPlatform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], pos=(obj.x, obj.y), surf=obj.image, direction=(0,2))
		
		
		# # add backgrounds
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[2]], (0,TILESIZE), pygame.image.load('../zones/0.png').convert_alpha())

		# add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == 'player': self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'], self.block_sprites)
			self.target = self.player

		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Tile(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)


	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1))
		return distance

	def update(self, dt):
		if ACTIONS['return']: 
			self.dialogue.enter_state()
			self.game.reset_keys()

		self.updated_sprites.update(dt)
		self.rendered_sprites.screenshake_update(dt)

	def render(self, screen):
		screen.fill(LIGHT_GREY)
		self.rendered_sprites.offset_draw(self.target)
		self.game.render_text(str(round(self.game.clock.get_fps(), 2)), WHITE, self.game.small_font, (HALF_WIDTH, TILESIZE))
		self.game.render_text(round(self.player.dir.y, 2), WHITE, self.game.small_font, RES/2)

