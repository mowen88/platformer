from state import State
from settings import *

class Dialogue(State):
	def __init__(self, game, zone, sprite):
		State.__init__(self, game)

		self.sprite = sprite
		self.offset = self.sprite.zone.rendered_sprites.offset

	def update(self, dt):

		if ACTIONS['return']: 
			self.exit_state()
		self.game.reset_keys()

		self.prev_state.update(dt)

	def render(self, screen):
		self.prev_state.render(screen)
		pygame.draw.rect(screen, PINK, (self.sprite.rect.left - 75 - self.offset.x, self.sprite.rect.top - 75 - self.offset.y, 100, 50))