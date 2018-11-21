import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
from sklearn import datasets
import ChessHandling


class CleanAndAnalyze(object):
    result_options = {'1/2': 0, '0-1': -1, '1-0': 1}

    def __init__(self, df):
        self.df = pd.DataFrame(df)
        self.elems_game_start = []

    def convert_result_to_numeric(self):
        result_converted = self.df['Result'].map(self.result_options).tolist()
        self.df.drop(['Result'], axis=1, inplace=True)
        result_conv_series = pd.Series(result_converted)
        print('hello converting to numeric')
        self.df['Result'] = result_conv_series

    def clean_df(self):
        fen_clean = np.array(self.df['FEN-Position'].tolist())
        print('starting cleaning of dataframe post loading')
        for idx, elem in enumerate(fen_clean):
            if str(fen_clean[idx]).__contains__('#'):
                self.elems_game_start.append({idx, elem})
                self.df.drop(idx, inplace=True)
        print(len('total new game lines: ' + str(len(self.elems_game_start))))

    def nine_pt_lead(self):
        print('nineptlead')
        self.df['NinePtlead'] = self.df.apply(
            lambda row: self.__nine_pt_calculate(row['MovePlayedValue'], row['Result']), axis=1)
        print(self.df.head())

    def __nine_pt_calculate(self, move_value_played, result):
        if str(result).__contains__(';'):
            return '-1000'
        elif move_value_played > 900 and result.__eq__('0-1'):
            return 'black'
        elif move_value_played < -900 and result.__eq__('1-0'):
            return 'white'
        else:
            return 'd.c'

    def average_calculate(self):
        move_col = []
        white_emv = []
        black_emv = []
        white_mvp = []
        black_mvp = []
        for idx, row in self.df.iterrows():
            current = row['EMV']
            turn = str(row['FEN-Position']).split(' ')[1]
            if idx > 1:
                if idx % 2 == 0 and turn == 'b':  # this means black move bc white always has first move aka odd numbers black being even
                    black_emv.append(row['EMV'])
                    black_mvp.append(row['MovePlayedValue'])
                else:  # for white when idx is odd
                    white_emv.append(row['EMV'])
                    white_mvp.append(row['MovePlayedValue'])
        black_np_mvp = np.array(black_mvp)
        white_np_mvp = np.array(white_mvp)
        black_arr = np.array(black_emv)
        white_arr = np.array(white_emv)
        average_black_emv = black_arr.mean()
        average_white_emv = white_arr.mean()
        average_black_mvp = black_np_mvp.mean()
        average_white_mvp = white_np_mvp.mean()
        print('EMV white: '+ str(average_white_emv) + ' white average is: ' + str(average_black_emv))
        print('MoveValuePlayed white: '+ str(average_white_mvp) + ' black: ' + str(average_black_mvp))

    def graph_input(self, feature, target):
        X = np.array(self.df[str(feature)])
        y = np.array(self.df[str(target)])
        plt.plot(X, y)
        print(X)
        print(y)
        X_test, X_train, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)
        print('split data')
        model = LinearRegression()
        model.fit(X_train, y_train)
        print('ran fit')
        print('model score on given data:' + str(model.score(X_test, y_test)))
        y_pred = model.predict(X=X_test)
        plt.plot(y_test, y_pred, '.')

        # plot a line, a perfit predict would all fall on this line
        x = np.linspace(0, 330, 100)
        y = x
        plt.plot(x, y)
        plt.show()
