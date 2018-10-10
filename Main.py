import argparse
import pandas as pd
import ChessHandling


def main():
    print('hi')
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="increase output verbosity", type=str)
    parser.add_argument("--tenptlead",
                        help="calculate if player had 10pt lead and lost specify specify an int of any value to run this",
                        type=int)
    parser.add_argument('--write', help='after everything write the dataFrame to file specified by name will write to local directory', type=str)
    args = parser.parse_args()
    df = pd.DataFrame

    if args.input is not None:
        temp = input('is this a directory(1) or a file(0)')
        if temp == 0:
            df = pd.read_csv(args.input, names=columns_list)
        elif temp == 1:
            df = ChessHandling.load_multiple_files(args.input)
    if args.tenptlead is not None:
        df['Score'] = df['FEN-Position'].apply(ChessHandling.parse_fen)
        df['NoTie'] = df['Result'].apply(ChessHandling.parse_result)
        df['TurnAround'] = df.apply(ChessHandling.ten_point_lead_and_lost, axis=1)
        print(df['Score'])
        print(df['NoTie'])
        print(df['TurnAround'])

    if args.write is not None:
        df.to_csv(args.write)




if __name__ == "__main__":
    main()
