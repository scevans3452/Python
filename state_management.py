import pygame, sys
from button import Button
from pygame.locals import (
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )

def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)

class MainMenu:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_width, self.screen_height = self.screen.get_size()
    
    def run(self, state_manager):
        while self.running:
            self.screen.fill((0, 0, 0))  # Clear screen
            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # Buttons
            PLAY_BUTTON    = Button(image=None, pos=(640, 250), text_input="PLAY",    font=get_font(75), base_color="red", hovering_color="White")
            OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="OPTIONS", font=get_font(75), base_color="red", hovering_color="White")
            QUIT_BUTTON    = Button(image=None, pos=(640, 550), text_input="QUIT",    font=get_font(75), base_color="red", hovering_color="White")
            
            pygame.display.set_caption('Main Menu')

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(self.screen)

            self.screen.blit(MENU_TEXT, MENU_RECT)

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
                        button.update(self.screen)
                        if button.hover(MENU_MOUSE_POS):
                            # print(f"inside the loop at least.")
                            if button.text_input   == "PLAY":
                                state_manager.change_state('gameplay')
                            elif button.text_input == "OPTIONS":
                                state_manager.change_state('options_menu')
                            elif button.text_input == "QUIT":
                                pygame.quit()
                                sys.exit()
            
            # Update and render elements specific to the main menu
            pygame.display.flip()

class OptionsMenu:
    # Similar structure to MainMenu class
    pass

class GameLoop:
    pass
    # Similar structure to MainMenu class but for the actual gameplay

class StateManager:
    def __init__(self):
        self.states = {
            'main_menu': MainMenu(),
            'options_menu': OptionsMenu(),
            'gameplay': GameLoop()
        }
        self.current_state = 'main_menu'

    def change_state(self, new_state):
        self.current_state = new_state

    def run_current_state(self):
        self.states[self.current_state].run()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    state_manager = StateManager()
    main_menu = MainMenu()
    main_menu.run(state_manager)

    while True:
        state_manager.run_current_state()
        clock.tick(60)  # Limit frame rate to 60 FPS

if __name__ == "__main__":
    main()
