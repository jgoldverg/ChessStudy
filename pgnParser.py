import os
import Game


class PGN_2_FEN(object):

    def __init__(self, file):
        self.file = file

        self.values = {1: 'Event', 2: 'Site', 3: 'Date', 4: 'Round', 5: 'Board', 6: 'WhiteFideId', 7: 'BlackFideId',
                       8: 'White', 9: 'Black', 10: 'Result', 11: 'LiveChessVersion', 12: "WhiteElo", 13: 'BlackElo',
                       14: 'ECO'}

    def extract_data(self):
        game_list = []

        line = open(self.file).readline()
        while line:
            if line.startswith('[Event'):
                game = Game.Game(line)
                game_list.append(game)

                if len(line) == 0:
                    continue

            if line.startswith(('[Site')):
                game_list.__getitem__(-1).site = line

            if line.startswith(('[Date')):
                game_list.__getitem__(-1).date = line

            if line.startswith(('[Round')):
                game_list.__getitem__(-1).round = line

            if line.startswith(('[Board')):
                game_list.__getitem__(-1).board = line

            if line.startswith(('[WhiteElo')):
                game_list.__getitem__(-1).whiteElo = line

            if line.startswith(('[BlackElo')):
                game_list.__getitem__(-1).blackElo = line

            if line.startswith(('[White')):
                game_list.__getitem__(-1).whiteName = line

            if line.startswith(('[Black')):
                game_list.__getitem__(-1).blackName = line

            if line.startswith(('[Result')):
                game_list.__getitem__(-1).result = line

            if line.startswith(('[WhiteFideId')):
                game_list.__getitem__(-1).whiteFid = line

            if line.startswith(('[BlackFideId')):
                game_list.__getitem__(-1).blackFid = line

            if line.startswith(('[Live')):
                game_list.__getitem__(-1).site = line

            if line.startswith(('[ECO')):
                game_list.__getitem__(-1).eco = line

        return game_list
