import pygame, random, player, settings

# initialize modules
pygame.mixer.init()
pygame.init()
settings.init()

# shortens implicit variable names from "pygame.VAR" to "VAR"
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Set the screen to windowed mode
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption('Basic Game')

# variables for score counter
score_value         = 0
previous_high_score = 0
roll_breakdown = [0,1,2,3] # breakdown of percentage of the roll from max potential
font                = pygame.font.Font('freesansbold.ttf', 32)
running             = True

def read_high_score(file):
    with open(file, 'r', encoding='utf-8') as file:
        read_from_file = file.read()
        previous_high_score = int(read_from_file)
    return previous_high_score

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_previous_high_score(x, y):
    high_score = font.render("High Score: " + str(previous_high_score), True, (255, 255, 255))
    screen.blit(high_score, (x, y))

def show_defense(x, y):
    text = font.render("Defense: " + str(player_obj.defense), True, (255, 255, 255))
    screen.blit(text, (x, y))

def show_ammo(x, y):
    text = font.render("Ammo: " + str(player_obj.ammo), True, (255, 255, 255))
    screen.blit(text, (x, y))

def set_interval(min, max, game_object, group):
    interval = random.randint(min, max)
    pygame.time.set_timer(group, interval)
    print(f"New {game_object} interval: {interval/1000} seconds")

def roll_dice(min, max):
    die_roll = random.randint(min, max)
    
    if die_roll <= (max*.25):
        quadrant = roll_breakdown[0]
    elif die_roll >= (max*.25) and die_roll <= (max*.50):
        quadrant = roll_breakdown[1]
    elif die_roll >= (max*.5) and die_roll <= (max*.75):
        quadrant = roll_breakdown[2]
    elif die_roll >= (max*.75):
        quadrant = roll_breakdown[3]
    else:
        quadrant = None
    return quadrant


# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
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


# Create custom events for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
INCREASE_SCORE = pygame.USEREVENT + 3
pygame.time.set_timer(INCREASE_SCORE, 100)
ADDPOWERUP = pygame.USEREVENT + 4
set_interval(settings.MIN_INTERVAL, settings.MAX_INTERVAL, "powerup", ADDPOWERUP)

# Instantiate player. Right now, this is just a rectangle.
player_obj = player.Player()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player_obj)
all_sprites.add(player_obj.bullets)  # Add bullets to the group

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("./assets/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Preload objects
for _ in range(random.randint(4, 7)):
    new_cloud = Cloud()
    new_cloud.rect.center = (
        random.randint(0, settings.SCREEN_WIDTH),
        random.randint(0, settings.SCREEN_HEIGHT),
    )
    new_cloud.update_opacity(random.randint(150, 220))
    clouds.add(new_cloud)
    all_sprites.add(new_cloud)

# Start the main loop
while running:
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

        # Add a new enemy
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = player.Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            new_cloud.update_opacity(random.randint(160, 220))
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # score uptick
        elif event.type == INCREASE_SCORE:
            score_value += (1 * settings.MODIFIER)

        # Add a powerup
        elif event.type == ADDPOWERUP:
            power_list = [player.Shield(), player.Double_Points()]
            new_power = power_list[random.randint(0, len(power_list)-1)]
            # print(f"{new_power}")
            powerups.add(new_power)
            all_sprites.add(new_power)
            # Reset the timer with a new random interval
            set_interval(settings.MIN_INTERVAL, settings.MAX_INTERVAL, "powerup", ADDPOWERUP)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player_obj.update(pressed_keys)
    player_obj.bullets.update()

    # Update the position of enemies and clouds
    enemies.update()
    powerups.update()
    clouds.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))
    previous_high_score = read_high_score('highscore.txt')
    show_score(0, 0)
    show_previous_high_score(0, 60)
    show_defense(0, settings.SCREEN_HEIGHT-50)
    show_ammo   (0, settings.SCREEN_HEIGHT-100)

    all_sprites.add(player_obj.bullets)  # Add bullets to the group

    # Draw all sprites
    for entity in all_sprites:
        if isinstance(entity, Explosion):
            screen.blit(entity.image, entity.rect)
            entity.update()
        else:
            screen.blit(entity.surf, entity.rect)



    #################
    #   COLLISIONS  #
    #################
    for bullet in player_obj.bullets:
        screen.blit(bullet.surf, bullet.rect)
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)  # True removes the enemy on collision
        for enemy in enemy_hit_list:
            score_value += (50 * settings.MODIFIER)
            explosion = Explosion(enemy.rect.center) # Create an explosion at the enemy's position
            all_sprites.add(explosion)  # Add the explosion to all_sprites group
        if enemy_hit_list:  # Remove the bullet upon collision with an enemy
            bullet.kill()

    # Enemy collision
    collided_enemy = pygame.sprite.spritecollideany(player_obj, enemies)
    if collided_enemy and not collided_enemy.collided:
        if player_obj.defense > 0:
            collided_enemy.kill()
            collided_enemy.collided = True
            player_obj.defense -= 1
            player.move_up_sound.stop()
            player.move_down_sound.stop()
            player.collision_sound.play()
            print(f"CLOSE CALL! Defense is now: {player_obj.defense}")
        else:
            player_obj.kill()
            player.move_up_sound.stop()
            player.move_down_sound.stop()
            player.collision_sound.play()
            running = False

    # Powerup Collision
    for powerup in powerups:
        # Check if any powerups have collided with the player
        powerup_collide = pygame.sprite.spritecollide(player_obj, powerups, True)  # True removes the enemy on collision
        if powerup_collide:
            player.powerup_sound.stop()
            player.move_up_sound.stop()
            player.move_down_sound.stop()
            player.powerup_sound.play()
            if isinstance(powerup, player.Shield) and not powerup.collided:
                powerup.kill()
                player_obj.defense += 1  # Give bonus to player
                print(f"Power-up type: {powerup.powertype}")
            elif isinstance(powerup, player.Double_Points) and not powerup.collided:
                now = pygame.time.get_ticks()
                if now - powerup.creation_time > powerup.duration:
                    settings.MODIFIER = 1
                else:
                    settings.MODIFIER = 2
                powerup.kill()
                print(f"Power-up type: {powerup.powertype}")
            powerup.collided = True


    # Powerup Collision
    for cloud in clouds:
        if cloud.rect.contains(player_obj):
            print("Player is completely covered by the cloud")
            # TODO:
            # ADD PLAYER SEEKING MISSILES
            # IF PLAYER IS HIDDEN BEHIND A CLOUD, THEN SEEKING MISSILE CAN'T TRACK PLAYER


    pygame.display.flip()
    clock.tick(30) # Ensure program maintains a rate of 30 frames per second

pygame.mixer.music.stop()
pygame.mixer.quit()

# updates highscore.txt if current score is greater than previous high score.
if previous_high_score < score_value:
    with open('highscore.txt', 'w', encoding = 'utf-8') as file:
        file.write(f'{score_value}')