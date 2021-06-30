import pygame
import pygame.freetype
from constants import *

pygame.init()


class Button:
    """Creates an instance of a button with a center positon, text, size, color, background color, and action to return
    when the button is clicked
    References this tutorial: https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
    """


    def __init__(self, center, text, text_size, text_rgb, bg_rgb=YELLOW, action=None):

        self.mouse_over = False
        self.action = action

        default_text = self.create_surface(text,text_size, text_rgb, bg_rgb)
        hovered_text = self.create_surface(text, text_size*1.2, text_rgb, bg_rgb)

        self.text_images = [default_text, hovered_text]
        self.text_rects = [default_text.get_rect(center=center), hovered_text.get_rect(center=center)]

    def create_surface(self, text, text_size, text_rgb,bg_rgb):
        """
        Creates and returns a surface containing text. Receives the text to be rendered, the text size, and the text color.
        Renders the background as YELLOW by default to match the window fill
        """

        # create font object
        font = pygame.freetype.SysFont('Courier', text_size)

        # render it with appropriate size and color, store as a surface
        text_surface, _ = font.render(text, text_rgb, bg_rgb)
        # return the surface
        return text_surface

    @property
    def image(self):
        """Returns the smaller text image if the button is not hovered over, and the larger one if it is hovered over"""
        return self.text_images[1] if self.mouse_over else self.text_images[0]

    @property
    def rect(self):
        """Returns the smaller or larger text rect depending on if the text is hovered over"""
        return self.text_rects[1] if self.mouse_over else self.text_rects[0]

    def update_button(self, mouse_pos, mouse_up):
        """Checks if the button is being interacted with"""
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw_button(self, window):
        """Draws the button onto a surface passed to this method"""
        # Image is blitted onto the screen (essentially copied onto another surface) and the rect establishes the position
        window.blit(self.image, self.rect)