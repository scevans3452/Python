from button import Button
import gameloop, settings, pygame, sys

from pygame.locals import (
        RLEACCEL,
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)

def main_menu():
    while True:

        screen.fill('black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Check for events
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()
        
        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        pygame.display.set_caption('Main Menu')

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)


main_menu()
# gameloop.game_loop()