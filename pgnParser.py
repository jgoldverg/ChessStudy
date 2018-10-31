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

        with open(self.file) as f:
            for line in f:
                if len(line) == 0:
                    continue
                if line.startswith('[Event'):
                    game_list.append(Game.Game(line))

                elif line.startswith('[Site'):
                    game_list.__getitem__(-1).site = line

                elif line.startswith('[Date'):
                    game_list.__getitem__(-1).date = line

                elif line.startswith('[Round'):
                    game_list.__getitem__(-1).round = line

                elif line.startswith('[Board'):
                    game_list.__getitem__(-1).board = line

                elif line.startswith('[WhiteElo'):
                    game_list.__getitem__(-1).whiteElo = line

                elif line.startswith('[BlackElo'):
                    game_list.__getitem__(-1).blackElo = line

                elif line.startswith('[White'):
                    game_list.__getitem__(-1).whiteName = line

                elif line.startswith('[Black'):
                    game_list.__getitem__(-1).blackName = line

                elif line.startswith('[Result'):
                    game_list.__getitem__(-1).result = line

                elif line.startswith('[WhiteFideId'):
                    game_list.__getitem__(-1).whiteFid = line

                elif line.startswith('[BlackFideId'):
                    game_list.__getitem__(-1).blackFid = line

                elif line.startswith('[Live'):
                    game_list.__getitem__(-1).site = line

                elif line.startswith('[ECO'):
                    game_list.__getitem__(-1).eco = line

                else:
                    game_list.__getitem__(-1).raw_data.append(line)

        return game_list
