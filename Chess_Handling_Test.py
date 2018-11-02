import unittest
import pandas
import ChessHandling


class Chess_Handling_Test(unittest.TestCase):

    def test_load_fen_shouldBeZero(self):
        self.assertEqual(set([0]), ChessHandling.parse_fen('kK'))

    def test_load_fen_queen(self):
        self.assertEqual({0, 9}, ChessHandling.parse_fen('q'))

    def test_load_fen_pawns(self):
        self.assertEqual(set([8]), ChessHandling.parse_fen('pppppppp/PPPPPPPP'))

    def test_load_fen_starting(self):
        self.assertEqual(set([39]), ChessHandling.parse_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))

    def test_exception(self):
        self.assertEqual('000', ChessHandling.parse_fen('#GAME'))

    def test_load_result_shouldBeZero(self):
        self.assertEqual(None, ChessHandling.parse_result('1'))

    def test_load_result_halfOfTwo(self):
        self.assertEqual(.5, ChessHandling.parse_result('1/2'))

    def test_load_result_white_win(self):
        self.assertEqual(1, ChessHandling.parse_result('1-0'))

    def test_load_result_blackwin(self):
        self.assertEqual(-1, ChessHandling.parse_result('0-1'))



