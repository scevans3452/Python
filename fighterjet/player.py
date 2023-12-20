import pygame, settings, random, math
# Setup for sounds. Defaults are good.
pygame.mixer.init()
pygame.init()
settings.init() 

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_SPACE,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

# Sound sources: Jon Fincher
collision_sound = pygame.mixer.Sound("./assets/Collision.ogg")
move_up_sound   = pygame.mixer.Sound("./assets/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("./assets/Falling_putter.ogg")
powerup_sound   = pygame.mixer.Sound("./assets/powerup.ogg")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        img1 = pygame.image.load("./assets/jet_new1.png").convert()
        img2 = pygame.image.load("./assets/jet_new2.png").convert()
        img1.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        img2.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.player_frames = [
            img1,
            img1,
            img1,
            img1,
            img1,
            img1,
            img2
        ]
        self.frame_index    = 0
        self.counter        = 60
        self.frame_rate     = 15  # Adjust the frame rate (frames per second)
        self.surf           = self.player_frames[self.frame_index]
        self.rect           = self.surf.get_rect()
        self.last_shot      = 0  # Initialize the time of the last shot
        self.bullets        = pygame.sprite.Group()  # Group for holding bullets
        self.ammo           = 10
        self.defense        = 0
        # Define the length of the aiming line
        self.aiming_line_length = 500  # Adjust as needed
        self.multi_shot_enabled = False
    
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -6)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 8)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-8, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)
        if pressed_keys[K_SPACE]:  # Check for spacebar press to fire projectiles
            current_time = pygame.time.get_ticks()  # Get the current time
            time_since_last_shot = current_time - self.last_shot
            if time_since_last_shot >= 500 and self.ammo > 0:  # Limit firing rate to once per second (1000 milliseconds)
                self.ammo -= 1
                self.fire(self.multi_shot_enabled)
                self.last_shot = current_time  # Update the time
                
        # Update the animation frame based on the frame rate
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.frame_index += 1
            if self.frame_index >= len(self.player_frames):
                self.frame_index = 0
            self.surf = self.player_frames[self.frame_index]
            self.counter = 0  # Reset the counter

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
    
    def fire(self, bool):
        trajectory_list = ["right", "up_right", "down_right"]
        if self.multi_shot_enabled:
            # self.fire(["right", "up_right", "down_right"])
            for trajectory in trajectory_list:
                bullet = Bullet(self.rect.midright, trajectory)
                self.bullets.add(bullet)  # Add the bullet to the bullets group
        else:
            bullet = Bullet(self.rect.midright)  # Create a bullet at player's left side
            self.bullets.add(bullet)  # Add the bullet to the bullets group

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, trajectory="right"):
        super(Bullet, self).__init__()
        self.base_image = pygame.image.load("./assets/laser.png").convert()
        self.surf = pygame.transform.scale(self.base_image, (settings.BULLET_WIDTH, settings.BULLET_HEIGHT))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(midleft=(pos[0] - 34, pos[1] + 5))
        self.speed = 12  # Adjust the bullet's speed as needed
        self.trajectory = trajectory  # Store the trajectory
        self.rotation_angle = -30
        if self.trajectory == "up_right":
            self.rotation_angle = self.rotation_angle
        elif self.trajectory == "down_right":
            self.rotation_angle = abs(self.rotation_angle)
        elif self.trajectory == "right":
            self.rotation_angle = 0
        self.surf = pygame.transform.rotate(self.surf, self.rotation_angle)

    def update(self, x=None, y=0):
        # Convert angle to radians for math functions
        angle_radians = math.radians(abs(self.rotation_angle))

        # Calculate the vertical distance (y)
        if x is None:
            x = self.speed  # Set x to self.speed if no x value is provided
        if self.trajectory == "up_right":       # Logic for bullets moving diagonally up and right
            y = x * math.tan(angle_radians)
        elif self.trajectory == "down_right":   # Logic for bullets moving diagonally down and right
            y = -(x * math.tan(angle_radians))
        self.rect.move_ip(x, y)
        if self.rect.left > settings.SCREEN_WIDTH or self.rect.right < 0 or self.rect.top < 0 or self.rect.bottom > settings.SCREEN_HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./assets/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(settings.SCREEN_WIDTH + 20, settings.SCREEN_WIDTH + 100),
                random.randint(12, settings.SCREEN_HEIGHT - 12), # using 12's because enemies can sometimes be impossible to shoot, or slightly off screen
            )
        )
        self.speed = random.randint(5, 12)
        self.collided = False

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()