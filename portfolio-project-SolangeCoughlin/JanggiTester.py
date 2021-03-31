import unittest
from JanggiGame import JanggiGame, Piece, General, Horse, Chariot, Soldier, Elephant, Cannon, Guard


class MyTestCase(unittest.TestCase):

    def test_general_movement(self):
        """Fixed row numbers"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("e2","e3"), False) # Red General can't move, not their turn
        self.assertEqual(Janggi.make_move("e9","e8"), True) # Blue General moves successfully
        self.assertEqual(Janggi.make_move("e2", "e3"), True) # Red General moves successfully
        self.assertEqual(Janggi.make_move("e8","e7"), False) # Blue General can't move outside palace
        self.assertEqual(Janggi.make_move("e2","d2"), False) # Red General can't move, not their turn
        self.assertEqual(Janggi.make_move("e8","d8"), True) # Blue General moves successfully
        self.assertEqual(Janggi.make_move("e3", "d3"), True) # Red General moves successfully
        Janggi.make_move("d8","d9")
        self.assertEqual(Janggi.make_move("d3", "c3"), False) # Red General can't move outside palace

        Janggi = JanggiGame() # Reinitialize the game
        self.assertEqual(Janggi.make_move("e9","d10"),False) # Blue - there's an advisor there
        self.assertEqual(Janggi.make_move("e9", "f1"), False)  # Blue - there's an advisor there
        self.assertEqual(Janggi.make_move("e9", "f9"), True) # Blue - successful move
        self.assertEqual(Janggi.make_move("e2","e2"),True) #Red pass
        self.assertEqual(Janggi.make_move("f9", "g9"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("f9", "f8"), True) # Blue success
        self.assertEqual(Janggi.make_move("e2", "e2"), True)  # Red pass
        self.assertEqual(Janggi.make_move("f8", "f7"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("f8", "g8"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("f8", "e8"), True)  # Blue moves
        self.assertEqual(Janggi.make_move("e2", "e2"), True)  # Red pass
        self.assertEqual(Janggi.make_move("e8", "e7"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("e8", "d8"), True)  # Blue moves
        self.assertEqual(Janggi.make_move("e2", "e2"), True)  # Red pass
        self.assertEqual(Janggi.make_move("d8", "d7"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("d8", "c8"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("d8", "d9"), True)  # Blue moves
        self.assertEqual(Janggi.make_move("e2", "e2"), True)  # Red pass
        self.assertEqual(Janggi.make_move("d9", "c9"), False)  # Blue - can't leave palace
        self.assertEqual(Janggi.make_move("d9", "e9"), True)  # Blue moves
        self.assertEqual(Janggi.make_move("e2", "e2"), True)  # Red pass
        self.assertEqual(Janggi.make_move("e9", "f8"), True)  # Blue moves diagonally



    def test_guard_movement(self):
        """Fixed row numbers"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("d10","e9"), False) # Should not allow guard to move onto the square where the general is
        self.assertEqual(Janggi.make_move("d10","d9"), True) # Blue guard moves successfully
        Janggi.make_move("e2","e2")
        self.assertEqual(Janggi.make_move("d9", "e10"), False) # Blue can't move diagonally in this direction
        self.assertEqual(Janggi.make_move("e9", "e10"), True) # Move general out of the way
        Janggi.make_move("e2", "e2")
        self.assertEqual(Janggi.make_move("d9", "d8"), True)
        Janggi.make_move("e2", "e2")
        self.assertEqual(Janggi.make_move("d8", "e9"), True)

    def test_soldier_movement(self):
        """Row numbers have been fixed"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("e7","e6"), True) # Blue soldier moves successfully
        self.assertEqual(Janggi.make_move("g4","g5"), True) # Red soldier moves successfully
        self.assertEqual(Janggi.make_move("f7", "f8"), False) # Blue soldier can't move backwards
        self.assertEqual(Janggi.make_move("f7","g7"), False) # Blue soldier can't move onto a space occupied by a blue piece
        self.assertEqual(Janggi.make_move("g7","g6"), True) # Blue soldier moves successfully
        self.assertEqual(Janggi.make_move("g5", "g6"), True) # Red soldier captures a blue piece

    def test_chariot_movement_1(self):
        """Fixed row numbers. Testing vertical and horizontal movement"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("a10","e10"), False) # Should not be able to move the chariot to this spot, due to blocking pieces
        self.assertEqual(Janggi.make_move("a10","a9"),True) # Move the chariot north successfully
        Janggi.make_move("e2","e2") # Red pass
        self.assertEqual(Janggi.make_move("a9","d9"),True) # Move the chariot east successfully
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("d9", "d1"), True)  # Move the chariot north successfully, capture a Red piece

    def test_chariot_movement_2(self):
        """Testing horizontal movement in the palace"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("a10", "a9"), True)  # Move the chariot north successfully
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("a9", "d9"), True)  # Move the chariot east successfully
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("d9","d8"), True) # Move the chariot north
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("e9", "e8"), True) # move the general out of the way
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("d8", "e9"), True) # Move diagonally 1
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("e9", "f10"), False) # advisor in the way
        self.assertEqual(Janggi.make_move("e9", "d10"), False) # advisor in the way
        self.assertEqual(Janggi.make_move("f10", "e10"), True) # move the advisor
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("e9", "f10"), True) # successfully
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("f10", "c7"), False) # can't move diagonally out of the palace
        Janggi.print_board()
        self.assertEqual(Janggi.make_move("f10", "d8"), True) # Move diagonally across the palace
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("e8","e9"), True) # move the general out of the way
        Janggi.make_move("e2", "e2")  # Red pass
        self.assertEqual(Janggi.make_move("d8", "g8"), True) # move horizontally out of the palace

    def test_horse_movement(self):
        """Fixed row numbers"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("c10","d8"),True) # Successfully move the blue horse
        self.assertEqual(Janggi.make_move("c1","c2"), False) # Not a valid move for red horse
        self.assertEqual(Janggi.make_move("c1","d3"), True) # Move red horse successfully
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("e9","e8"),True) # Move blue general up
        self.assertEqual(Janggi.make_move("c1","d3"),True) # Move red horse
        self.assertEqual(Janggi.make_move("c10", "e9"), False) # Blue horse can't move, blocked by advisor
        self.assertEqual(Janggi.make_move("d10","d9"), True) # Move the advisor out of the way
        self.assertEqual(Janggi.make_move("d3","e5"), True) # Move the red horse
        self.assertEqual(Janggi.make_move("c10","e9"), True) # Blue horse moves successfully



    def test_elephant_movement(self):
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("b10","d7"), True) # Blue elephant successfully moves
        self.assertEqual(Janggi.make_move("b1","e3"), False) # Red elephant is blocked in this direction
        self.assertEqual(Janggi.make_move("b1","d4"), True) # Red elephant moves successfully

    def test_cannon_movement_1(self):
        """Fixed row numbers"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("b8","b6"), False) # Blue cannon, nothing to jump
        self.assertEqual(Janggi.make_move("c7", "b7"), True) # Blue soldier moving into position for jumping
        self.assertEqual(Janggi.make_move("c4", "b4"), True) # Red soldier moving into position for jumping
        self.assertEqual(Janggi.make_move("b8", "b6"), True) # Blue cannon, valid move
        self.assertEqual(Janggi.make_move("b3", "b6"), False) # Red cannon, can't capture a cannon
        self.assertEqual(Janggi.make_move("b3", "b5"), True) # Valid red cannon movement
        self.assertEqual(Janggi.make_move("b6", "b3"), False) # Blue cannon, can't jump over a cannon
        self.assertEqual(Janggi.make_move("b6", "f6"), False) # Blue cannon has nothing to jump over
        self.assertEqual(Janggi.make_move("e7", "e6"), True) # Blue soldier (?) moves into position
        self.assertEqual(Janggi.make_move("e2", "e1"), True) # Red movement
        self.assertEqual(Janggi.make_move("b6", "f6"), True) # Valid cannon movement

    def test_cannon_movement_2(self):
        """Fixed row numbers"""
        Janggi = JanggiGame()
        self.assertEqual(Janggi.make_move("e9", "e8"), True) # blue general moves up
        self.assertEqual(Janggi.make_move("e2", "e3"),True) # red gen moves
        self.assertEqual(Janggi.make_move("b8", "f8"),True) # blue cannon moves
        self.assertEqual(Janggi.make_move("e3", "e2"),True) # red gen moves
        self.assertEqual(Janggi.make_move("d10", "e9"),True) # blue advisor moves
        self.assertEqual(Janggi.make_move("e2", "e2"), True) # red passes
        self.assertEqual(Janggi.make_move("f8", "d10"),True) # blue cannon moves

    def test_check_with_cannon(self):
        Janggi = JanggiGame()
        Janggi.make_move("a7", "b7")
        Janggi.make_move("c4", "c5")
        Janggi.make_move("b8", "b5")
        Janggi.make_move("c5", "c5")
        Janggi.make_move("b5", "e5")
        self.assertEqual(Janggi.is_in_check("Red"),True)

    def test_check_with_horse(self):
        Janggi = JanggiGame()
        Janggi.make_move("c10", "d8")
        Janggi.make_move("a1", "a1")
        Janggi.make_move("d8", "e6")
        Janggi.make_move("a1", "a1")
        Janggi.make_move("e6", "d4")
        self.assertEqual(Janggi.is_in_check("Red"),True)

    def test_game_with_check(self):
        """These moves are made the Gradescope to test is_in_check functionality"""
        Janggi = JanggiGame()
        Janggi.make_move("c7", "c6")
        Janggi.make_move("c1", "d3")
        Janggi.make_move("b10", "d7")
        Janggi.make_move("b3", "e3")
        Janggi.make_move("c10", "d8")
        Janggi.make_move("h1", "g3")
        Janggi.make_move("e7", "e6")
        Janggi.make_move("e3", "e6")
        print(Janggi.is_in_check("Blue"))
        Janggi.make_move("h8", "e8")
        Janggi.make_move("d3", "e5")
        Janggi.make_move("c8", "c4")
        Janggi.make_move("e5", "c4")
        Janggi.make_move("i10", "i8")
        Janggi.make_move("g4", "f4")
        Janggi.make_move("i8", "f8")
        Janggi.make_move("g3", "h5")
        Janggi.make_move("h10", "g8")
        Janggi.make_move("e6", "e3")
        #Janggi.print_board()
        self.assertEqual(Janggi.is_in_check("blue"),True)
        self.assertEqual(Janggi.is_in_check("red"), False)

    def test_checkmate(self):
        Janggi = JanggiGame()
        Janggi.make_move("a7", "b7")
        Janggi.make_move("g4", "h4")
        Janggi.make_move("c10", "d8")
        Janggi.make_move("h3", "h5")
        Janggi.make_move("i7", "h7")
        Janggi.make_move("e2", "f3")
        Janggi.make_move("h10", "f7")
        Janggi.make_move("e4", "e5")
        Janggi.make_move("h7", "h6")
        Janggi.make_move("c4", "c5")
        Janggi.make_move("h6", "h5")
        Janggi.make_move("b3", "g3")
        Janggi.make_move("f7", "h4")
        Janggi.make_move("g3", "g10")
        Janggi.make_move("i10", "i6")
        Janggi.make_move("h1", "g3")
        Janggi.make_move("i6", "d6")
        Janggi.make_move("c1", "d3")
        Janggi.make_move("d6", "d3")
        Janggi.make_move("f3", "f2")
        Janggi.make_move("h4", "f1")
        Janggi.make_move("g3", "f1")
        Janggi.make_move("b8", "f8")
        Janggi.make_move("d1", "e2")
        Janggi.make_move("g7", "f7")
        Janggi.make_move("e5", "f5")
        Janggi.make_move("d3", "g3")
        Janggi.make_move("e2", "f3")
        Janggi.make_move("g3", "g2")
        chariot = Janggi.get_piece_from_id('b%2')
        chariot.check_for_moves(Janggi)
        print(chariot.get_move_list())
        print(Janggi.checkmate_check("Red"))


    def test_checkmate_2(self):
        Janggi = JanggiGame()
        Janggi.make_move("a7", "b7")
        Janggi.make_move("g4", "h4")
        Janggi.make_move("c10", "d8")
        Janggi.make_move("h3", "h5")
        Janggi.make_move("i7", "h7")
        Janggi.make_move("e2", "f3")
        Janggi.make_move("h10", "f7")
        Janggi.make_move("e4", "e5")
        Janggi.make_move("h7", "h6")
        Janggi.make_move("c4", "c5")
        Janggi.make_move("h6", "h5")
        Janggi.make_move("b3", "g3")
        Janggi.make_move("f7", "h4")
        Janggi.make_move("g3", "g10")
        Janggi.make_move("i10", "i6")
        Janggi.make_move("h1", "g3")
        Janggi.make_move("i6", "d6")
        Janggi.make_move("c1", "d3")
        Janggi.make_move("d6", "d3")
        Janggi.make_move("f3", "f2")
        Janggi.make_move("h4", "f1")
        Janggi.make_move("g3", "f1")
        Janggi.make_move("b8", "f8")
        Janggi.make_move("d1", "e2")
        Janggi.make_move("g7", "f7")
        Janggi.make_move("e5", "f5")
        Janggi.make_move("d3", "g3")
        Janggi.make_move("e2", "f3")
        Janggi.make_move("g3", "g2")
        print(Janggi.checkmate_check("Red"))
        print(Janggi.make_move("a1", "a3"))
        # Test order
        # self._Blue_Piece_List = ["b$1", "b$2", "b^1", "b^2", "b~1", "b~2", "b%1", "b%2", "b#1", "b#2", "b-1", "b-2",
        #                         "b-3", "b-4", "b-5", "b@"]
        # self._Red_Piece_List = ["r$1", "r$2", "r^1", "r^2", "r~1", "r~2", "r%1", "r%2", "r#1", "r#2", "r-1", "r-2",
        #                        "r-3", "r-4", "r-5", "r@"]
        # self._blue_start_pos = [[9, 3], [9, 5], [9, 2], [9, 6], [9, 1], [9, 7], [9, 0], [9, 8], [7, 1], [7, 7], [6, 0],
        #                        [6, 2], [6, 4], [6, 6], [6, 8], [8, 4]]
        # self._red_start_pos = [[0, 3], [0, 5], [0, 2], [0, 7], [0, 1], [0, 6], [0, 0], [0, 8], [2, 1], [2, 7], [3, 0],
        #                       [3, 2], [3, 4], [3, 6], [3, 8], [1, 4]]


    def test_checkmate_3(self):
        Janggi = JanggiGame()
        Janggi.make_move("c10", "d8")
        Janggi.make_move("g4", "h4")
        Janggi.make_move("i7", "h7")
        Janggi.make_move("h3", "h7")
        Janggi.make_move("g7", "h7")
        Janggi.make_move("h1", "g3")
        Janggi.make_move("i10", "i6")
        Janggi.make_move("e4", "e5")
        Janggi.make_move("a7", "b7")
        Janggi.make_move("c1", "d3")
        Janggi.make_move("h10", "g8")
        Janggi.make_move("e5", "e6")
        Janggi.make_move("e7", "e6")
        Janggi.make_move("g3", "f5")
        Janggi.make_move("e6", "e5")
        Janggi.make_move("d3", "e5")
        Janggi.make_move("i6", "e6")
        Janggi.make_move("c4", "b4")
        Janggi.make_move("h8", "e8")
        Janggi.make_move("b3", "b7")
        Janggi.make_move("e6", "e5")
        Janggi.make_move("e2", "d3")
        Janggi.make_move("e5", "f5")
        Janggi.make_move("g1", "e4")
        Janggi.make_move("f5", "d5")
        Janggi.make_move("b1", "d4")
        Janggi.make_move("d5", "d4")
        print(Janggi.get_game_state())

        #self._Blue_Piece_List = ["b$1", "b$2", "b^1", "b^2", "b~1", "b~2", "b%1", "b%2", "b#1", "b#2", "b-1", "b-2",
            #                     "b-3", "b-4", "b-5", "b@"]
        #self._Red_Piece_List = ["r$1", "r$2", "r^1", "r^2", "r~1", "r~2", "r%1", "r%2", "r#1", "r#2", "r-1", "r-2",
           #                     "r-3", "r-4", "r-5", "r@"]
        #self._blue_start_pos = [[9, 3], [9, 5], [9, 2], [9, 7], [9, 1], [9, 6], [9, 0], [9, 8], [7, 1], [7, 7], [6, 0],
         #                       [6, 2], [6, 4], [6, 6], [6, 8], [8, 4]]
        #self._red_start_pos = [[0, 3], [0, 5], [0, 2], [0, 7], [0, 1], [0, 6], [0, 0], [0, 8], [2, 1], [2, 7], [3, 0],
          #                     [3, 2], [3, 4], [3, 6], [3, 8], [1, 4]]


if __name__ == '__main__':
    unittest.main()
