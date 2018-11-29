import os
import Game
import re
class PGN_2_FEN(object):

    def __init__(self, file):
        self.file = file

        self.values = {1: 'Event', 2: 'Site', 3: 'Date', 4: 'Round', 5: 'Board', 6: 'WhiteFideId', 7: 'BlackFideId',
                       8: 'White', 9: 'Black', 10: 'Result', 11: 'LiveChessVersion', 12: "WhiteElo", 13: 'BlackElo',
                       14: 'ECO'}
        self.game_list = []

    def extract_data(self):
        game_list = []
        with open(self.file) as f:
            for line in f:
                if str(line).__contains__('[Event'):
                    game_list.append(Game.Game(line))

                elif line.startswith('[Site'):
                    game_list.__getitem__(len(game_list)-1).site = line

                elif line.startswith('[Date'):
                    game_list.__getitem__(len(game_list)-1).date = line

                elif line.startswith('[Round'):
                    game_list.__getitem__(len(game_list)-1).round = line

                elif line.startswith('[Board'):
                    game_list.__getitem__(len(game_list)-1).board = line

                elif line.startswith('[WhiteElo'):
                    game_list.__getitem__(len(game_list)-1).whiteElo = line

                elif line.startswith('[BlackElo'):
                    game_list.__getitem__(len(game_list)-1).blackElo = line

                elif line.startswith('[White'):
                    game_list.__getitem__(len(game_list)-1).whiteName = line

                elif line.startswith('[Black'):
                    game_list.__getitem__(len(game_list)-1).blackName = line

                elif line.startswith('[Result'):
                    game_list.__getitem__(len(game_list)-1).result = line

                elif line.startswith('[WhiteFideId'):
                    game_list.__getitem__(len(game_list)-1).whiteFid = line

                elif line.startswith('[BlackFideId'):
                    game_list.__getitem__(len(game_list)-1).blackFid = line

                elif line.startswith('[Live'):
                    game_list.__getitem__(len(game_list)-1).site = line

                elif line.startswith('[ECO'):
                    game_list.__getitem__(len(game_list)-1).eco = line

                elif line.__contains__(';'):
                    continue
                else:
                    game_list.__getitem__(len(game_list)-1).raw_data.append(line)

        self.game_list = game_list
