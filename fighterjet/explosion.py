import pygame

from pygame.locals import (
    RLEACCEL
)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Explosion, self).__init__()
        explosion_image = pygame.image.load('./assets/explosion.png').convert()
        self.image = pygame.transform.scale(explosion_image, (40, 50))
        self.rect = self.image.get_rect(center=pos)
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.duration = 800  # Duration of the explosion in milliseconds
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        self.rect.move_ip(-5, 0)
        now = pygame.time.get_ticks()
        if now - self.creation_time > self.duration:
            self.kill()  # Remove the explosion after its duration expires
