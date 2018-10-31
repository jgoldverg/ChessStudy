import re


class Game(object):
    # event, site date, round, board# as str, whiteId, blackId, WhiteName, BlackName, Result(1-0, 0-1, 1/2), ChessVersion(irrelevant), blackRating, whiteRating, moveslist
    def __init__(self, event):
        self.event = event
        self.raw_data = []
        self.times = []
        self.moves = []

    def convert_moves(self):
        self.strip_moves()
        self.moves = list(re.findall("(?:\d+\.\s+)?(.*?)\s+\{[^}]*\}(?:\s+\d+\.\s+)?", str(self.raw_data)))

    def strip_moves(self):
        stripped_moves = [move.strip() for move in self.raw_data]
        for i in stripped_moves:
            if i == '':
                stripped_moves.remove(i)
        self.raw_data = stripped_moves

    def convert_time(self):
        self.times = list(
            re.findall(r"{\[%clk (.*?)\]}", str(self.raw_data)))
