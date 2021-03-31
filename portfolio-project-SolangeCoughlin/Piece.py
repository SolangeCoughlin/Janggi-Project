import pygame
from constants import *

class Piece():
    """A class that defines the general information about a piece, such as whose team it is on and where it is.
    Other piece classes will inherit from this and define piece specific details"""

    def __init__(self, player):
        """Initializes the piece with two data members: its location (initially empty) and its team."""
        self._location = []
        self._team = player
        self._move_list = []
        self._icon = ""

        self._blue_palace_spaces = [[7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5]]
        self._blue_palace_diags = [[7, 5], [8, 4], [9, 3], [7, 3], [8, 4], [9, 5]]
        self._red_palace_spaces = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
        self._red_palace_diags = [[2, 3], [1, 4], [0, 5], [0, 3], [1, 4], [2, 5]]

    def calc_pixel_position(self,index):
        """Receives an integer representing either the row or column index whose pixel center postion needs to be determined.
        Returns the pixel position where an icon must be drawing for it to appear centered in the square. Subtracts 20 from
        the square center, which is half the size of the current icon size, to yield the correct biased location."""

        return (SQUARE_SIZE * index + (SQUARE_SIZE // 2)) - half_icon

    def draw(self,window):
        pos = self.get_location()
        row = pos[0]
        col = pos[1]

        window.blit(self._icon,(self.calc_pixel_position(col),self.calc_pixel_position(row)))

    def get_location(self):
        """Returns the current location of the piece"""
        return self._location

    def set_location(self, new_pos):
        """Sets a new location for the piece as a list [row, col]"""
        self._location = new_pos

    def get_team(self):
        """Returns the team the piece is on"""
        return self._team

    def get_move_list(self):
        """Returns the move list for the piece"""
        return self._move_list

    def off_the_board(self, pos):
        """Returns True if the given position is off the board, and False otherwise"""

        result = False
        if (pos[0] < 0 or pos[0] > 9) or (pos[1] < 0 or pos[1] > 8):
            result = True

        return result


class General(Piece):
    """Represents the General piece. Communicates with the Piece class to inherit from it, and is created by the
    JanggiGame class. JanggiGame defines if a piece is considered a general or a guard by assigning it an ID and a
    start position. Decisions on checking a General piece will be made based on the piece ID, not its class.
    The JanggiGame class will also update the piece's location on the board. The piece knows what all its valid moves are from its current position."""

    def __init__(self, player):
        """Initializes the piece and sets it to belong to a certain player. Initializes the list of viable moves for the piece"""
        super().__init__(player)

        # This data member is a list containing tuples that represent coordinate pairs. These pairs describe how this piece can move on the board, relative to its current position.
        # The General piece can move one space in any direction in the palace.
        self._diag_movement = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self._normal_movement = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        if player == "Blue":
            self._opponent = "Red"
            self._icon = blue_gen
        else:
            self._opponent = "Blue"
            self._icon = red_gen

    def check_for_moves(self, game):
        """Receives the game object that is playing with this piece as a parameter, to allow it to check for valid moves.
        Based on its current location, the piece will check all available positions it could move to to see if they're valid.
        If it is, it adds it to the valid_moves list"""

        self._move_list = []

        current_pos = self.get_location()

        if self.get_team() == "Blue":
            if current_pos in self._blue_palace_diags:
                self._movement = self._diag_movement
            else:
                self._movement = self._normal_movement
        else:
            if current_pos in self._red_palace_diags:
                self._movement = self._diag_movement
            else:
                self._movement = self._normal_movement

        for move in self._movement:

            new_pos = [int(current_pos[0]) + move[0], int(current_pos[1]) + move[1]]

            # Blue general logic
            if self.get_team() == "Blue" and new_pos in self._blue_palace_spaces:
                if (game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[0].lower()) and self.space_is_safe(game,new_pos):
                    self._move_list.append(new_pos)

            # Red general logic
            if self.get_team() == "Red" and new_pos in self._red_palace_spaces:
                if (game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[0].lower()) and self.space_is_safe(game,new_pos):
                    self._move_list.append(new_pos)


        return self._move_list

    def space_is_safe(self, game, new_pos):
        """Receives an object of the game and a new position ( a list containing a row and column).
        Returns true if the new_pos is safe for the general to move into, and False if it is not."""

        if self.get_team() == "Blue":
            opponent_dict = game.get_piece_dictionary("Red")
        else:
            opponent_dict = game.get_piece_dictionary("Blue")

        space_is_safe = True

        for piece_id in opponent_dict:
            piece = game.get_piece_from_id(piece_id)
            move_list = piece.get_move_list()
            if new_pos in move_list:
                space_is_safe = False

        return space_is_safe


class Guard(Piece):
    """Represents the Guard piece. Communicates with the Piece class to inherit from it, and is created by the JanggiGame class.
    Decisions on checking a General piece will be made based on the piece ID, not its class. The JanggiGame class will also update the piece's location on the board. The piece knows what all its valid moves are from its current position."""

    def __init__(self, player):
        """Initializes the piece and sets it to belong to a certain player. Initializes the list of viable moves for the piece"""
        super().__init__(player)

        # This data member is a list containing tuples that represent coordinate pairs. These pairs describe how this piece can move on the board, relative to its current position.
        # The guard piece can move one space in any direction in the palace.
        self._diag_movement = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self._normal_movement = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        if player == "Blue":
            self._opponent = "Red"
            self._icon = blue_adv
        else:
            self._opponent = "Blue"
            self._icon = red_adv

    def check_for_moves(self, game):
        """Receives the game object that is playing with this piece as a parameter, to allow it to check for valid moves.
                Based on its current location, the piece will check all available positions it could move to to see if they're valid.
                If it is, it adds it to the valid_moves list"""

        self._move_list = []

        current_pos = self.get_location()

        if self.get_team() == "Blue":
            if current_pos in self._blue_palace_diags:
                self._movement = self._diag_movement
            else:
                self._movement = self._normal_movement
        else:
            if current_pos in self._red_palace_diags:
                self._movement = self._diag_movement
            else:
                self._movement = self._normal_movement

        for move in self._movement:

            new_pos = [int(current_pos[0]) + move[0], int(current_pos[1]) + move[1]]

            # Blue general logic
            if self.get_team() == "Blue" and new_pos in self._blue_palace_spaces:
                if (game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[0].lower()):
                    self._move_list.append(new_pos)

            # Red general logic
            if self.get_team() == "Red" and new_pos in self._red_palace_spaces:
                if (game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[0].lower()):
                    self._move_list.append(new_pos)

        return self._move_list


class Soldier(Piece):
    """Represents the Soldier pieces. Communicates with the Piece class to inherit from it, and is created by the JanggiGame class.
    The JanggiGame class will also update the piece's location on the board. The piece knows what all its valid moves are from its current
    position."""

    def __init__(self, player):
        """Initializes the piece and sets it to belong to a certain player. Initializes the list of viable moves for the piece"""
        super().__init__(player)

        # This data member is a list containing tuples that represent coordinate pairs. These pairs describe how this piece can move on the board, relative to its current position.
        # The Solder piece can move one space forward or one piece to the left or right if it is not in the palace. Inside the palace, it can also move forward diagonally.
        # Depending on which team the piece is on, "forward" movement in the tuples below will be reversed
        self._movement = []
        if player == "Blue":
            self._regular_movement = [(-1, 0), (0, 1), (0, -1)]
            self._palace_movement = [(-1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1)]
            self._opponent = "Red"
            self._icon = blue_sol
        else:
            self._regular_movement = [(1, 0), (0, 1), (0, -1)]
            self._palace_movement = [(1, 0), (0, 1), (0, -1), (1, 1), (1, -1)]
            self._opponent = "Blue"
            self._icon = red_sol

    def check_for_moves(self, game):
        """Receives the game object that is playing with this piece as a parameter, to allow it to check for valid moves.
                Based on its current location, the piece will check all available positions it could move to to see if they're valid.
                If it is, it adds it to the valid_moves list"""
        # Need to move diagonally in the palace but not if you're on the edge and you're trying to move away from it.

        self._move_list = []

        if self.get_location() in self._blue_palace_diags or self.get_location() in self._red_palace_diags:
            self._movement = self._palace_movement
        else:
            self._movement = self._regular_movement

        for move in self._movement:
            current_pos = self.get_location()
            new_pos = [int(current_pos[0]) + move[0], int(current_pos[1]) + move[1]]
            if not self.off_the_board(new_pos):
                if current_pos not in self._blue_palace_spaces and current_pos not in self._red_palace_spaces:
                    if game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[0].lower():
                        self._move_list.append(new_pos)
                else:
                    if new_pos[1] >= 3 or new_pos[1] <= 5:
                        if game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[
                            0].lower():
                            self._move_list.append(new_pos)

        return self._move_list


class Chariot(Piece):
    """Represents the Chariot pieces. Communicates with the Piece class to inherit from it, and is created by the JanggiGame class.
    The JanggiGame class will also update the piece's location on the board.The piece knows what all its valid moves are from its current
    position."""

    def __init__(self, player):
        super().__init__(player)

        if player == "Blue":
            self._opponent = "Red"
            self._icon = blue_char
        else:
            self._opponent = "Blue"
            self._icon = red_char

    def check_for_moves(self, game):
        """Receives the game object that is playing with this piece as a parameter, to allow it to check for valid moves.
                Based on its current location, the piece will check all available positions it could move to to see if they're valid.
                If it is, it adds it to the valid_moves list"""
        current_pos = self.get_location()

        self._move_list = []

        current_pos = self.get_location()
        row = current_pos[0]
        col = current_pos[1]

        # Check to the north
        next_pos = [row-1,col]
        saw_a_piece = False
        while (not self.off_the_board(next_pos)) and (saw_a_piece is False):
            if game.whats_here(next_pos) == "___":
                #add the space and keep going
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                saw_a_piece = True
                # add the space and keep going through another cycle
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                # add the space but don't count it and keep going
                self._move_list.append(next_pos)
            else: # count the piece and increment and stop next round
                saw_a_piece = True
            next_row = next_pos[0] - 1
            next_pos = [next_row, col]


        # Check to the south
        next_pos = [row + 1, col]
        saw_a_piece = False
        while (not self.off_the_board(next_pos)) and (saw_a_piece is False):
            if game.whats_here(next_pos) == "___":
                # add the space and keep going
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                saw_a_piece = True
                # add the space and keep going through another cycle
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                # add the space but don't count it and keep going
                self._move_list.append(next_pos)
            else:  # count the piece and increment and stop next round
                saw_a_piece = True
            next_row = next_pos[0] + 1
            next_pos = [next_row, col]

        # Check to the east
        next_pos = [row, col+1]
        saw_a_piece = False
        while (not self.off_the_board(next_pos)) and (saw_a_piece is False):
            if game.whats_here(next_pos) == "___":
                # add the space and keep going
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                saw_a_piece = True
                # add the space and keep going through another cycle
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                # add the space but don't count it and keep going
                self._move_list.append(next_pos)
            else:  # count the piece and increment and stop next round
                saw_a_piece = True
            next_col = next_pos[1] + 1
            next_pos = [row, next_col]

        # Check to the west
        next_pos = [row, col - 1]
        saw_a_piece = False
        while (not self.off_the_board(next_pos)) and (saw_a_piece is False):
            if game.whats_here(next_pos) == "___":
                # add the space and keep going
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                saw_a_piece = True
                # add the space and keep going through another cycle
                self._move_list.append(next_pos)
            elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                # add the space but don't count it and keep going
                self._move_list.append(next_pos)
            else:  # count the piece and increment and stop next round
                saw_a_piece = True
            next_col = next_pos[1] - 1
            next_pos = [row, next_col]

        if current_pos in self._blue_palace_diags or current_pos in self._red_palace_diags:

            # CHeck to the southeast
            next_pos = [row + 1, col + 1]
            saw_a_piece = False
            while (next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (saw_a_piece is False):
                if game.whats_here(next_pos) == "___":
                    # add the space and keep going
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    saw_a_piece = True
                    # add the space and keep going through another cycle
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    # add the space but don't count it and keep going
                    self._move_list.append(next_pos)
                else:  # count the piece and increment and stop next round
                    saw_a_piece = True
                next_row = next_pos[0] + 1
                next_col = next_pos[1] + 1
                next_pos = [next_row, next_col]

            #Check to the northeast
            next_pos = [row - 1, col + 1]
            saw_a_piece = False
            while (next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (
                    saw_a_piece is False):
                if game.whats_here(next_pos) == "___":
                    # add the space and keep going
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    saw_a_piece = True
                    # add the space and keep going through another cycle
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    # add the space but don't count it and keep going
                    self._move_list.append(next_pos)
                else:  # count the piece and increment and stop next round
                    saw_a_piece = True
                next_row = next_pos[0] - 1
                next_col = next_pos[1] + 1
                next_pos = [next_row, next_col]

            # Check to the northwest
            next_pos = [row - 1, col - 1]
            saw_a_piece = False
            while (next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (
                    saw_a_piece is False):
                if game.whats_here(next_pos) == "___":
                    # add the space and keep going
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    saw_a_piece = True
                    # add the space and keep going through another cycle
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    # add the space but don't count it and keep going
                    self._move_list.append(next_pos)
                else:  # count the piece and increment and stop next round
                    saw_a_piece = True
                next_row = next_pos[0] - 1
                next_col = next_pos[1] - 1
                next_pos = [next_row, next_col]

            # Check to the southeast
            next_pos = [row + 1, col - 1]
            saw_a_piece = False
            while (next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (
                    saw_a_piece is False):
                if game.whats_here(next_pos) == "___":
                    # add the space and keep going
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] != '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    saw_a_piece = True
                    # add the space and keep going through another cycle
                    self._move_list.append(next_pos)
                elif game.whats_here(next_pos)[1] == '@' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                    # add the space but don't count it and keep going
                    self._move_list.append(next_pos)
                else:  # count the piece and increment and stop next round
                    saw_a_piece = True
                next_row = next_pos[0] + 1
                next_col = next_pos[1] - 1
                next_pos = [next_row, next_col]

        return self._move_list

class Cannon(Piece):
    """Represents the Cannon pieces. Communicates with the Piece class to inherit from it, and communicates the JanggiGame to check the board for whether a move is valid.
    The JanggiGame class will update the piece's location if it is moved. The piece knows where it is, and what moves it is allowed to make, including if it is blocked from
    an otherwise valid move by another piece on the board."""

    def __init__(self, player):
        """Initializes the piece to belong to a certain team"""
        super().__init__(player)

        # _piece_count is used to detect if there is exactly one piece between the cannon and its target
        self._piece_count = 0

        if player == "Blue":
            self._opponent = "Red"
            self._icon = blue_can
        else:
            self._opponent = "Blue"
            self._icon = red_can

    def check_for_moves(self, game):
        """Receives the game object that is playing with this piece as a parameter, to allow it to check for valid moves.
        Based on its current location, the piece will check all available positions it could move to to see if they're valid.
        If it is, it adds it to the valid_moves list"""

        self._move_list = []


        current_pos = self.get_location()
        row = current_pos[0]
        col = current_pos[1]

        # Check to the north
        next_pos = [row - 1, col]
        piece_count = 0
        saw_a_cannon = False
        while piece_count < 2 and (saw_a_cannon is False) and (not self.off_the_board(next_pos)):
            if piece_count == 1:
                if game.whats_here(next_pos) == "___":
                    self._move_list.append(next_pos)
                else:
                    if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[0].lower():
                        self._move_list.append(next_pos)
                        piece_count += 1
                    if game.whats_here(next_pos)[1] == '#':
                        saw_a_cannon = True
                    if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                        piece_count += 1
                next_row = next_pos[0] - 1
                next_pos = [next_row, col]
            elif game.whats_here(next_pos)[1] == '#':
                saw_a_cannon = True
            elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                piece_count += 1
                next_row = next_pos[0] - 1
                next_pos = [next_row, col]
            else:
                if piece_count == 0:
                    next_row = next_pos[0] - 1
                    next_pos = [next_row, col]

        # Check to the south
        next_pos = [row + 1, col]
        piece_count = 0
        saw_a_cannon = False
        while ((not self.off_the_board(next_pos)) and (piece_count < 2) and (saw_a_cannon is False)):
            if piece_count == 1:
                if game.whats_here(next_pos) == "___":
                    self._move_list.append(next_pos)
                else:
                    if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                        0].lower():
                        self._move_list.append(next_pos)
                        piece_count += 1
                    if game.whats_here(next_pos)[1] == '#':
                        saw_a_cannon = True
                    if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                        piece_count += 1
                next_row = next_pos[0] + 1
                next_pos = [next_row, col]
            elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                piece_count += 1
                next_row = next_pos[0] + 1
                next_pos = [next_row, col]
            elif game.whats_here(next_pos)[1] == '#':
                saw_a_cannon = True
            else:
                next_row = next_pos[0] + 1
                next_pos = [next_row, col]

        # Check to the east
        next_pos = [row, col + 1]
        piece_count = 0
        saw_a_cannon = False
        while (not self.off_the_board(next_pos)) and (piece_count < 2) and (saw_a_cannon is False):
            if piece_count == 1:
                if game.whats_here(next_pos) == "___":
                    self._move_list.append(next_pos)
                else:
                    if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                        0].lower():
                        self._move_list.append(next_pos)
                        piece_count += 1
                    if game.whats_here(next_pos)[1] == '#':
                        saw_a_cannon = True
                    if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                        piece_count += 1
                next_col = next_pos[1] + 1
                next_pos = [row, next_col]
            elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                piece_count += 1
                next_col = next_pos[1] + 1
                next_pos = [row, next_col]
            elif game.whats_here(next_pos)[1] == '#':
                saw_a_cannon = True
            else:
                next_col = next_pos[1] + 1
                next_pos = [row, next_col]

        # Check to the west
        next_pos = [row, col - 1]
        piece_count = 0
        saw_a_cannon = False
        while (not self.off_the_board(next_pos)) and (piece_count < 2) and (saw_a_cannon is False):
            if piece_count == 1:
                if game.whats_here(next_pos) == "___":
                    self._move_list.append(next_pos)
                else:
                    if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                        0].lower():
                        self._move_list.append(next_pos)
                        piece_count += 1
                    if game.whats_here(next_pos)[1] == '#':
                        saw_a_cannon = True
                    if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                        piece_count += 1
                next_col = next_pos[1] - 1
                next_pos = [row, next_col]
            elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                piece_count += 1
                next_col = next_pos[1] - 1
                next_pos = [row, next_col]
            elif game.whats_here(next_pos)[1] == '#':
                saw_a_cannon = True
            else:
                next_col = next_pos[1] - 1
                next_pos = [row, next_col]

        if current_pos in self._blue_palace_diags or current_pos in self._red_palace_diags:

            # CHeck to the southeast
            next_pos = [row + 1, col + 1]
            piece_count = 0
            saw_a_cannon = False
            while ((not self.off_the_board(next_pos)) and next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (piece_count < 2) and (saw_a_cannon is False):
                if piece_count == 1:
                    if game.whats_here(next_pos) == "___":
                        self._move_list.append(next_pos)
                    else:
                        if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                            0].lower():
                            self._move_list.append(next_pos)
                            piece_count += 1
                        if game.whats_here(next_pos)[1] == '#':
                            saw_a_cannon = True
                        if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                            piece_count += 1
                    next_row = next_pos[0] + 1
                    next_col = next_pos[1] + 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                    piece_count += 1
                    next_row = next_pos[0] + 1
                    next_col = next_pos[1] + 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos)[1] == '#':
                    saw_a_cannon = True
                else:
                    next_row = next_pos[0] + 1
                    next_col = next_pos[1] + 1
                    next_pos = [next_row, next_col]

            # Check to the southeast
            next_pos = [row + 1, col - 1]
            piece_count = 0
            saw_a_cannon = False
            while ((not self.off_the_board(next_pos)) and next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (piece_count < 2) and (saw_a_cannon is False):
                if piece_count == 1:
                    if game.whats_here(next_pos) == "___":
                        self._move_list.append(next_pos)
                    else:
                        if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                            0].lower():
                            self._move_list.append(next_pos)
                            piece_count += 1
                        if game.whats_here(next_pos)[1] == '#':
                            saw_a_cannon = True
                        if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                            piece_count += 1
                    next_row = next_pos[0] + 1
                    next_col = next_pos[1] - 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                    piece_count += 1
                    next_row = next_pos[0] + 1
                    next_col = next_pos[1] - 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos)[1] == '#':
                    saw_a_cannon = True
                else:
                    next_row = next_pos[0] + 1
                    next_col = next_pos[1] - 1
                    next_pos = [next_row, next_col]

            # Check to the northwest
            next_pos = [row - 1, col - 1]
            piece_count = 0
            saw_a_cannon = False
            while ((not self.off_the_board(next_pos)) and next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (piece_count < 2) and (saw_a_cannon is False):
                if piece_count == 1:
                    if game.whats_here(next_pos) == "___":
                        self._move_list.append(next_pos)
                    else:
                        if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                            0].lower():
                            self._move_list.append(next_pos)
                            piece_count += 1
                        if game.whats_here(next_pos)[1] == '#':
                            saw_a_cannon = True
                        if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                            piece_count += 1
                    next_row = next_pos[0] - 1
                    next_col = next_pos[1] - 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                    piece_count += 1
                    next_row = next_pos[0] - 1
                    next_col = next_pos[1] - 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos)[1] == '#':
                    saw_a_cannon = True
                else:
                    next_row = next_pos[0] - 1
                    next_col = next_pos[1] - 1
                    next_pos = [next_row, next_col]

            # Check to the northeast
            next_pos = [row - 1, col + 1]
            piece_count = 0
            saw_a_cannon = False
            while ((not self.off_the_board(next_pos)) and next_pos in self._blue_palace_diags or next_pos in self._red_palace_diags) and (piece_count < 2) and (saw_a_cannon is False):
                if piece_count == 1:
                    if game.whats_here(next_pos) == "___":
                        self._move_list.append(next_pos)
                    else:
                        if game.whats_here(next_pos)[1] != '#' and game.whats_here(next_pos)[0] == self._opponent[
                            0].lower():
                            self._move_list.append(next_pos)
                            piece_count += 1
                        if game.whats_here(next_pos)[1] == '#':
                            saw_a_cannon = True
                        if game.whats_here(next_pos)[0] != self._opponent[0].lower():
                            piece_count += 1
                    next_row = next_pos[0] - 1
                    next_col = next_pos[1] + 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos) != "___" and game.whats_here(next_pos)[1] != '#':
                    piece_count += 1
                    next_row = next_pos[0] - 1
                    next_col = next_pos[1] + 1
                    next_pos = [next_row, next_col]
                elif game.whats_here(next_pos)[1] == '#':
                    saw_a_cannon = True
                else:
                    next_row = next_pos[0] - 1
                    next_col = next_pos[1] + 1
                    next_pos = [next_row, next_col]

        return self._move_list


