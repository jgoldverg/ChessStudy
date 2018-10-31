import pandas as pd
import os
import fileinput
import numpy as np

local_directory_test = '/home/jacob/ChessIndependentStudy/MOVES'
# Looking up the points to convert them
blackPointsDictionary = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9}
whitePointsDictionary = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9}

columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                "MovePlayedValue", "ValueDifference"]


# method takes in string, for convenience I decided to take the whole string and just the fen seperately(not
def parse_fen(row):
    fen_str_no_space = str(row).split(' ')[0]
    print(fen_str_no_space)
    white_points = 0
    black_points = 0
    #    positions_to_calculate = str(row).split('\n')
    if '#' in str(row):
        return 000
    for c in fen_str_no_space:
        if str(c) in blackPointsDictionary.keys():
            black_points += blackPointsDictionary.get(c)
        elif str(c) in whitePointsDictionary.keys():
            white_points += whitePointsDictionary.get(c)
        else:
            continue
    x = white_points - black_points
    return int(x)


# white win is a 1 black win is a -1 and a draw is 1/2 or (.5)


result_options = {'1/2': 0.5, '0-1': -1.0, '1-0': 1.0}


def parse_result(row):
    if row in result_options:
        return result_options.get(row)
    else:
        return 0.0


# the method using parseResult and parseFen to see if there was a comeback so to speak.
def ten_point_lead_and_lost(row):
    if row['Score'] > 900 and row['NoTie'] == -1.0:
        return 'black flip'
    elif row['Score'] < -900 and row['NoTie'] == 1.0:
        return 'white flip'
    else:
        return ''


def ten_point_calculate(point, result):
    point = parse_fen(point)
    result = parse_result(result)
    if point > 900 and result == -1.0:
        return 'black'
    elif point < -900 and result == 1.0:
        return 'white'
    else:
        return ''


def load_multiple_files(path, column_names):
    if path is None:
        file_list_names = os.listdir(local_directory_test)
    else:
        file_list_names = os.listdir(path)

    np_array = []
    for file_ in file_list_names:
        data_frame = pd.read_csv(local_directory_test + '/' + file_, names=columns_list)
        np_array.append(data_frame.as_matrix())

    combo_np = np.vstack(np_array)
    return combo_np
