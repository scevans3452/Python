import pygame, pygame_widgets, sys, settings, math

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from gameloop import Game
from button import Button
from pygame.locals import (
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )



SCREEN               = pygame.display.set_mode((1280, 720))
center_offset_width  = int(SCREEN.get_width()/2)
center_offset_height = int(SCREEN.get_height()/2)
slider_width         = 500
slider_height        = 2
slider_text_width    = 50
slider_output_width  = 30
slider_offset_width  = (center_offset_width - int(slider_width/2))
slider_offset_height = (center_offset_height - int(slider_height/2))
#load image
bg = pygame.image.load("./assets/skyline_updated.png").convert()
bg_width = bg.get_width()
bg_height = bg.get_height()  # Get the original height of the image

# Calculate the scale factor for the image height to fit the screen
scale_factor = SCREEN.get_height() / bg_height

# Resize the image to fit the screen height while maintaining aspect ratio
bg = pygame.transform.scale(bg, (int(bg_width * scale_factor), SCREEN.get_height()))

def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)

def read_high_score(self, file):
        with open(file, 'r', encoding='utf-8') as file:
            read_from_file = file.read()
            previous_high_score = int(read_from_file)
        return previous_high_score

class MainMenu:
    def __init__(self):
        self.running = True
        self.screen_width, self.screen_height = SCREEN.get_size()
        self.menu_text = get_font(100).render("FIGHTER PILOT", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(640, 150))
        self.scroll = 0
        self.tiles = math.ceil(SCREEN.get_width()  / bg.get_width()) + 1
        self.focused_button_index = 0  # Initially, the first button is focused

    def run(self, state_manager):
        while self.running:
            SCREEN.fill((0, 0, 0))  # Clear screen
            #draw scrolling background
            for i in range(0, self.tiles):
                SCREEN.blit(bg, (i * bg.get_width() + self.scroll, 0))
                # pygame.draw.rect(screen, (255, 0, 0), (i * bg.get_width() + scroll, 0, bg.get_width(), SCREEN_HEIGHT), 1)

            #scroll background
            self.scroll -= .1

            #reset scroll
            if abs(self.scroll) > bg.get_width():
                self.scroll = 0
                
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SCREEN.blit(bg, (0,-100))
            # Buttons
            PLAY_BUTTON         = Button(image=None, pos=(640, 300), text_input="PLAY",         font=get_font(70), base_color="red", hovering_color="green")
            OPTIONS_BUTTON      = Button(image=None, pos=(640, 400), text_input="OPTIONS",      font=get_font(70), base_color="red", hovering_color="green")
            ACHIEVEMENTS_BUTTON = Button(image=None, pos=(640, 500), text_input="ACHIEVEMENTS", font=get_font(70), base_color="red", hovering_color="green")
            QUIT_BUTTON         = Button(image=None, pos=(640, 600), text_input="QUIT",         font=get_font(70), base_color="red", hovering_color="green")

            button_list = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, ACHIEVEMENTS_BUTTON]
            
            pygame.display.set_caption('Main Menu')

            for button in button_list:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            SCREEN.blit(self.menu_text, self.menu_rect)

            # Check for events
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, ACHIEVEMENTS_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(SCREEN)
                        if button.hover(MENU_MOUSE_POS):
                            if button.text_input   == "PLAY":
                                state_manager.start_game()
                                state_manager.start_main_menu()
                            elif button.text_input == "OPTIONS":
                                state_manager.change_state('options_menu')
                                state_manager.run_current_state(state_manager)
                            elif button.text_input == "ACHIEVEMENTS":
                                state_manager.change_state('achievements_menu')
                                state_manager.run_current_state(state_manager)
                            elif button.text_input == "QUIT":
                                pygame.quit()
                                sys.exit()
            
            # Update and render elements specific to the main menu
            pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.mixer.quit()

