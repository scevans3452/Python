import pygame, random, settings

from pygame.locals import (
    RLEACCEL
)

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super(Shield, self).__init__()
        self.base_image = pygame.image.load("./assets/shield.png").convert()
        self.surf = pygame.transform.scale(self.base_image, (settings.POW_WIDTH, settings.POW_HEIGHT))
        self.rect = self.surf.get_rect()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.powertype = "Shield"
        self.collided = False
        self.rect = self.surf.get_rect(
            center=(
                random.randint(settings.SCREEN_WIDTH + 20, settings.SCREEN_WIDTH + 100),
                random.randint(0, settings.SCREEN_HEIGHT),
            )
        )
        self.speed = 6
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Ammo(pygame.sprite.Sprite):
    def __init__(self):
        super(Ammo, self).__init__()
        self.base_image = pygame.image.load("./assets/ammo.png").convert()
        self.surf = pygame.transform.scale(self.base_image, (settings.POW_WIDTH, settings.POW_HEIGHT))
        self.rect = self.surf.get_rect()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.powertype = "Ammo"
        self.collided = False
        self.rect = self.surf.get_rect(
            center=(
                random.randint(settings.SCREEN_WIDTH + 20, settings.SCREEN_WIDTH + 100),
                random.randint(0, settings.SCREEN_HEIGHT),
            )
        )
        self.speed = 6
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Double_Points(pygame.sprite.Sprite):
    def __init__(self):
        super(Double_Points, self).__init__()
        self.base_image = pygame.image.load("./assets/Double_Points.png").convert()
        self.surf = pygame.transform.scale(self.base_image, (settings.POW_WIDTH, settings.POW_HEIGHT))
        self.rect = self.surf.get_rect()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.powertype = "Double_Points"
        self.collided = False
        self.creation_time = pygame.time.get_ticks()
        self.duration = 3000 # 3 seconds
        self.rect = self.surf.get_rect(
            center=(
                random.randint(settings.SCREEN_WIDTH + 20, settings.SCREEN_WIDTH + 100),
                random.randint(0, settings.SCREEN_HEIGHT),
            )
        )
        self.speed = 6
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Multi_Shot(pygame.sprite.Sprite):
    def __init__(self):
        super(Multi_Shot, self).__init__()
        self.base_image = pygame.image.load("./assets/spread_shot.png").convert()
        self.surf = pygame.transform.scale(self.base_image, (settings.POW_WIDTH, settings.POW_HEIGHT))
        self.rect = self.surf.get_rect()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.powertype = "Multi Shot"
        self.collided = False
        self.creation_time = pygame.time.get_ticks()
        self.duration = 3000 # 3 seconds
        self.rect = self.surf.get_rect(
            center=(
                random.randint(settings.SCREEN_WIDTH + 20, settings.SCREEN_WIDTH + 100),
                random.randint(0, settings.SCREEN_HEIGHT),
            )
        )
        self.speed = 6
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
