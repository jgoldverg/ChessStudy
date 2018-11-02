import argparse
import pandas as pd
import ChessHandling
import os
import numpy as np
import AIF2JSON_MDv2 as aifToJson
import pgnParser
import csv


def main():
    print('hi')
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="increase output verbosity MOVES for now", dest='input', type=str)
    parser.add_argument("--inputAIF", help="input AIF data, .png files", dest='inputAIF', type=str)
    parser.add_argument("--inputPGN", help="input PGN data, .png files", dest='inputPGN', type=str)
    parser.add_argument("--tenptlead",
                        help="calculate if player had 10pt lead and lost specify specify an int of any value to run this",
                        type=int, dest='tenptlead')
    parser.add_argument('--write',
                        help='specify path, it will be written as a csv',
                        type=str, dest='write')
    args = parser.parse_args()
    df = pd.DataFrame

    if args.input is not None:
        temp = input('is this a directory(1) or a file(0) ')
        if int(temp) == 0:  # file
            list = ChessHandling.read_file(args.input)
            df = pd.read_csv(args.input, names=columns_list)  # read the list returned from read_file()
            print('loaded file')
        elif int(temp) == 1:  # directory
            file_list_names = os.listdir(args.input)  # get specified directory
            np_array = []
            for file_ in file_list_names:
                temp = args.input
                data_frame = pd.read_csv(temp + '/' + file_,
                                         names=columns_list)  # make dataframe per file then combine them using a numpy array
                print(file_ + '/t loaded', end=' ')
                np_array.append(data_frame.values)  # attatch dataframe to numpy array

            df = pd.DataFrame(np.vstack(np_array), columns=columns_list)  # set df = to total
            print(df)

    if args.tenptlead is not None:
        df['TurnAround'] = df.apply(lambda row: ChessHandling.ten_point_calculate(row['FEN-Position'], row['Result']),
                                    axis=1)
        print(df)

    if args.write is not None:
        file = args.write
        df.to_csv(file)

    if args.inputAIF is not None:
        file = args.inputAIF
        json = aifToJson.PickleAIF(file)
        print(json)

    if args.inputPGN is not None:
        game_list = pgnParser.PGN_2_FEN(args.inputPGN).extract_data()
        [game.convert_moves() for game in game_list]
        [game.convert_time() for game in game_list]
        game = game_list[0]
        print(game.moves)

if __name__ == "__main__":
    main()
