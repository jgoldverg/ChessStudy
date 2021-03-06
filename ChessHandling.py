import pandas as pd
import os
import fileinput
import numpy as np

local_directory_test = '/home/jacob/ChessIndependentStudy/MOVES'
# Looking up the points to convert them
blackPointsDictionary = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9}
whitePointsDictionary = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9}


# method takes in string, for convenience I decided to take the whole string and just the fen seperately(not
def parse_fen(row):
    fen_str_no_space = str(row).split(' ')[0]
    white_points = 0
    black_points = 0
    #    positions_to_calculate = str(row).split('\n')
    if '#' in str(row):
        return '000'
    for c in fen_str_no_space:
        if blackPointsDictionary.keys().__contains__(c):
            black_points += blackPointsDictionary.get(c)
        elif whitePointsDictionary.keys().__contains__(c):
            white_points += whitePointsDictionary.get(c)

    x = white_points - black_points
    return str(x)


# white win is a 1 black win is a -1 and a draw is 1/2 or (.5)


result_options = {'1/2': 0.5, '0-1': -1.0, '1-0': 1.0}


def parse_result(row):
    if row in result_options.keys():
        return int(result_options.get(row))
    else:
        return 0.0


def ten_point_calculate(point, result):
    num = parse_fen(point)
    res = parse_result(str(result))
    if str(num) == '000':
        return 'new game'
    if int(num) >= 9 and res == -1.0:
        return 'black'
    elif int(num) <= -9 and res == 1.0:
        return 'white'
    else:
        return '000'


def nine_pt_calculate(EMV, res):
    if str(res).__contains__(';'):
        return -1000
    elif EMV > 900 and res == -1.0:
        return -1
    elif EMV < -900 and res == 1.0:
        return 1
    else:
        return 0


def load_multiple_files(path, column_names):
    if path is None:
        file_list_names = os.listdir(local_directory_test)
    else:
        file_list_names = os.listdir(path)

    np_array = []
    for file_ in file_list_names:
        data_frame = pd.read_csv(local_directory_test + '/' + file_, names=column_names)
        np_array.append(data_frame.as_matrix())

    combo_np = np.vstack(np_array)
    return combo_np


def read_file(file):
    list = []
    with open(file) as f:
        for line in f:
            inner_list = line.split(',')
            list.append(inner_list)



