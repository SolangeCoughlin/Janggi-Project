# Author: Solange Coughlin
# Date: 3/3/2021
# Description: This file contains a class that allows two players to play Janggi, a strategy board game similar to western Chess

import copy, pygame
from Piece import *

# Initializing pygame module
pygame.init()


class JanggiGame():
    """Represents the game of Janggi, and contains as a data member who the players are and the board for the game. This
    class communicates with the classes, General, Guard, Chariot, Horse, Elephant, and Cannon to create the various piece objects
    and orient them on the board. The game is responsible for knowing whose turn it is, checking if a valid move leads to a piece
    capture and removing the captured piece, moving pieces around the board and updating a piece location both on the board and
    in the piece's internal data member, checking for checkmate, and updating the status of the game if it changes."""

    def __init__(self):
        """Initialize the game by creating the board, creating the Piece objects, and 'placing' them on the board by placing markers on the board
        and creating a dictionary containing all pieces and their current positions. Initializes the game to start on blue's turn"""

        # The board is a list containing 10 lists. Each of the 10 lists represents a row of the game board. Each row contains 9 "empty" (three spaces) strings
        # representing the columns of the game board.
        self._board = [["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 0
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 1
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 2
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 3
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 4
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 5
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 6
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 7
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"],  # Row 8
                       ["___", "___", "___", "___", "___", "___", "___", "___", "___"]]  # Row 9

        self._current_turn = "Blue"
        self._game_state = "UNFINISHED"

        self._Blue_Piece_List = ["b$1","b$2","b^1","b^2","b~1","b~2","b%1","b%2","b#1","b#2","b-1","b-2","b-3","b-4","b-5","b@"] # Original order
        self._Red_Piece_List = ["r$1","r$2","r^1","r^2","r~1","r~2","r%1","r%2","r#1","r#2","r-1","r-2","r-3","r-4","r-5","r@"] # Original order
        self._blue_start_pos = [[9,3], [9,5], [9,2], [9,7], [9,1], [9,6], [9,0], [9,8],[7,1],[7,7],[6,0],[6,2],[6,4],[6,6],[6,8],[8,4]] # Original order
        self._red_start_pos = [[0, 3], [0, 5], [0, 2], [0, 7], [0, 1], [0, 6], [0, 0], [0, 8], [2, 1], [2, 7], [3, 0], [3, 2], [3, 4], [3, 6], [3, 8],[1, 4]] # Original order

        self._blue_palace_spaces = [[7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5]]
        self._red_palace_spaces = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
        self._Blue_Pieces = {}
        self._Red_Pieces = {}
        self._checking_pieces = {}

        for index in range(len(self._Blue_Piece_List)):
            piece_id = self._Blue_Piece_List[index]
            start_position = self._blue_start_pos[index]

            # The symbol @ represents the General piece
            if piece_id[1] == "@":
                general = General("Blue")
                self._Blue_Pieces[piece_id] = general
                self.put_piece_on_board(piece_id, general, start_position)

            # The symbol - represents a Soldier piece
            elif piece_id[1] == "-":
                soldier = Soldier("Blue")
                self._Blue_Pieces[piece_id] = soldier
                self.put_piece_on_board(piece_id, soldier, start_position)

            # The symbol $ represents a Guard piece.
            elif piece_id[1] == "$":
                guard = Guard("Blue")
                self._Blue_Pieces[piece_id] = guard
                self.put_piece_on_board(piece_id, guard, start_position)

            # The symbol % represents a chariot piece
            elif piece_id[1] == "%":
                chariot = Chariot("Blue")
                self._Blue_Pieces[piece_id] = chariot
                self.put_piece_on_board(piece_id, chariot, start_position)

            # The symbol ^ represents a horse piece
            elif piece_id[1] == "^":
                horse = Horse("Blue")
                self._Blue_Pieces[piece_id] = horse
                self.put_piece_on_board(piece_id, horse, start_position)

            # The symbol ~ represents an elephant piece
            elif piece_id[1] == '~':
                elephant = Elephant("Blue")
                self._Blue_Pieces[piece_id] = elephant
                self.put_piece_on_board(piece_id, elephant, start_position)

            else:  # The last piece, represented by #, is the cannon.
                cannon = Cannon("Blue")
                self._Blue_Pieces[piece_id] = cannon
                self.put_piece_on_board(piece_id, cannon, start_position)

        for index in range(len(self._Red_Piece_List)):
            piece_id = self._Red_Piece_List[index]
            start_position = self._red_start_pos[index]
            if piece_id[1] == "@":
                general = General("Red")
                self._Red_Pieces[piece_id] = general
                self.put_piece_on_board(piece_id, general, start_position)
            elif piece_id[1] == "-":
                soldier = Soldier("Red")
                self._Red_Pieces[piece_id] = soldier
                self.put_piece_on_board(piece_id, soldier, start_position)
            elif piece_id[1] == "$":
                guard = Guard("Red")
                self._Red_Pieces[piece_id] = guard
                self.put_piece_on_board(piece_id, guard, start_position)

            elif piece_id[1] == "%":
                chariot = Chariot("Red")
                self._Red_Pieces[piece_id] = chariot
                self.put_piece_on_board(piece_id, chariot, start_position)

            elif piece_id[1] == "^":
                horse = Horse("Red")
                self._Red_Pieces[piece_id] = horse
                self.put_piece_on_board(piece_id, horse, start_position)

            elif piece_id[1] == '~':
                elephant = Elephant("Red")
                self._Red_Pieces[piece_id] = elephant
                self.put_piece_on_board(piece_id, elephant, start_position)

            else:  # The last piece, represented by #, is the cannon.
                cannon = Cannon("Red")
                self._Red_Pieces[piece_id] = cannon
                self.put_piece_on_board(piece_id, cannon, start_position)

        # Once all pieces are on the board, create their initial move lists
        self.update_all_move_lists()

    def put_piece_on_board(self, piece_id, piece_obj, start_pos):
        """Receives a piece ID, and piece object and a start position, and places the piece on the board in the given position"""

        self._board[start_pos[0]][start_pos[1]] = piece_id
        piece_obj.set_location(start_pos)

    def update_all_move_lists(self):
        """Updates the move lists for all pieces"""

        for piece_id in self._Red_Pieces:
            piece = self.get_piece_from_id(piece_id)
            piece.check_for_moves(self)
            move_list = piece.get_move_list()

        for piece_id in self._Blue_Pieces:
            piece = self.get_piece_from_id(piece_id)
            piece.check_for_moves(self)
            move_list = piece.get_move_list()

    def piece_belongs_to_turntaker(self,pos):
        """Returns true if the piece in the given position belongs to the player whose turn it is. Returns False otherwise."""

        piece_id = self.whats_here(pos)
        if piece_id == "___" or piece_id[0] != self._current_turn[0].lower():
            return False
        else:
            return True

    def make_move(self, start_pos, end_pos):
        """Receives a start position and end position, and checks if the move is valid. If it is, it executes the move
        and updates the board and pieces and game turn. If the move is not valid, it returns False. At the end of
        executing a valid move, this method checks if the game has ended and updates the game status accordingly."""

        # Start the make_move process by parsing the input positions into board indexing format
        start = self.parse_position(start_pos)
        end = self.parse_position(end_pos)
        if self._current_turn == "Blue" or self._current_turn == "blue":
            opponent = "Red"
        else:
            opponent = "Blue"

        # Is the game still ongoing?
        if self._game_state != "UNFINISHED":
            return False

        if not self.piece_belongs_to_turntaker(start):
            return False

        # Get the contents of the start position on the board
        piece_id = self.whats_here(start)

        # Once it's established the piece belongs to the current player, check if the player is passing their turn. If they are, update the turn and end
        if start == end:
            self.update_turn()
            return True

        # Once it's established the piece belongs to the current player, check if the end position is in range for the piece
        piece = self.get_piece_from_id(piece_id)
        available_moves = piece.check_for_moves(self)
        if end not in available_moves:
            return False

        # At this point, move is almost valid! Check if the move would put the player's general in check...

        # Test the move to see if it puts the player's general in check. If is evaluates True, it puts the general in check, so return False, as it is not valid.
        # If it returns False, the move has not put the general in check, and test_move_for_check has already executed to move.
        if self.move_causes_check(start, end, piece):
            return False
        else:
            self.execute_move(start, end, piece)

        # Check if the opponent is in checkmate after the move. If the opponent is in check and checkmate_check returns True, then player is in checkmate.

        if self.is_in_check(opponent) and self.checkmate_check(opponent):
            if opponent == "Red" or opponent == "red":
                self._game_state = "BLUE_WON"
            else:
                self._game_state = "RED_WON"

        else:
            # Update the current turn and return True for a successful move
            piece.check_for_moves(self)
            self.update_all_move_lists()
            self.update_turn()

        self.record_move(start_pos, end_pos)
        return True

    def record_move(self, start_pos, end_pos):
        with open('move_list.txt','a') as outfile:
            outfile.write(start_pos + '->' + end_pos + '\n')

    def execute_move(self, start, end, piece):
        """Updates board and piece positions for valid moves"""

        if self.whats_here(end) != "___":
            captured_piece_id = self.whats_here(end)
            self.remove_piece(captured_piece_id)

        # Move the piece to the end position
        self._board[end[0]][end[1]] = self.whats_here(start)

        # Set the start position to empty
        self._board[start[0]][start[1]] = "___"

        # Set the location of the piece
        piece.set_location(end)

    def move_causes_check(self, start, end, piece):
        """Receives a list with a row and column describing a position for start and end position. Also receives a
         piece object for the piece whose move is being tested. The method tests the move to determine if the move puts
         the general in check. If it does, returns True, else returns False."""

        captured_piece_id = ""
        move_causes_check = False

        if self.whats_here(end) != "___":
            captured_piece_id = self.whats_here(end)

        # Move the piece to the end position
        self._board[end[0]][end[1]] = self.whats_here(start)

        # Set the start position to empty
        self._board[start[0]][start[1]] = "___"

        # Set the location of the piece
        piece.set_location(end)

        if piece.get_team() == "Blue":
            player = "Blue"
        else:
            player = "Red"

        if self.is_in_check(player):
            # If this is true, the move is not valid and should not be allowed. Undo the changes above and return True
            move_causes_check = True

        self._board[start[0]][start[1]] = self._board[end[0]][
            end[1]]  # Set the original start to match whats now at the end
        piece.set_location(start)  # Change the location back to the start

        # If a piece was captured, restore it to the board
        if captured_piece_id != "":
            self._board[end[0]][end[1]] = captured_piece_id  # the location for this piece was never changed
        else:
            self._board[end[0]][end[1]] = "___"

        return move_causes_check

    def update_turn(self):
        """Updates the turn to be the next player."""

        if self._current_turn == "Blue":
            self._current_turn = "Red"
        else:
            self._current_turn = "Blue"

    def is_in_check(self, player):
        """Receives a player (red or blue) and returns True if the player is in check and False if they are not in check."""

        player_in_check = False
        self._checking_pieces = {}

        if player == "Blue" or player == "blue":
            general = self.get_piece_from_id("b@")
        else:
            general = self.get_piece_from_id("r@")

        general_location = general.get_location()

        if player == "Blue" or player == "blue":
            opponent_dict = self._Red_Pieces
        else:
            opponent_dict = self._Blue_Pieces

        for piece in opponent_dict:
            this_piece = self.get_piece_from_id(piece)
            this_piece.check_for_moves(self)
            if general_location in this_piece.get_move_list():
                player_in_check = True
                self._checking_pieces[piece] = this_piece

        return player_in_check

    def checkmate_check(self, player):
        """This method is called as part of determining of the player is in checkmate. It tests if the general can't move,
        and whether the piece putting the general in checkmate can be blocked or captured. If the general can move or the
        checking piece can be blocked or captured, the method returns False. Otherwise, it returns True."""

        checkmate = False
        general_can_move = False
        checking_piece_can_be_captured = False
        checking_piece_can_be_blocked = False

        if player == "Blue" or player == 'blue':
            general = self.get_piece_from_id('b@')
            player_dict = self.get_piece_dictionary("Blue")
        else:
            general = self.get_piece_from_id('r@')
            player_dict = self.get_piece_dictionary("Red")

        # Check if the general has any valid moves. If the general does, test them to ensure they aren't protected by another piece.
        general.check_for_moves(self)
        general_moves = general.get_move_list()
        if general_moves:
            for move in general_moves:
                if not self.move_causes_check(general.get_location(), move, general):
                    general_can_move = True

        # Check if any pieces can capture the piece putting the general in check
        for checking_piece_id in self._checking_pieces:
            checking_piece = self.get_piece_from_id(checking_piece_id)
            checking_piece_location = checking_piece.get_location()

            for player_piece_id in player_dict:
                player_piece = self.get_piece_from_id(player_piece_id)
                player_piece_location = player_piece.get_location()
                player_piece_moves = player_piece.get_move_list()

                if checking_piece_location in player_piece_moves:

                    if not self.move_causes_check(player_piece_location, checking_piece_location, player_piece):
                        checking_piece_can_be_captured = True

            # Check if any pieces can block the piece causing the check WITHOUT putting their general in check
            # Checking piece is a CANNON
            # Check if a piece can move into the row/column of the cannon
            # Check if a piece can move out of the row/column of the cannon
            # Test the move to see if it can be made without endangering the general
            if checking_piece_id[1] == '#':

                # Determine if the piece and general share a row or a column
                if checking_piece_location[0] == general.get_location()[0]:

                    # Determine the "higher" and "lower" columns for comparison purposes
                    checking_piece_col = checking_piece_location[1]
                    general_col = general.get_location()[1]
                    max_col = max(checking_piece_col, general_col)
                    min_col = min(checking_piece_col, general_col)
                    spaces_between_pieces = []
                    space_count = min_col

                    while space_count < max_col:
                        space_count += 1
                        if self._board[checking_piece_location[0]][space_count] == "___":
                            spaces_between_pieces.append([checking_piece_location[0], space_count])
                else:
                    # If the general and the chariot are in the same column
                    checking_piece_row = checking_piece_location[0]
                    general_row = general.get_location()[0]
                    max_row = max(checking_piece_row, general_row)
                    min_row = min(checking_piece_row, general_row)
                    spaces_between_pieces = []
                    space_count = min_row

                    while space_count < max_row:
                        space_count += 1
                        if self._board[space_count][checking_piece_location[1]] == "___":
                            spaces_between_pieces.append([space_count, checking_piece_location[1]])

                for piece_id in player_dict:
                    piece = self.get_piece_from_id(piece_id)
                    player_piece_moves = piece.get_move_list()

                    # Scenario 2: If there is a piece between the checking piece and the general, try and move it
                    if piece.get_location() in spaces_between_pieces:
                        for move in player_piece_moves:
                            if not self.move_causes_check(piece.get_location(), move, piece):
                                checking_piece_can_be_blocked = True

                    for move in player_piece_moves:

                        # Scenario 1: If there is a move in the same row as the checking piece and between the general and the piece, see if you can move there
                        if move in spaces_between_pieces:
                            if not self.move_causes_check(piece.get_location(), move, piece):
                                checking_piece_can_be_blocked = True

            # Checking piece is a ELEPHANT
            if checking_piece_id[1] == '~':
                # Figure out what direction the piece needs to be blocked in
                # Check if a piece can move into that space
                # Test the move to see if it can be made without endangering the general

                if (checking_piece_location[0] == (general.get_location()[0]) - 3):
                    # Check in the space north of the elephant
                    blocking_space = [checking_piece_location[0] - 1, checking_piece_location[1]]

                elif (checking_piece_location[1] == (general.get_location()[1]) + 3):
                    # look west
                    blocking_space = [checking_piece_location[0], checking_piece_location[1] - 1]

                else:
                    blocking_space = [checking_piece_location[0], checking_piece_location[1] - 1]

                for piece_id in player_dict:
                    piece = self.get_piece_from_id(piece_id)
                    player_piece_moves = piece.get_move_list()
                    if blocking_space in player_piece_moves:
                        if not self.move_causes_check(piece.get_location(), blocking_space, piece):
                            checking_piece_can_be_blocked = True

            # If the checking piece is a HORSE
            if checking_piece_id[1] == '^':
                # Figure out what direction the piece needs to be blocked in
                # Check if a piece can move into that space
                # Test the move to see if it can be made without endangering the general

                if (checking_piece_location[0] == (general.get_location()[0]) - 2):
                    # Check in the space north of the elephant
                    blocking_space = [checking_piece_location[0] - 1, checking_piece_location[1]]

                elif (checking_piece_location[1] == (general.get_location()[1]) + 2):
                    # look west
                    blocking_space = [checking_piece_location[0], checking_piece_location[1] - 1]

                else:
                    blocking_space = [checking_piece_location[0], checking_piece_location[1] - 1]

                for piece_id in player_dict:
                    piece = self.get_piece_from_id(piece_id)
                    player_piece_moves = piece.get_move_list()
                    if blocking_space in player_piece_moves:
                        if not self.move_causes_check(piece.get_location(), blocking_space, piece):
                            checking_piece_can_be_blocked = True

            # Checking piece is a CHARIOT
            if checking_piece_id[1] == '%':
                if checking_piece_location[0] == general.get_location()[0]:

                    # Determine the "higher" and "lower" columns for comparison purposes
                    checking_piece_col = checking_piece_location[1]
                    general_col = general.get_location()[1]
                    max_col = max(checking_piece_col, general_col)
                    min_col = min(checking_piece_col, general_col)
                    spaces_between_pieces = []
                    space_count = min_col

                    while space_count < max_col:
                        space_count += 1
                        if self._board[checking_piece_location[0]][space_count] == "___":
                            spaces_between_pieces.append([checking_piece_location[0], space_count])
                else:
                    # If the general and the chariot are in the same column
                    checking_piece_row = checking_piece_location[0]
                    general_row = general.get_location()[0]
                    max_row = max(checking_piece_row, general_row)
                    min_row = min(checking_piece_row, general_row)
                    spaces_between_pieces = []
                    space_count = min_row

                    while space_count < max_row:
                        space_count += 1
                        if self._board[space_count][checking_piece_location[1]] == "___":
                            spaces_between_pieces.append([space_count,checking_piece_location[1]])

                for piece_id in player_dict:
                    piece = self.get_piece_from_id(piece_id)
                    player_piece_moves = piece.get_move_list()

                    for move in player_piece_moves:

                        # Scenario 1: If there is a move in the same row as the checking piece and between the general and the piece, see if you can move there
                        if move in spaces_between_pieces:
                            if not self.move_causes_check(piece.get_location(), move, piece):
                                checking_piece_can_be_blocked = True

        # If all the things are True, than checkmate is True
        if (not general_can_move) and (not checking_piece_can_be_captured) and (not checking_piece_can_be_blocked):
            checkmate = True

        return checkmate

    def get_piece_dictionary(self, player):
        """Returns the piece dictionary for the player passed to the method"""

        if player == "Blue" or player == "blue":
            return self._Blue_Pieces
        else:
            return self._Red_Pieces

    def get_game_state(self):
        """Returns the state of the game, either 'UNFINISHED' if still underway, or 'RED_WON' or 'BLUE_WON' if either player has won"""

        return self._game_state

    def get_current_turn(self):
        """Returns whose turn it currently is"""

        return self._current_turn

    def print_board(self):
        """Prints out the board"""

        for row in self._board:
            print(row)

    def parse_position(self, pos):
        """Receives a string representing a board position and breaks it into to integer values in a list. The first value is converted to a number from the letter
        at the start of the position, and the second value is the number portion of the string converted to an integer. This method returns a list containing the row
        and column of the position in a format compatible with the board. The first value represents the row, and the second value represents the column"""

        # The first letter in the string represents the column. Convert this to a number using ord() to get the Unicode representation and subtract 97 (a = 97 in Unicode,
        # so column a would result in column 0)
        letter_col = pos[0]
        col = int(ord(letter_col) - 97)

        # Python row 0 is row 1 from the user's perspective, so subtract the given number from 10 to yield the row for indexing the board
        row = int(pos[1:]) - 1

        return [row, col]

    def get_piece_from_id(self, piece_id):
        """Receives a string representing the piece on the board, and returns the object for that piece"""

        if piece_id[0] == "b":
            return self._Blue_Pieces[piece_id]
        else:
            return self._Red_Pieces[piece_id]

    def remove_piece(self, piece_id):
        """Receives a piece_id, and removes the piece from the dictionary of pieces in the game"""

        if self._current_turn == "Blue":
            del self._Red_Pieces[piece_id]
        else:
            del self._Blue_Pieces[piece_id]

    def whats_here(self, location):
        """Receives a list containing a row and a column (representing a board space) and returns the contents of the space on the board.
        The method is called by pieces in the game to allow them to tell if they can move"""

        return self._board[location[0]][location[1]]

def main():
    pass


if __name__ == '__main__':
    main()
