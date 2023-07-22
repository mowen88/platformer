import pygame
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from state import State
from sprites import Tile, Platform
from player import Player

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		self.beam_particle =  pygame.sprite.Group()

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()

		self.create_map()

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		Platform(self.game, self, [self.platform_sprites, self.updated_sprites, self.rendered_sprites], (3 * TILESIZE, 15 * TILESIZE), pygame.Surface((TILESIZE * 3, TILESIZE)))

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
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def render(self, screen):
		screen.fill(LIGHT_GREY)
		self.rendered_sprites.offset_draw(self.target)
		self.game.render_text(round(self.player.platform_speed.x, 3), WHITE, self.game.small_font, RES/2)

