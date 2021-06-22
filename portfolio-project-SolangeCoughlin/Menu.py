import pygame
from Button import *
from constants import *


class Menu:

    def __init__(self, title_text, width=800, height=600):
        self.title_text = title_text
        self.width = width
        self.height = height
        self.running = True
        self.playing = False
        self.font = pygame.font.SysFont('Courier', 50)

    # make a window
    def draw_window(self, window):
        window.fill(YELLOW)
        #window.blit(self.title_text, (35, 35))

        # make buttons
        play = Button('Play', (WIDTH//2)-90, (HEIGHT//2)-20, window)
        play.make_button()

    # do something with button presses

    def main(self):

        pygame.init()

        window = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Janggi")
        icon = pygame.image.load('assets/chess.png')

        pygame.display.set_icon(icon)

        while self.running is True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
            self.draw_window(window)
            title_img = self.font.render(self.title_text, True, (0, 0, 0))
            title_len = title_img.get_width()
            window.blit(title_img, ((WIDTH // 2 - title_len // 2), HEIGHT//5))

            pygame.display.update()

menu = Menu("Janggi")
menu.main()