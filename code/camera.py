import pygame, math, random
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, game, zone):
        super().__init__()

        self.game = game
        self.zone = zone
        self.offset = pygame.math.Vector2()
        self.acc = pygame.math.Vector2()
        self.screenshake_timer = 0

    def screenshake(self):
        if self.game.screenshaking:
            self.screenshake_timer += 1
            if self.screenshake_timer < 120:
                random_number = random.randint(-1, 1)
                self.offset += [random_number, random_number]
            else:
                self.game.screenshaking = False

    def screenshake_update(self, dt):
        self.screenshake_timer *= dt

    def offset_draw(self, target):
        self.game.screen.fill(LIGHT_GREEN)

        mouse_dist = self.zone.get_distance(pygame.mouse.get_pos(), target.rect.center) / 10

        self.offset.x += (target.rect.centerx - HALF_WIDTH - self.offset.x)
        self.offset.y += (target.rect.centery - HALF_HEIGHT - self.offset.y)

        # Apply screenshake effect if needed
        self.screenshake()

        for layer in LAYERS.values():
            for sprite in self.zone.rendered_sprites:
                if sprite.z == layer:
                    offset = sprite.rect.topleft - self.offset
                    self.game.screen.blit(sprite.image, offset)
