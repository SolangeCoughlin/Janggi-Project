import pygame
from constants import *
from JanggiGame import *
from Button import *
from enum import Enum

"""
This tutorial referenced in creating this game project: https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
"""

def draw_board(window):
    """
    Draws the board onto the screen while the game is running
    """
    window.fill(YELLOW)
    window.blit(board, (35, 35))

def draw_title(window):
    """
    Draws the game title onto the title screen
    """
    title_surface, _ = TITLE_FONT.render("Janggi", BLACK, YELLOW)
    title_rect = title_surface.get_rect(center=(300,250))
    window.blit(title_surface, title_rect)

def get_mouse_position():
    """
    Returns the position of the mouse, converted into which square it is occupying
    """
    pos = pygame.mouse.get_pos()
    pos = (pos[0]//SQUARE_SIZE, pos[1]//SQUARE_SIZE)
    return pos

def convert_to_game_syntax(pos):
    """
    Receives a tuple containing the square the mouse is currently in, and converts it to the syntax expected by the game
    """
    col_num = pos[0]
    col_letter = chr(col_num + 97)

    row_num = str(pos[1]+1)
    return col_letter + row_num

def draw_pieces(window,game,dict):
    """
    Draws the pieces onto the board while the game is running
    """
    for piece_id in dict:
        piece = game.get_piece_from_id(piece_id)
        piece.draw(window)

def show_text(window,text,color):
    """
    Receives a surface to draw on, text to display, and the color for the text. Writes text based on these parameters
    to the given screen
    """
    font = pygame.freetype.SysFont("Courier", 30)
    text_surface, _ = font.render(text, color)
    text_rect = text_surface.get_rect(center = (WIDTH//2,HEIGHT//2-50))
    window.blit(text_surface, text_rect)

class GameState(Enum):
    """
    Records the available game states
    """
    QUIT = -1
    TITLE = 0
    PLAYING = 1
    GAME_OVER = 2

def main():
    """
    Main function running the main game loop
    """
    pygame.init()

    # Create the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Update the caption and icon of the game window
    pygame.display.set_caption("Janggi")
    icon = pygame.image.load('assets/chess.png')

    pygame.display.set_icon(icon)
    game_state = GameState.TITLE

    # Game loop
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(window)
        if game_state == GameState.PLAYING:
            game_state = play_game(window)
        if game_state == GameState.GAME_OVER:
            game_state = end_game(window)
        if game_state == GameState.QUIT:
            pygame.quit()
            return

def title_screen(window):
    """
    Called when the game state is being on the Title screen. Returns a new game state depending on what buttons are
    clicked by the user
    """

    # Create start and quit buttons to show on the title screen
    start_button = Button(
        (300,400),
        "Start",
        25,
        BLACK,
        YELLOW,
        GameState.PLAYING
    )
    quit_button = Button(
        (300,450),
        "Quit",
        25,
        BLACK,
        YELLOW,
        GameState.QUIT
    )

    # Create a collection of the buttons to loop through
    buttons = [start_button, quit_button]

    # Running loop
    while True:

        # Detect if the mouse has been clicked and record as a boolean to control button actions
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Fill the screen and draw the game title
        window.fill(YELLOW)
        draw_title(window)

        # Loop through the buttons on the title screen and check for hovering or actions from clicks
        for button in buttons:
            button_action = button.update_button(pygame.mouse.get_pos(), mouse_up)
            if button_action is not None:
                # If there has been a click, return the action associated with the button
                return button_action
            # Draw the button on screen
            button.draw_button(window)

        pygame.display.update()

def play_game(window):
    """
    Called when the game state is playing.
    """

    Janggi = JanggiGame()
    start_letters = ""
    end = ""
    draw_board(window)

    while True:

        for event in pygame.event.get():

            # If the user clicks the X on the game window, exit the game and stop the game loop
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT

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
                                new_highlight = highlight.convert_alpha()
                                new_highlight.set_alpha(100)
                                window.blit(new_highlight,(x+3,y+3))
                        else:
                            start_letters = end = ""

                    # If start letters are not empty, than this click is for the end position. Get the end position
                    else:
                        end = convert_to_game_syntax(pos)
                        Janggi.make_move(start_letters,end)
                        draw_board(window)
                        start_letters = end = ""

        # Draw pieces on the board and update the display
        draw_pieces(window, Janggi, Janggi.get_piece_dictionary("Red"))
        draw_pieces(window, Janggi, Janggi.get_piece_dictionary("Blue"))

        # Action if the game is finished. Run the end game screen
        if Janggi.get_game_state() != "UNFINISHED":
            return end_game(Janggi, window)

        pygame.display.update()

def end_game(game,window):
    """
    Called when game state is game_over, or a player has been checkmated
    """

    # Make surfaces and rects for the box containing the game result, and will be a backdrop for the end game buttons
    end_box = pygame.Surface((250,250))
    end_box_border = pygame.Surface((252,252))
    end_box_rect = end_box.get_rect(center=(WIDTH//2,HEIGHT//2))
    end_box_border_rect = end_box_border.get_rect(center=(WIDTH//2,HEIGHT//2))

    # Make back and quit buttons and put in a collection
    back_button = Button(
        (WIDTH//2, HEIGHT//2 + 25),
        "Back to Menu",
        20,
        BLACK,
        WHITE,
        GameState.TITLE
    )
    quit_button = Button(
        (WIDTH//2, HEIGHT//2+75),
        "Quit",
        20,
        BLACK,
        WHITE,
        GameState.QUIT
    )

    buttons = [back_button, quit_button]

    # Running loop
    while True:
        # Detect mouse clicks to perform actions based on the buttons clicked
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Fill the end_box components and blit to the screen
        end_box.fill(WHITE)
        end_box_border.fill(BLACK)
        window.blit(end_box_border, end_box_border_rect)
        window.blit(end_box, end_box_rect)

        # Based on the game state, print text to the window showing the winner
        if game.get_game_state() == "RED_WON":
            show_text(window, "Red Wins!", RED)
        else:
            show_text(window, "Blue Wins!", BLUE)

        # Loop through the buttons and detect actions requested by the user (go back to main screen or quit)
        for button in buttons:
            button_action = button.update_button(pygame.mouse.get_pos(), mouse_up)
            if button_action is not None:
                return button_action
            # Drawing onto the window instead of the end box gets the buttons to actually work
            button.draw_button(window)

        pygame.display.update()


if __name__ == "__main__":
    main()
