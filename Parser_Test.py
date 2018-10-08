import unittest
import Parser


class MyTestCase(unittest.TestCase):

    def test_load_fen_shouldBeZero(self):
        self.assertEqual(set([0]), Parser.parse_fen('kK'))

    def test_load_fen_queen(self):
        self.assertEqual({0, 9}, Parser.parse_fen('q'))

    def test_load_fen_pawns(self):
        self.assertEqual(set([8]), Parser.parse_fen('pppppppp/PPPPPPPP'))

    def test_load_fen_starting(self):
        self.assertEqual(set([8]), Parser.parse_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))
