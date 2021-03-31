import pygame
pygame.init()

WIDTH = 630
HEIGHT = 700

COLS = 9
ROWS = 10

SQUARE_SIZE = HEIGHT//ROWS    # Could also be calculated with WIDTH//COLS, squares are square. 75 pixels

# Colors
WHITE = (255, 255, 255)
YELLOW = (239,228,176)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

board = pygame.image.load('assets/janggiboard.png')

scale_size = 76
half_icon = scale_size//2

FONT = pygame.font.SysFont(None,75)

highlight = pygame.image.load('assets/highlight_block.png')

# Importing game piece images and scaling to 40x40
red_gen = pygame.image.load('assets/red_general.png')
red_gen = pygame.transform.scale(red_gen,(scale_size,scale_size))

red_sol = pygame.image.load('assets/red_soldier.png')
red_sol = pygame.transform.scale(red_sol,(scale_size,scale_size))

red_char = pygame.image.load('assets/red_chariot.png')
red_char = pygame.transform.scale(red_char,(scale_size,scale_size))

red_adv = pygame.image.load('assets/red_advisor.png')
red_adv = pygame.transform.scale(red_adv,(scale_size,scale_size))

red_can = pygame.image.load('assets/red_cannon.png')
red_can = pygame.transform.scale(red_can,(scale_size,scale_size))

red_el = pygame.image.load('assets/red_elephant.png')
red_el = pygame.transform.scale(red_el,(scale_size,scale_size))

red_horse = pygame.image.load('assets/red_horse.png')
red_horse = pygame.transform.scale(red_horse,(scale_size,scale_size))

blue_gen = pygame.image.load('assets/blue_general.png')
blue_gen = pygame.transform.scale(blue_gen,(scale_size,scale_size))

blue_sol = pygame.image.load('assets/blue_soldier.png')
blue_sol = pygame.transform.scale(blue_sol,(scale_size,scale_size))

blue_char = pygame.image.load('assets/blue_chariot.png')
blue_char = pygame.transform.scale(blue_char,(scale_size,scale_size))

blue_adv = pygame.image.load('assets/blue_advisor.png')
blue_adv = pygame.transform.scale(blue_adv,(scale_size,scale_size))

blue_can = pygame.image.load('assets/blue_cannon.png')
blue_can = pygame.transform.scale(blue_can,(scale_size,scale_size))

blue_el = pygame.image.load('assets/blue_elephant.png')
blue_el = pygame.transform.scale(blue_el,(scale_size,scale_size))

blue_horse = pygame.image.load('assets/blue_horse.png')
blue_horse = pygame.transform.scale(blue_horse,(scale_size,scale_size))