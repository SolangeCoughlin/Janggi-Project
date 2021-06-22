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
    window.blit(board, (35, 35))

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
    window.blit(message, (35, 35))

while running:

    for event in pygame.event.get():

        # If the user clicks the X on the game window, exit the game and stop the game loop
        if event.type == pygame.QUIT:
            running = False

        # If the user pressed and released the mouse button, start checking the click
        if event.type == pygame.MOUSEBUTTONUP:

            # Action if the game is not finished
            if Janggi.get_game_state() == "UNFINISHED":

                # Get the position of the mouse
                pos = get_mouse_position()

                # If the start letters are blank, the piece clicked is in its start position. Get the position
                if start_letters == "":

                    # Pass the mouse position to this function to get the start position in a form that Janggi can use
                    start_letters = convert_to_game_syntax(pos)

                    # Change the start_letters into numbers that can be passed to the game
                    start_numbers = [pos[1],pos[0]]

                    # Get the id of the piece selected
                    piece_id = Janggi.whats_here(start_numbers)

                    # If the piece belongs to the player whose turn it is, continue
                    if Janggi.piece_belongs_to_turntaker(start_numbers):

                        # Get the piece object, and then get the list of moves the piece can make
                        piece = Janggi.get_piece_from_id(piece_id)
                        moves = piece.get_move_list()

                        # For each move, highlight it on the board
                        for move in moves:
                            x = piece.calc_pixel_position(move[1])
                            y = piece.calc_pixel_position(move[0])
                            highlight = highlight.convert_alpha()
                            highlight.set_alpha(100)
                            window.blit(highlight,(x+3,y+3))
                    else:
                        start_letters = end = ""

                # If start letters are not empty, than this click is for the end position. Get the end position
                else:
                    end = convert_to_game_syntax(pos)
                    Janggi.make_move(start_letters,end)
                    draw_board()
                    start_letters = end = ""

            # Action if the game is finished. Display the winner (note: this needs to be updated - right now this only shows
            # that the same has ended when the user clicks after a move that puts a player in checkmate was made on the previous turn)
            else:
                if Janggi.get_game_state() == "RED_WINS":
                    show_text("Red Wins!",RED)
                else:
                    show_text("Blue Wins!",BLUE)

    # Draw pieces on the board and update the display
    draw_pieces(Janggi.get_piece_dictionary("Red"))
    draw_pieces(Janggi.get_piece_dictionary("Blue"))
    pygame.display.update()
