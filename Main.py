import argparse
import pandas as pd
import ChessHandling
import os
import numpy as np
import pgnParser
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import datasets
from sklearn.linear_model import LinearRegression
import matplotlib as mpl
import matplotlib.pyplot as plt
import AI_File
import seaborn as sns

df = pd.DataFrame


# Example Run python3 Main.py --input/dir/.txt --tenptlead 1 --write/dir/filename.txt
def main():
    print('hi')
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputMOVES", help="input MOVES", dest='inputMOVES', type=str)
    parser.add_argument("--inputAIF", help="input AIF Path, .png files", dest='inputAIF', type=str)
    parser.add_argument("--inputPGN", help="input PGN Path, .png files", dest='inputPGN', type=str)
    parser.add_argument("--average", help="create average column", dest='average', type=int)
    parser.add_argument("--nineptlead", help="calculate if move had a 10pt diff with a loss", dest='nineptlead',
                        type=int)
    parser.add_argument("--graph", help="graph the current loaded dataframe", dest='graph', type=int)
    parser.add_argument('--write', help='specify path, it will be written as a csv', type=str, dest='write')
    parser.add_argument('--clean', help='clean file', type=int, dest='clean')
    parser.add_argument('--regression', help='start regression enter 1 for linear 2 logistic 3 polynomial regression',
                        dest='reg', type=int)
    args = parser.parse_args()
    df_analyzeobj = None  # when working with a single file use this
    df_array_analyze = []  # list of ai objects when working with a directory
    df_array = []  # raw dataframe list when working with a directory
    dirorfile = input('is this a directory(1) or a file(0)')

    if args.inputMOVES is not None:
        if int(dirorfile) == 0:  # file
            df_analyzeobj = AI_File.CleanAndAnalyze(pd.read_csv(args.inputMOVES, names=columns_list))
            print('loaded file' + '_' + '/' + str(args.inputMOVES).split('/')[-1])
            print('cleaned df')
        else:  # directory
            file_list_names = os.listdir(args.inputMOVES)  # get specified directory
            print('amounnt of files in the directory')
            print(len(file_list_names))  # the list of directories to double check
            for iter_file in file_list_names:  # iterate through all files inside of directory
                print(iter_file + '/t loaded', end=' ')
                df_array_analyze.append(AI_File.CleanAndAnalyze(pd.read_csv(args.inputMOVES + '/' + iter_file,
                                                                            names=columns_list)))  # putting the dataframe into AI object and storing it in a list
        print('done loading files')
        print('After loading file head')

    if args.nineptlead is not None:
        print('nine pt lead')
        input('you still there? Press enter ')
        if int(dirorfile) == 1:  # is this a directory?
            print('nineptlead loading')
            [x.nine_pt_lead() for x in df_array_analyze]
            print(str(len(df_array_analyze)) + 'the amount of files loaded and dataframes created')
        else:
            df_analyzeobj.nine_pt_lead()
        print('finished nineptlead')

    if args.graph is not None:
        print('graphing')
        visualize = input('1:describe, 2:histogram, 3:linear regression')
        if int(visualize) == 1:
            print(df_analyzeobj.df.describe())
        elif int(visualize) == 2:
            df_analyzeobj.clean_df()
            df_analyzeobj.make_hist()
        elif int(visualize) == 3:
            X = input('enter feature to set as the X')
            y = input('enter target to set as y')
            df_analyzeobj.linear_regression(X, y)
            plt.show()
        elif int(visualize) == 4:
            X = input('enter feature to set as the X')
            y = input('enter target to set as y')
            df_analyzeobj.linear_regression(X, y)
            plt.show()


    if args.write is not None:
        print('starting to write file')
        if dirorfile == 1:
            try:
                dir_write = input('Enter directory to create for the writing of df')
                os.mkdir(dir_write)
                [df.df.to_csv(dir_write) for df in df_array_analyze]
            except FileExistsError:
                print('the directory exists broooooo')
    else:
        df_analyzeobj.df.to_csv(args.write)

    if args.inputAIF is not None:
        file = args.inputAIF
        print(file)

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