class OptionsMenu:
    def __init__(self):
        self.running = True
        self.screen_width, self.screen_height = SCREEN.get_size()
        self.menu_text = get_font(100).render("OPTIONS", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(640, 150))

        # VOLUME CONTROLS
        self.volume_control = {
            'volume_slider' : Slider(SCREEN, slider_offset_width, slider_offset_height, slider_width, slider_height, min=0, max=99, step=1, initial=99, handleColour=(0, 255, 255), colour=(255, 255, 255), handleRadius=10),
            'description'   : TextBox(SCREEN, slider_offset_width - slider_text_width - 80, slider_offset_height+slider_height, slider_text_width, slider_height*7, fontSize=16, textColour=(255,222,222), colour=(0, 0, 0)),
            'output'        : TextBox(SCREEN, slider_offset_width + slider_width + 20, slider_offset_height+slider_height, slider_output_width, slider_height*7, fontSize=16, textColour=(255,222,222), colour=(0, 0, 0))
        }
        self.volume_control['output'].disable()  # Act as label instead of textbox
        self.volume_control['description'].setText("MUSIC VOLUME")  # Act as label instead of textbox

    def run(self, state_manager):
        pygame.mixer.init()
        while self.running:
            events = pygame.event.get()
            SCREEN.fill((0, 0, 0))  # Clear screen

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            BACK_BUTTON = Button(image=None, pos=(640, SCREEN.get_height() - 100), text_input="BACK", font=get_font(75),
                                 base_color="red", hovering_color="White")
            BACK_BUTTON.changeColor(MENU_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            SCREEN.blit(self.menu_text, self.menu_rect)

            # Draw and update the slider
            # FOR LOOP IF THERE ARE MORE SLIDERS SETUP
            self.volume_control['volume_slider'].listen(events)
            self.volume_control['volume_slider'].draw()

            slider_value = self.volume_control['volume_slider'].getValue()
            settings.ACTUAL_VOLUME = slider_value / 99.0            # Convert the slider value to a volume between 0.0 and 1.0
            pygame.mixer.music.set_volume(settings.ACTUAL_VOLUME)   # Set the mixer volume

            # Check for events
            for event in events:
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        state_manager.start_main_menu()
                        # pygame.quit()
                        # sys.exit()
                if event.type == QUIT:
                    self.running = False
                    # Quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    BACK_BUTTON.changeColor(MENU_MOUSE_POS)
                    BACK_BUTTON.update(SCREEN)
                    if BACK_BUTTON.hover(MENU_MOUSE_POS):
                        state_manager.start_main_menu()
                self.volume_control['output'].setText(self.volume_control['volume_slider'].getValue())

            pygame_widgets.update(events)
            pygame.display.update()
                        
            # Update and render elements specific to the options menu
            pygame.display.flip()

class AchievementsMenu:
    def __init__(self):
        self.running = True
        self.screen_width, self.screen_height = SCREEN.get_size()
        self.menu_text = get_font(100).render("ACHIEVEMENTS", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(640, 150))

        # Add all achievements to map
        self.achievements_map = {
            'highscore'         : get_font(24).render("HIGHSCORE: " + str(read_high_score(self, 'highscore.txt')), True, "#b68f40"),
            'next'              : get_font(24).render("NEXT ACHIEVEMENT", True, "#b68f40"),
            'next2'              : get_font(24).render("NEXT ACHIEVEMENT", True, "#b68f40"),
        }

        # Create list of key/values for dynamically adding later
        self.achievements_keys = list(self.achievements_map.keys())
        self.achievements_values = list(self.achievements_map.values())

    def run(self, state_manager):
        pygame.mixer.init()
        while self.running:
            events = pygame.event.get()
            SCREEN.fill((0, 0, 0))  # Clear screen
            
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            BACK_BUTTON = Button(image=None, pos=(640, SCREEN.get_height() - 100), text_input="BACK", font=get_font(75),
                                 base_color="red", hovering_color="White")
            BACK_BUTTON.changeColor(MENU_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            SCREEN.blit(self.menu_text, self.menu_rect)
            for index, key in enumerate(self.achievements_keys):
                if index < len(self.achievements_values):
                    text_surface = self.achievements_values[index]
                    center_x = (SCREEN.get_width() - text_surface.get_width()) // 2
                    y_position = 300 + index * 30  # Adjust these values as needed
                    SCREEN.blit(text_surface, (center_x, y_position))


            # Check for events
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        state_manager.start_main_menu()
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    BACK_BUTTON.changeColor(MENU_MOUSE_POS)
                    BACK_BUTTON.update(SCREEN)
                    if BACK_BUTTON.hover(MENU_MOUSE_POS):
                        state_manager.start_main_menu()
            pygame.display.update()
            pygame.display.flip()

class StateManager:
    def __init__(self):
        self.states = {
            'main_menu': MainMenu(),
            'options_menu': OptionsMenu(),
            'achievements_menu': AchievementsMenu(),
            'gameplay': Game()
        }
        self.current_state = 'main_menu'
        self.options_screen_active = False

    def change_state(self, new_state):
        self.current_state = new_state

    def run_current_state(self, state):
        self.states[self.current_state].run(state)

    def play_game_music(self):
        # Load and play background music
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/game_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def start_game(self):
        # Set the current state to 'gameplay' and start the game loop
        self.states['gameplay'] = Game()  # Create a new Game instance
        self.change_state('gameplay')
        self.run_current_state(self)

    def start_main_menu(self):
        self.states['main_menu'] = MainMenu()
        self.change_state('main_menu')
        self.run_current_state(self)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    state_manager = StateManager()
    state_manager.play_game_music()

    while True:
        state_manager.run_current_state(state_manager)
        clock.tick(60)  # Limit frame rate to 60 FPS

if __name__ == "__main__":
    main()
