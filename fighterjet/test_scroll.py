import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Scroll")

#load image
bg = pygame.image.load("./assets/skyline_updated.png").convert()
bg_width = bg.get_width()
bg_height = bg.get_height()  # Get the original height of the image

# Calculate the scale factor for the image height to fit the screen
scale_factor = SCREEN_HEIGHT / bg_height

# Resize the image to fit the screen height while maintaining aspect ratio
bg = pygame.transform.scale(bg, (int(bg_width * scale_factor), SCREEN_HEIGHT))

#define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH  / bg.get_width()) + 1

#game loop
run = True
while run:

    clock.tick(FPS)

    #draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg.get_width() + scroll, 0))
        # pygame.draw.rect(screen, (255, 0, 0), (i * bg.get_width() + scroll, 0, bg.get_width(), SCREEN_HEIGHT), 1)

    #scroll background
    scroll -= 1

    #reset scroll
    if abs(scroll) > bg.get_width():
        scroll = 0

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
