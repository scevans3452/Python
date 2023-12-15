import pygame, sys

from gameloop import Game
from button import Button
from pygame.locals import (
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )

SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)

class MainMenu:
    def __init__(self):
        self.running = True
        self.music_playing = False  # Add a flag to track if music is playing
        self.screen_width, self.screen_height = SCREEN.get_size()
        self.menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(640, 100))

    def run(self, state_manager):
        pygame.mixer.init()
        # Load the background music only if it's not playing
        if not self.music_playing:
            pygame.mixer.music.load("./assets/main_menu.mp3")
            pygame.mixer.music.play(loops=-1)
            self.music_playing = True
            
        while self.running:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.fill((0, 0, 0))  # Clear screen
            # Buttons
            PLAY_BUTTON    = Button(image=None, pos=(640, 250), text_input="PLAY",    font=get_font(75), base_color="red", hovering_color="White")
            OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="OPTIONS", font=get_font(75), base_color="red", hovering_color="White")
            QUIT_BUTTON    = Button(image=None, pos=(640, 550), text_input="QUIT",    font=get_font(75), base_color="red", hovering_color="White")
            
            pygame.display.set_caption('Main Menu')

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
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
                                self.music_playing = False
                                state_manager.start_main_menu()
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
    
    def run(self, state_manager):
        while self.running:
            SCREEN.fill((0, 0, 0))  # Clear screen
            menu_text = get_font(100).render("OPTIONS", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # Buttons
            BACK_BUTTON    = Button(image=None, pos=(640, 250), text_input="BACK", font=get_font(75), base_color="red", hovering_color="White")

            pygame.display.set_caption('Options Menu')

            
            BACK_BUTTON.changeColor(MENU_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            SCREEN.blit(menu_text, menu_rect)

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
                    BACK_BUTTON.changeColor(MENU_MOUSE_POS)
                    BACK_BUTTON.update(SCREEN)
                    if BACK_BUTTON.hover(MENU_MOUSE_POS):
                        state_manager.change_state('main_menu')
                        state_manager.run_current_state(state_manager)
                        
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

    def change_state(self, new_state):
        self.current_state = new_state

    def run_current_state(self, state):
        self.states[self.current_state].run(state)

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

    while True:
        state_manager.run_current_state(state_manager)
        clock.tick(60)  # Limit frame rate to 60 FPS

if __name__ == "__main__":
    main()
