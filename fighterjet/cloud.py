import pygame, random, settings

from pygame.locals import (
    RLEACCEL
)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, opacity=255):  # Default opacity is 255 (fully opaque)
        super(Cloud, self).__init__()
        self.base_image = pygame.image.load("./assets/cloud.png").convert()
        self.surf = pygame.transform.scale(self.base_image, (120, 60))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(settings.SCREEN_WIDTH + 40, settings.SCREEN_WIDTH + 100),
                random.randint(0, settings.SCREEN_HEIGHT),
            )
        )
        self.opacity = opacity  # Set the initial opacity

    def update_opacity(self, new_opacity):
        self.opacity = new_opacity

    def update(self):
        self.surf.set_alpha(self.opacity)  # Set the alpha (opacity) value for the surface

        self.rect.move_ip(random.randint(-4, -2), 0)
        if self.rect.right < 0:
            self.kill()
