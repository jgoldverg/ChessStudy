import argparse
import pandas as pd
import ChessHandling
import os
import numpy as np
import AIF2JSON_MDv2 as aifToJson
import pgnParser
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
import AI_File
import matplotlib.pyplot as plt
import csv

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
    parser.add_argument("--tenptlead",
                        help="calculate if player had 10pt lead and lost specify specify an int of any value to run this, on current dataframe",
                        type=int, dest='tenptlead')
    parser.add_argument("--nineptlead", help="calculate if move had a 10pt diff with a loss", dest='nineptlead',
                        type=int)
    parser.add_argument("--graphDf", help="graph the current loaded dataframe", dest='graphDf', type=int)
    parser.add_argument('--write', help='specify path, it will be written as a csv', type=str, dest='write')
    parser.add_argument('--clean', help='clean file', type=int, dest='clean')
    args = parser.parse_args()
    df_analyzeObj = None

    if args.inputMOVES is not None:
        temp = input('is this a directory(1) or a file(0) ')
        if int(temp) == 0:  # file
            list = ChessHandling.read_file(args.inputMOVES)
            df = pd.read_csv(args.inputMOVES, names=columns_list)  # read the list returned from read_file()
            print('loaded file' + '_' + '/' + str(args.inputMOVES).split('/')[-1])
        else:  # directory
            file_list_names = os.listdir(args.inputMOVES)  # get specified directory
            np_array = []
            for file_ in file_list_names:
                temp = args.inputMOVES
                data_frame = pd.read_csv(temp + '/' + file_,
                                         names=columns_list)  # make dataframe per file then combine them using a numpy array
                print(file_ + '/t loaded', end=' ')
                np_array.append(data_frame.values)  # attatch dataframe to numpy array
            df = pd.DataFrame(np.vstack(np_array), columns=columns_list)  # set df = to total

        print('done loading files')
        df_analyzeObj = AI_File.CleanAndAnalyze(df)
        df_analyzeObj.clean_df()
        df_analyzeObj.convert_result_to_numeric()
        print('After loading file head')
        print(df_analyzeObj.df.head())
#        feature_str = input('Enter features you would like to graph as csv')
 #       list_feature = feature_str.strip().split(',')
#        target_str = input('What are you trying to study? give me a target cause me hungry!!!')
  #      target_str.strip()
   #     df = df.fillna
    #    list_target = target_str.split(',')
     #   df_analyzeObj.graph_cols(list_feature, list_target)

    # if the TurnAround column is not writing to file then it is full of NaN as in those elements were not populated
    if args.tenptlead is not None:
        np_arr = np.array
        np_arr = df.apply(lambda row: ChessHandling.ten_point_calculate(row['FEN-Position'], row['Result']),
                          axis=1)  # this method returns the string white black or empty
        df['TurnAround'] = np_arr

    if args.nineptlead is not None:
        print('nine pt lead')
        df_analyzeObj.nine_pt_lead()

    if args.write is not None:
        file = args.write
        df_analyzeObj.df.to_csv(file)

    if args.inputAIF is not None:
        file = args.inputAIF
        json = aifToJson.PickleAIF(file)
        print(json)

    if args.inputPGN is not None:
        pgnObj = pgnParser.PGN_2_FEN(args.inputPGN)
        pgnObj.extract_data()
        game_list = pgnObj.game_list
        print('done loading pgn file')
        print('total amount of games in file: ' + str(len(game_list)))
        [item.convert_moves() for item in game_list]
        [item.convert_time() for item in game_list]
        game = game_list[0]


if __name__ == "__main__":
    main()
