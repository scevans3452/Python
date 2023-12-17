import pygame, random, sys, settings, player, settings
from button import Button
from explosion import Explosion
from cloud import Cloud
from pygame.locals import (RLEACCEL, K_ESCAPE, KEYDOWN, QUIT)

def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)

class Game:
    def __init__(self):
        # Set the screen to windowed mode
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Fighter Pilot')

        # Variables
        self.timer_duration         = 5000  # 5000 milliseconds = 5 seconds
        self.background_color       = (135, 206, 250)
        self.score_value            = 0
        self.previous_high_score    = 0
        self.roll_breakdown         = [0,1,2,3] # breakdown of percentage of the roll from max potential
        self.font                   = pygame.font.Font('freesansbold.ttf', 32)
        self.running                = True
        self.paused                 = False  # Initially, the game is not paused

        # Create custom events
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDCLOUD, 1000)

        self.INCREASE_SCORE = pygame.USEREVENT + 3
        pygame.time.set_timer(self.INCREASE_SCORE, 100)

        self.ADDPOWERUP = pygame.USEREVENT + 4
        self.set_interval(settings.MIN_INTERVAL, settings.MAX_INTERVAL, "powerup", self.ADDPOWERUP)

        self.TIMER_EVENT = pygame.USEREVENT + 5

        # Create groups to hold sprites
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Instantiate player. Right now, this is just a rectangle.
        self.player_obj = player.Player()

        # Setup the clock for a decent framerate
        self.clock = pygame.time.Clock()

        self.all_sprites.add(self.player_obj)
        self.all_sprites.add(self.player_obj.bullets)  # Add bullets to the group

        # Preload objects
        for _ in range(random.randint(4, 10)):
            new_cloud = Cloud()
            new_cloud.rect.center = (
                random.randint(0, settings.SCREEN_WIDTH),
                random.randint(0, settings.SCREEN_HEIGHT),
            )
            new_cloud.update_opacity(random.randint(150, 220))
            self.clouds.add(new_cloud)
            self.all_sprites.add(new_cloud)


    def read_high_score(self, file):
        with open(file, 'r', encoding='utf-8') as file:
            read_from_file = file.read()
            previous_high_score = int(read_from_file)
        return previous_high_score

    def show_score(self, x, y):
        score = self.font.render("Score: " + str(self.score_value), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def show_previous_high_score(self, x, y):
        self.high_score = self.font.render("High Score: " + str(self.previous_high_score), True, (255, 255, 255))
        self.screen.blit(self.high_score, (x, y))

    def show_defense(self, x, y):
        self.text = self.font.render("Defense: " + str(self.player_obj.defense), True, (255, 255, 255))
        self.screen.blit(self.text, (x, y))

    def show_ammo(self, x, y):
        self.text = self.font.render("Ammo: " + str(self.player_obj.ammo), True, (255, 255, 255))
        self.screen.blit(self.text, (x, y))

    def set_interval(self, min, max, game_object, group):
        interval = random.randint(min, max)
        pygame.time.set_timer(group, interval)
        # print(f"New {game_object} interval: {interval/1000} seconds")

    def run(self, state):

        pygame.init()

        # Start the main game loop
        while self.running:
            if not self.paused:
                pygame.mixer.music.set_volume(settings.ACTUAL_VOLUME)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.paused = not self.paused
                            # self.running = False
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    # Add a new enemy
                    elif event.type == self.ADDENEMY:
                        # Create the new enemy and add it to sprite groups
                        new_enemy = player.Enemy()
                        self.enemies.add(new_enemy)
                        self.all_sprites.add(new_enemy)

                    # Add a new cloud
                    elif event.type == self.ADDCLOUD:
                        # Create the new cloud and add it to sprite groups
                        new_cloud = Cloud()
                        new_cloud.update_opacity(random.randint(160, 220))
                        self.clouds.add(new_cloud)
                        self.all_sprites.add(new_cloud)

                    # score uptick
                    elif event.type == self.INCREASE_SCORE:
                        self.score_value += (1 * settings.MODIFIER)

                    # Add a powerup
                    elif event.type == self.ADDPOWERUP:
                        self.power_list = [player.Shield(), player.Double_Points(), player.Ammo()]
                        self.new_power = self.power_list[random.randint(0, (len(self.power_list)-1))]
                        # print(f"{new_power}")
                        self.powerups.add(self.new_power)
                        self.all_sprites.add(self.new_power)
                        # Reset the timer with a new random interval
                        self.set_interval(settings.MIN_INTERVAL, settings.MAX_INTERVAL, "powerup", self.ADDPOWERUP)
                    
                    elif event.type == self.TIMER_EVENT:
                        settings.MODIFIER = 1
                        self.background_color = (135, 206, 250)  # Reset back to the original color

                # Get the set of keys pressed and check for user input
                pressed_keys = pygame.key.get_pressed()
                self.player_obj.update(pressed_keys)
                self.player_obj.bullets.update()

                # Update the position of enemies and clouds
                self.enemies.update()
                self.powerups.update()
                self.clouds.update()

                # Fill the screen with sky blue
                self.screen.fill(self.background_color)
                self.previous_high_score = self.read_high_score('highscore.txt')
                self.show_score(0, 0)
                self.show_previous_high_score(0, 60)
                self.show_defense(0, settings.SCREEN_HEIGHT-50)
                self.show_ammo   (0, settings.SCREEN_HEIGHT-100)

                self.all_sprites.add(self.player_obj.bullets)  # Add bullets to the group

                # Draw all sprites
                for entity in self.all_sprites:
                    if isinstance(entity, Explosion):
                        self.screen.blit(entity.image, entity.rect)
                        entity.update()
                    else:
                        self.screen.blit(entity.surf, entity.rect)



                #################
                #   COLLISIONS  #
                #################
                for bullet in self.player_obj.bullets:
                    self.screen.blit(bullet.surf, bullet.rect)
                    self.enemy_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, True)  # True removes the enemy on collision
                    for enemy in self.enemy_hit_list:
                        self.score_value += (50 * settings.MODIFIER)
                        self.explosion = Explosion(enemy.rect.center) # Create an explosion at the enemy's position
                        self.all_sprites.add(self.explosion)  # Add the explosion to all_sprites group
                    if self.enemy_hit_list:  # Remove the bullet upon collision with an enemy
                        bullet.kill()

                # Enemy collision
                collided_enemy = pygame.sprite.spritecollideany(self.player_obj, self.enemies)
                if collided_enemy and not collided_enemy.collided:
                    if self.player_obj.defense > 0:
                        collided_enemy.kill()
                        collided_enemy.collided = True
                        self.player_obj.defense -= 1
                        player.move_up_sound.stop()
                        player.move_down_sound.stop()
                        player.collision_sound.play()
                        print(f"CLOSE CALL! Defense is now: {self.player_obj.defense}")
                    else:
                        self.player_obj.kill()
                        player.move_up_sound.stop()
                        player.move_down_sound.stop()
                        player.collision_sound.play()
                        self.running = False


                # Powerup Collision
                for powerup in self.powerups:
                    if pygame.sprite.collide_rect(self.player_obj, powerup):
                        print(f"Power-up type: {powerup.powertype}")
                        player.powerup_sound.stop()
                        player.move_up_sound.stop()
                        player.move_down_sound.stop()
                        player.powerup_sound.play()
                        
                        if isinstance(powerup, player.Shield) and not powerup.collided:
                            powerup.kill()
                            self.player_obj.defense += 1
                            powerup.collided = True
                        
                        elif isinstance(powerup, player.Ammo) and not powerup.collided:
                            powerup.kill()
                            powerup.collided = True
                            self.player_obj.ammo += 1
                            
                        elif isinstance(powerup, player.Double_Points) and not powerup.collided:
                            powerup.kill()
                            settings.MODIFIER = 2                                           # Double points
                            self.background_color = (225, 255, 0)                           # Gold
                            pygame.time.set_timer(self.TIMER_EVENT, self.timer_duration)    # Start the timer
                            powerup.collided = True

                # Cloud Collision
                for cloud in self.clouds:
                    if cloud.rect.contains(self.player_obj):
                        print("Player is completely covered by the cloud")
                        # TODO:
                        # ADD PLAYER SEEKING MISSILES
                        # IF PLAYER IS HIDDEN BEHIND A CLOUD, THEN SEEKING MISSILE CAN'T TRACK PLAYER


                pygame.display.flip()
                self.clock.tick(30) # Ensure program maintains a rate of 30 frames per second

            else:  # When paused, show the pause menu
                pygame.mixer.music.set_volume(settings.ACTUAL_VOLUME*.3)
                MENU_MOUSE_POS = pygame.mouse.get_pos()

                # Create a surface with per-pixel alpha
                alpha_surface = pygame.Surface((500, 300), pygame.SRCALPHA)
                pygame.draw.rect(alpha_surface, (135, 206, 250, 100), (0, 0, 500, 300))

                # Blit the surface onto the screen
                self.screen.blit(alpha_surface, ((self.screen.get_width() - 500) // 2, (self.screen.get_height() - 300) // 2))

                # Render and display your pause menu elements
                pause_text = get_font(50).render("Paused", True, (255, 255, 255))
                pause_text_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, (self.screen.get_height() - 300) // 2 + 50))

                RESUME_BUTTON = Button(image=None, pos=(self.screen.get_width() // 2, (self.screen.get_height() - 300) // 2 + 120), text_input="Resume", font=get_font(40), base_color="red", hovering_color="White")
                QUIT_BUTTON = Button(image=None, pos=(self.screen.get_width() // 2, (self.screen.get_height() - 300) // 2 + 180), text_input="Main Menu", font=get_font(40), base_color="red", hovering_color="White")

                self.screen.blit(pause_text, pause_text_rect)

                for button in [RESUME_BUTTON, QUIT_BUTTON]:
                    button.changeColor(MENU_MOUSE_POS)
                    button.update(self.screen)

                # Check for events in the pause menu
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RESUME_BUTTON.hover(MENU_MOUSE_POS):
                            self.paused = not self.paused  # Resume the game
                        if QUIT_BUTTON.hover(MENU_MOUSE_POS):
                            self.running = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.paused = not self.paused
                    if event.type == QUIT:
                        # Quit the game
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        # pygame.mixer.music.stop()
        # pygame.mixer.quit()