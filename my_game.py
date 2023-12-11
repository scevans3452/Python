import pygame
import random

# Setup for sounds. Defaults are good.
pygame.mixer.init()
pygame.init()

# shortens implicit variable names from "pygame.VAR" to "VAR"
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_SPACE,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 600

# Set the screen to windowed mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Basic Game')

# variables for score counter
score_value         = 0
previous_high_score = 0
font                = pygame.font.Font('freesansbold.ttf', 32)
running             = True

def read_high_score(file):
    with open(file, 'r', encoding='utf-8') as file:
        read_from_file = file.read()
        previous_high_score = int(read_from_file)
    return previous_high_score

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_previous_high_score(x, y):
    high_score = font.render("High Score : " + str(previous_high_score), True, (255, 255, 255))
    screen.blit(high_score, (x, y))


# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf       = pygame.image.load("./sample_project/jet.png").convert()
        self.rect       = self.surf.get_rect()
        self.last_shot  = 0  # Initialize the time of the last shot
        self.bullets    = pygame.sprite.Group()  # Group for holding bullets
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 8)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)
        if pressed_keys[K_SPACE]:  # Check for spacebar press to fire projectiles
            current_time = pygame.time.get_ticks()  # Get the current time
            time_since_last_shot = current_time - self.last_shot
            if time_since_last_shot >= 500:  # Limit firing rate to once per second (1000 milliseconds)
                self.fire()
                self.last_shot = current_time  # Update the time

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def fire(self):
        bullet = Bullet(self.rect.midright)  # Create a bullet at player's left side
        self.bullets.add(bullet)  # Add the bullet to the bullets group

# Define a bullet object to handle player projectiles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 10))  # Adjust size here (width=5, height=10)
        self.surf.fill((255, 55, 55))  # Red bullet surface (you can load an image here)
        self.rect = self.surf.get_rect(midleft=pos)  # Position the bullet at the player's left side
        self.speed = 10  # Adjust the bullet's speed as needed

    def update(self):
        self.rect.move_ip(self.speed, 0)  # Move the bullet towards the right
        if self.rect.left > SCREEN_WIDTH:  # Remove the bullet if it goes off the screen
            self.kill()  # Remove the sprite from all groups it belongs to

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./sample_project/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("./sample_project/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

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
        now = pygame.time.get_ticks()
        if now - self.creation_time > self.duration:
            self.kill()  # Remove the explosion after its duration expires


# Create custom events for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
INCREASE_SCORE = pygame.USEREVENT + 3
pygame.time.set_timer(INCREASE_SCORE, 100)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player.bullets)  # Add bullets to the group

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("./sample_project/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound   = pygame.mixer.Sound("./sample_project/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("./sample_project/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("./sample_project/Collision.ogg")

# Start the main loop
while running:

    for bullet in player.bullets:
        screen.blit(bullet.surf, bullet.rect)
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)  # True removes the enemy on collision
        for enemy in enemy_hit_list:
            score_value += 50
            # Create an explosion at the enemy's position
            explosion = Explosion(enemy.rect.center)
            all_sprites.add(explosion)  # Add the explosion to all_sprites group
        if enemy_hit_list:  # Remove the bullet upon collision with an enemy
            bullet.kill()


    # Check for events
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == QUIT:
            # Quit the game
            pygame.quit()
            #sys.exit()

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == INCREASE_SCORE:
            score_value += 1

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player.bullets.update()

    # Update the position of enemies and clouds
    enemies.update()
    clouds.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))
    previous_high_score = read_high_score('highscore.txt')
    show_score(0, 0)
    show_previous_high_score(0, 60)

    all_sprites.add(player.bullets)  # Add bullets to the group

    # Draw all sprites
    for entity in all_sprites:
        if isinstance(entity, Explosion):
            screen.blit(entity.image, entity.rect)
            entity.update()
        else:
            screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # Stop the loop
        running = False

    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()

# updates highscore.txt if current score is greater than previous high score.
if previous_high_score < score_value:
    with open('highscore.txt', 'w', encoding = 'utf-8') as file:
        file.write(f'{score_value}')