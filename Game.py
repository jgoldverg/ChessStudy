import re


class Game(object):
    #event, site date, round, board# as str, whiteId, blackId, WhiteName, BlackName, Result(1-0, 0-1, 1/2), ChessVersion(irrelevant), blackRating, whiteRating, moveslist
    def __init__(self, event):
        self.event = event
        self.moves = []

    def convert_clock(self):
        results = re.findall(r"{\[%clk (.*?)\]}", str(self.moves))
        


