import argparse
import pandas as pd
import ChessHandling
import os
import numpy as np
import AIF2JSON_MDv2 as aifToJson
import pgnParser


def main():
    print('hi')
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="increase output verbosity MOVES for now", type=str)
    parser.add_argument("--inputAIF", help="input AIF data, .png files", type=str)
    parser.add_argument("--inputPGN", help="input PGN data, .png files", type=str)
    parser.add_argument("--tenptlead",
                        help="calculate if player had 10pt lead and lost specify specify an int of any value to run this",
                        type=int)
    parser.add_argument('--write',
                        help='after everything write the dataFrame to file specified by name will write to local directory',
                        type=str)
    args = parser.parse_args()
    df = pd.DataFrame

    if args.input is not None:  # if input is none then really nothing to do
        temp = input('is this a directory(1) or a file(0)')
        if temp == 0:  # file
            df = pd.read_csv(args.input, names=columns_list)
        elif temp == 1:  # directory
            file_list_names = os.listdir(args.input)  # get specified directory
            np_array = []
            for file_ in file_list_names:
                print(file_ + '/t current file looking at')
                data_frame = pd.read_csv(args.input + '/' + file_,
                                         names=columns_list)  # make dataframe per file then combine them using a numpy array
                np_array.append(data_frame.values)  # attatch dataframe to numpy array

            df = pd.DataFrame(np.vstack(np_array), columns=columns_list)  # set df = to total

    if args.tenptlead is not None:
        df['TurnAround'] = df.apply(lambda row: ChessHandling.ten_point_calculate(row['FEN-Position'], row['Result']),
                                    axis=1)
        print(df['TurnAround'].tolist())
    if args.write is not None:
        df.to_csv(args.write)

    if args.inputAIF is not None:
        json = aifToJson.PickleAIF(args.inputAIF)
        print(json)

    if args.inputPGN is not None:
        game_list = pgnParser.PGN_2_FEN(args.inputPGN).extract_data()

        for i in list(game_list):
            print(i)


if __name__ == "__main__":
    main()
