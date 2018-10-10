import pandas as pd
import os
import fileinput
import numpy as np

filePathTest = '/shared/projects/regan/Chess/CSE712/MOVES/AA1025Kom10moves.txt'

file_path_local = '/home/jacob/ChessIndependentStudy/MOVES/AA1025Kom10moves.txt'

local_directory_test = '/home/jacob/ChessIndependentStudy/MOVES'
# Looking up the points to convert them
blackPointsDictionary = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9}
whitePointsDictionary = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9}

columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                "MovePlayedValue", "ValueDifference"]
df = pd.read_csv(file_path_local, names=columns_list)


# method takes in string, for convenience I decided to take the whole string and just the fen seperately(not
def parse_fen(row):
    fen_str_no_space = str(row).split(' ')[0]
    white_points = 0
    black_points = 0
    #    positions_to_calculate = str(row).split('\n')
    print()
    if '#' in str(row):
        return {'new game'}
    for c in fen_str_no_space:
        if str(c) in blackPointsDictionary.keys():
            black_points += blackPointsDictionary.get(c)
        elif str(c) in whitePointsDictionary.keys():
            white_points += whitePointsDictionary.get(c)
        else:
            continue
    return white_points - black_points


# white win is a 1 black win is a -1 and a draw is 1/2 or (.5)


result_options = {'1/2': .5, '0-1': -1, '1-0': 1}


def parse_result(row):
    print(row)
    if row in result_options:
        return result_options.get(row)
    else:
        return None


# the method using parseResult and parseFen to see if there was a comeback so to speak.
def ten_point_lead_and_lost(row):
    if row['Score'] > 900.0 and row['NoTie'] == -1.0:
        return 'black flip'
    elif row['Score'] < -900.0 and row['NoTie'] == 1.0:
        return 'white flip'
    else:
        return None

def write_file(name):
    df.to_csv(name + 'DataFrame')


def load_multiple_files(path):
    if path is None:
        file_list_names = os.listdir(local_directory_test)
    else:
        file_list_names = os.listdir(path)

    np_array = []
    for file_ in file_list_names:
        data_frame = pd.read_csv(local_directory_test + '/' + file_, names=columns_list)
        np_array.append(data_frame.as_matrix())

    combo_np = np.vstack(np_array)
    return pd.DataFrame(combo_np)


df['Points'] = df['FEN-Position'].apply(parse_fen)
