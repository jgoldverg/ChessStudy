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
        temp = str(self.raw_data).replace("'", "")
        temp = str(temp).replace(',', '')
        self.moves = list(re.findall(r'(?:\d+\.\s+)?(.*?)\s+\{[^}]*\}(?:\s+\d+\.\s+)?', temp.strip()))

    def strip_moves(self):
        stripped_moves = [move.strip() for move in self.raw_data]
        for i in stripped_moves:
            if i == '':
                stripped_moves.remove(i)
        self.raw_data = stripped_moves

    def convert_time(self):
        self.times = list(
            re.findall(r"{\[%clk (.*?)\]}", str(self.raw_data)))
        value = re.findall(r'((.*?)\d:\d\d:\d\d)', str(self.times))
        print(value)

    def time_convert_to_time_used(self, value):
        value = re.findall(r'((.*?)\d[:]\d\d[:]\d\d)', str(self.times))
        hours = 0
        minuites = 0
        seconds = 0
        print(value)


class Move(object):

    def __int__(self, move):
        self.move = move

    def clean_move(self):
        for line in self.move:
            str(line)
