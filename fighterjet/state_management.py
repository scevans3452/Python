import pygame, pygame_widgets, sys, settings

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

def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)

class MainMenu:
    def __init__(self):
        self.running = True
        # self.music_playing = False  # Add a flag to track if music is playing
        self.screen_width, self.screen_height = SCREEN.get_size()
        self.menu_text = get_font(100).render("FIGHTER PILOT", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(640, 150))

    def run(self, state_manager):
        while self.running:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.fill((0, 0, 0))  # Clear screen
            # Buttons
            PLAY_BUTTON         = Button(image=None, pos=(640, 300), text_input="PLAY",         font=get_font(70), base_color="red", hovering_color="White")
            OPTIONS_BUTTON      = Button(image=None, pos=(640, 400), text_input="OPTIONS",      font=get_font(70), base_color="red", hovering_color="White")
            ACHIEVEMENTS_BUTTON = Button(image=None, pos=(640, 500), text_input="ACHIEVEMENTS", font=get_font(70), base_color="red", hovering_color="White")
            QUIT_BUTTON         = Button(image=None, pos=(640, 600), text_input="QUIT",         font=get_font(70), base_color="red", hovering_color="White")
            
            pygame.display.set_caption('Main Menu')

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, ACHIEVEMENTS_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            SCREEN.blit(self.menu_text, self.menu_rect)

            # Check for events
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                if event.type == QUIT:
                    self.running = False
                    # Quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(SCREEN)
                        if button.hover(MENU_MOUSE_POS):
                            if button.text_input   == "PLAY":
                                state_manager.start_game()
                                # self.music_playing = False
                                state_manager.start_main_menu() # don't want new instance, just got back to where we were
                            elif button.text_input == "OPTIONS":
                                state_manager.change_state('options_menu')
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
            menu_text = get_font(100).render("OPTIONS", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            BACK_BUTTON = Button(image=None, pos=(640, 250), text_input="BACK", font=get_font(75),
                                 base_color="red", hovering_color="White")
            BACK_BUTTON.changeColor(MENU_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            SCREEN.blit(menu_text, menu_rect)

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

class StateManager:
    def __init__(self):
        self.states = {
            'main_menu': MainMenu(),
            'options_menu': OptionsMenu(),
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
