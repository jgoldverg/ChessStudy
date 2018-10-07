import unittest
import pandas
import ChessHandling


class Chess_Handling_Test(unittest.TestCase):

    def test_load_fen(self):
        self.assertEqual({[0]},
                         ChessHandling.parse_fen('kK'))
    def test_load_fen_queen(self):
        self.assertEqual({0,9}, ChessHandling.parse_fen('q'))

    def test_load_files(self):
        self.assertEqual(1, ChessHandling.Game.load_files())