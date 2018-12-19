import argparse
import os
import pandas as pd
import AI_File
import pgnParser
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# Example Run python3 Main.py --input/dir/.txt --tenptlead 1 --write/dir/filename.txt
def main():
    print('hi')
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputMOVES", help="input MOVES", dest='inputMOVES', type=str)
    parser.add_argument("--inputPGN", help="input PGN Path, .png files", dest='inputPGN', type=str)
    parser.add_argument("--average", help="create average column", dest='average', type=int)
    parser.add_argument("--nineptlead", help="calculate if move had a 10pt diff with a loss", dest='nineptlead',
                        type=int)
    parser.add_argument("--graph", help="graph the current loaded dataframe", dest='graph', type=int)
    parser.add_argument('--write', help='specify path, it will be written as a csv', type=str, dest='write')
    parser.add_argument('--clean', help='clean file', type=int, dest='clean')
    args = parser.parse_args()
    df_analyzeobj = None  # when working with a single file use this
    df_array_analyze = []  # list of ai objects when working with a directory
    df_array = []  # raw dataframe list when working with a directory
    dirorfile = input('Is this a directory or a file? 0 for file, 1 for Directory:')

    if args.inputMOVES is not None:
        if int(dirorfile) == 0:  # file
            df_analyzeobj = AI_File.CleanAndAnalyze(pd.read_csv(args.inputMOVES, names=columns_list))
            print(df_analyzeobj.df['FEN-Position'].size)
            print('loaded file' + '_' + '/' + str(args.inputMOVES).split('/')[-1])
        else:  # directory
            file_list_names = os.listdir(args.inputMOVES)  # get specified directory
            print('amounnt of files in the directory')
            print(len(file_list_names))  # the list of directories to double check
            for iter_file in file_list_names:  # iterate through all files inside of directory
                print(iter_file + 'loaded', end=' ')
                df_array.append(pd.read_csv(args.inputMOVES + '/' + iter_file, names=columns_list))
            df = pd.concat(df_array)
            df_analyzeobj = AI_File.CleanAndAnalyze(df)

        df_analyzeobj.clean()
        print('done loading files')
        print('After loading file head')

    if args.nineptlead is not None:
        print('Nine Point Lead stage')
#        df_analyzeobj.clean()
        df_analyzeobj.create_all_columns()
        print('finished nineptlead')
        print(df_analyzeobj.df.head())

    if args.graph is not None:
        visualize = 0
        while visualize != 6:
            print('graphing stage')
            print('1:simply describes the overall dataframe and prints it to console')
            print('2: creates a histogram from the current dataframe')
            print('3: linear regression, will need to enter a single feature, and a single target!')
            print(
                '4: multi var regression, must specify multiple features as csv! and the target should also be in csv format')
            print('5 is to show frequency of a submitted column name case sensitive:')
            print('6 is to quit the graphing phase and exit the program')
            visualize = input('1:describe, 2:histogram, 3:linear regression. 4:multi-var linear regression, 5 show frequency of entered column, and 6 is to break out of graph and exit')
            if int(visualize) == 1:
                print(df_analyzeobj.df.describe())
            elif int(visualize) == 2:
                df_analyzeobj.make_hist()
            elif int(visualize) == 3:
                df_analyzeobj.linear_regression()
            elif int(visualize) == 4:
                X = input('enter feature to set as the X: ')
                X = str(X).strip().split(',')
                y = input('enter target to set as y: ')
                y = str(y).strip().split(',')
                df_analyzeobj.multi_linear_reg(list(X), y)

            elif int(visualize) == 5:
                target = input('Please enter a column to show frequencies of: ')
                dict_nine = df_analyzeobj.group_mates(target)
                print(dict_nine)
            else:
                break

    if args.write is not None:
        print('writing dataframe to file')
        df_analyzeobj.df.to_csv(args.write)

    if args.inputPGN is not None:
        pgnObj = pgnParser.PGN_2_FEN(args.inputPGN)
        pgnObj.extract_data()
        game_list = pgnObj.game_list
        print('done loading pgn file')
        print('total amount of games in file: ' + str(len(game_list)))
        for item in game_list:
            item.convert_time()
            item.convert_moves()

        game = game_list[1]
        print(game.moves)
        print(game.times)


if __name__ == "__main__":
    main()
