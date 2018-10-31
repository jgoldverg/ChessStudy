import unittest
import pgnParser


class png_parser_test(unittest.TestCase):

    def test_load_file(self):
        first_event = pgnParser.PGN_2_FEN(
            '/home/jacob/ChessIndependentStudy/RAW/wco2018openthru9/wco2018_r01_open.pgn').extract_data()[0].event
        self.assertEqual(len('[Event "World Chess Olympiad 2018"]'.strip()), len(str(first_event).strip()))

    def test_load_file_Date(self):
        first_date = pgnParser.PGN_2_FEN(
            '/home/jacob/ChessIndependentStudy/RAW/wco2018openthru9/wco2018_r01_open.pgn').extract_data()[0].date
        self.assertEqual('[Date "2018.09.24"]'.strip(), str(first_date).strip())

    def test_moves_file_moves(self):
        moves = pgnParser.PGN_2_FEN(
            '/home/jacob/ChessIndependentStudy/RAW/wco2018openthru9/wco2018_r01_open.pgn').extract_data()[0].moves
        self.assertIsNotNone(moves)

    def test_game_object_moves_clock(self):
        test_obj = pgnParser.PGN_2_FEN(
            '/home/jacob/ChessIndependentStudy/RAW/wco2018openthru9/wco2018_r01_open.pgn').extract_data()[0]
        move_to_check = test_obj.moves
        self.assertIsNotNone(move_to_check)


    def test_game_move_parse(self):
        test_obj = pgnParser.PGN_2_FEN(
            '/home/jacob/ChessIndependentStudy/RAW/wco2018openthru9/wco2018_r01_open.pgn').extract_data()[0]
        move_to_check = test_obj.moves
        list(move_to_check)
        self.assertEqual('1. e4 {[%clk 1:23:29]} c5 {[%clk 1:30:39]} ', move_to_check[0])

    def test_move_converter(self):
        test_obj = pgnParser.PGN_2_FEN(
            '/home/jacob/ChessIndependentStudy/RAW/wco2018openthru9/wco2018_r01_open.pgn').extract_data()[0]
        move_to_check = test_obj.convert_moves()[1]
        self.assertEqual('e4', move_to_check)
