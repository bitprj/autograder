test = {
    "name": "test.py",
    "points": 1,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> board = create_board(7, 9)\n>>> print(board)\nMines: 9\n  0123456\n0 XXXXXXX 0\n1 XXXXXXX 1\n2 XXXXXXX 2\n3 XXXXXXX 3\n4 XXXXXXX 4\n5 XXXXXXX 5\n6 XXXXXXX 6\n  0123456\n>>> random.seed(5)\n>>> board = create_board(7, 9)\n>>> board.show(2, 3)\n>>> board.flag(4, 6)\n>>> print(board)\nMines: 8\n  0123456\n0 XXXXXXX 0\n1 XXXXXXX 1\n2 XXXMXXX 2\n3 XXXXXXX 3\n4 XXXXXXF 4\n5 XXXXXXX 5\n6 XXXXXXX 6\n  0123456\n>>> random.seed(9)\n>>> board = create_board(9, 10)\n>>> board.show(3, 7)\n>>> board.flag(0, 0)\n>>> print(board)\nMines: 9\n  012345678\n0 F1        0\n1 X1        1\n2 X111221   2\n3 XXXXXX1   3\n4 XXXXXX21  4\n5 XXXXXXX1  5\n6 XXXXXXX2  6\n7 XXXXXXX1  7\n8 XXXXXXX1  8\n  012345678\n>>> random.seed(9)\n>>> board = create_board(9, 10)\n>>> board.show(3, 7)\n>>> board.flag(0, 0)\n>>> board.show(4, 0)\n>>> board.show(6, 2)\n>>> board.show(7, 2)\n>>> print(board)\nMines: 9\n  012345678\n0 F1        0\n1 X1        1\n2 X111221   2\n3 XXXXXX1   3\n4 1XXXXX21  4\n5 XXXXXXX1  5\n6 XX1XXXX2  6\n7 XX2XXXX1  7\n8 XXXXXXX1  8\n  012345678\n>>> random.seed(9)\n>>> board = create_board(9, 10)\n>>> board.show(3, 7)\n>>> board.flag(0, 0)\n>>> board.show(4, 0)\n>>> board.show(6, 2)\n>>> board.show(7, 2)\n>>> board.flag(7, 0)\n>>> board.show(4, 2)\n>>> board.show(8, 4)\n>>> board.show(8, 0)\n>>> print(board)\nMines: 8\n  012345678\n0 F1        0\n1 X1        1\n2 X111221   2\n3 XXXXXX1   3\n4 1X222321  4\n5 XXX1 1X1  5\n6 XX11 2X2  6\n7 FX21 1X1  7\n8 MXX1 1X1  8\n  012345678\n\n\n\n"
                }
            ],
            "setup": ">>> from checkpoint1 import *\n",
            "type": "doctest"
        }
    ]
}