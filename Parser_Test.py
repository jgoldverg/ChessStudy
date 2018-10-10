import unittest
import Parser


class MyTestCase(unittest.TestCase):


    def test_load_fen_queen(self):
        self.assertEqual({0, 9}, self.parse_fen('q'))

    def test_load_fen_pawns(self):
        self.assertEqual(set([8]), self.parse_fen('pppppppp/PPPPPPPP'))

    def test_load_fen_starting(self):
        self.assertEqual(set([8]), self.parse_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))


if __name__ == '__main__':
    unittest.main()