class Horse(Piece):
    """Represents the Horse pieces.Communicates with the Piece class to inherit from it, and is created by the JanggiGame class.
    The JanggiGame class will also update the piece's location on the board.The piece knows what all its valid moves are from its current
    position."""

    def __init__(self, player):
        """Initializes the piece and sets it to belong to a certain player. Initializes the list of viable moves for the piece"""
        super().__init__(player)

        self._movement = [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self._block_direction = [(-1, 0), (-1, 0), (1, 0), (1, 0), (0, 1), (0, -1), (0, 1), (0, -1)]
        self._blocking_spots = []

        if player == "Blue":
            self._opponent = "Red"
            self._icon = blue_horse
        else:
            self._opponent = "Blue"
            self._icon = red_horse

    def check_for_moves(self, game):
        """Receives the game object that is playing with this piece as a parameter, to allow it to check for valid moves.
                Based on its current location, the piece will check all available positions it could move to to see if they're valid.
                If it is, it adds it to the valid_moves list"""

        current_pos = self.get_location()
        self._move_list = []

        for index in range(len(self._movement)):
            # Get the target position
            new_pos = [int(current_pos[0]) + self._movement[index][0], int(current_pos[1]) + self._movement[index][1]]

            # If the new position is on the board
            if (new_pos[0] >= 0 and new_pos[0] <= 9) and (new_pos[1] >= 0 and new_pos[1] <= 8):
                # Get the blocking spot and check if its blocked
                blocking_spot = [int(current_pos[0]) + self._block_direction[index][0],
                                 int(current_pos[1]) + self._block_direction[index][1]]

                # If the blocking spot is free and the end position is either free or has an opponent there, add it to the list
                if game.whats_here(blocking_spot) == "___" and (
                        game.whats_here(new_pos) == "___" or game.whats_here(new_pos)[0] == self._opponent[0].lower()):
                    self._move_list.append(new_pos)

        return self._move_list


class Elephant(Horse):
    """Represents the Elephant pieces, and inherits from the Horse class, as they have very similar movement and the same
    move checking logic. Communicates with the Piece class to inherit from it, and is created by the JanggiGame class.
    The JanggiGame class will also update the piece's location on the board.The piece knows what all its valid moves are from its current
    position."""

    def __init__(self, player):
        """Initializes the piece and sets it to belong to a certain player. Initializes the list of viable moves for the piece"""
        super().__init__(player)
        if player == "Blue":
            self._icon = blue_el
        else:
            self._icon = red_el

        self._movement = [(-3, 2), (-3, -2), (3, 2), (3, -2), (2, 3), (2, -3), (-2, 3), (-2, -3)]