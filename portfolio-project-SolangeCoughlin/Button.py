import pygame

pygame.init()


class Button:
    """Creates an instance of a button, which will display text to the user and can detect when it is clicked.
    Behavior of the button when clicked is defined where the button is implemented"""

    def __init__(self, btn_text, x, y, window, width=180, height=40):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.btn_text = btn_text
        self.window = window

    def make_button(self):
        """Creates an instances of a button, and returns True if the button is clicked and False otherwise.
        Also draws the button onto the window defined when the button is initialized"""

        clicked = False
        action = False

        pos = pygame.mouse.get_pos()

        button = pygame.Rect(self.x, self.y, self.width, self.height)
        font = pygame.font.SysFont('Courier',20)

        if button.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.window, (230, 230, 230), button)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked is True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.window, (230, 230, 230), button)
        else:
            pygame.draw.rect(self.window, (255, 255, 255), button)

        txt_img = font.render(self.btn_text,True, (0,0,0))
        text_len = txt_img.get_width()
        self.window.blit(txt_img, ((self.x + self.width//2 - text_len//2), self.y+10))
        return action
