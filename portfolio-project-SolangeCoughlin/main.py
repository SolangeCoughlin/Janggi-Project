import pygame
from constants import *
from JanggiGame import *

pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))

    #Update the caption and icon of the game window
pygame.display.set_caption("Janggi")
icon = pygame.image.load('assets/chess.png')

pygame.display.set_icon(icon)
Janggi = JanggiGame()

def draw_board():
    window.fill(YELLOW)
    window.blit(board,(35,35))

def get_mouse_position():
    pos = pygame.mouse.get_pos()
    pos = (pos[0]//SQUARE_SIZE, pos[1]//SQUARE_SIZE)
    return pos

def convert_to_game_syntax(pos):
    col_num = pos[0]
    col_letter = chr(col_num + 97)

    row_num = str(pos[1]+1)
    return col_letter + row_num


# Game Loop
running = True
start_letters = ""
end = ""
draw_board()

def draw_pieces(dict):
    for piece_id in dict:
        piece = Janggi.get_piece_from_id(piece_id)
        piece.draw(window)

def show_text(text,color):
    message = FONT.render(text, True, color)
    window.blit(message,(35,35))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if Janggi.get_game_state() == "UNFINISHED":
                pos = get_mouse_position()
                if start_letters == "":
                    start_letters = convert_to_game_syntax(pos)
                    start_numbers = [pos[1],pos[0]]
                    piece_id = Janggi.whats_here(start_numbers)
                    if Janggi.piece_belongs_to_turntaker(start_numbers):
                        piece = Janggi.get_piece_from_id(piece_id)
                        moves = piece.get_move_list()
                        for move in moves:
                            x = piece.calc_pixel_position(move[1])
                            y = piece.calc_pixel_position(move[0])
                            highlight = highlight.convert_alpha()
                            highlight.set_alpha(100)
                            window.blit(highlight,(x,y))
                    else:
                        start_letters = end = ""
                else:
                    end = convert_to_game_syntax(pos)
                    Janggi.make_move(start_letters,end)
                    draw_board()
                    start_letters = end = ""
            else:
                if Janggi.get_game_state() == "RED_WINS":
                    show_text("Red Wins!",RED)
                else:
                    show_text("Blue Wins!",BLUE)

    draw_pieces(Janggi.get_piece_dictionary("Red"))
    draw_pieces(Janggi.get_piece_dictionary("Blue"))
    pygame.display.update()