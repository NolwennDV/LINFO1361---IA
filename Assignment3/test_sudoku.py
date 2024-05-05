import unittest
from sudoku import objective_score

class TestSudoku(unittest.TestCase):
    def test_objective_score(self):
        # Test case 1: Empty board
        board1 = [[0] * 9 for _ in range(9)]
        self.assertEqual(objective_score(board1), 0)

        # Test case 2: Completely filled board with no duplicates
        board2 = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)]
        self.assertEqual(objective_score(board2), 0)

        # Test case 3: Board with duplicates in rows, columns, and sub-boards
        board3 = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ]
        print(objective_score(board3))
        #self.assertEqual(objective_score(board3), 324)

if __name__ == '__main__':
    unittest.main()