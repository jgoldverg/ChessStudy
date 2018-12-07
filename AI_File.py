import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
# matplotlib.use('Agg')

from sklearn import datasets
import ChessHandling
import time


class CleanAndAnalyze(object):
    result_options = {'1/2': 0, '0-1': -1, '1-0': 1}

    def __init__(self, df):
        self.df = pd.DataFrame(df)
        self.elems_game_start = []

    def convert_result_to_numeric(self):
        result_converted = self.df['Result'].map(self.result_options).tolist()
        self.df.drop(['Result'], axis=1, inplace=True)
        result_conv_series = pd.Series(result_converted)
        self.df['Result'] = result_conv_series

    def clean_df(self):
        fen_clean = np.array(self.df['FEN-Position'].tolist())
        for idx, elem in enumerate(fen_clean):
            if str(fen_clean[idx]).__contains__('#'):
                self.elems_game_start.append({idx, elem})
                self.df.drop(idx, inplace=True)

    def nine_pt_lead(self):
        self.df['NinePtlead'] = self.df.apply(
            lambda row: self.__nine_pt_calculate(row['MovePlayedValue'], row['Result']), axis=1)
        print(self.df.head())

    def __nine_pt_calculate(self, move_value_played, result):
        if str(result).__contains__(';'):
            return 2.5  # dummy value
        elif move_value_played > 900 and result.__eq__('0-1'):
            return -1  # black
        elif move_value_played < -900 and result.__eq__('1-0'):
            return 1  # white
        else:
            return 0  # whatever

    def _frequency_of_missed_check_mates(self):
        self.clean_df()
        X_train, X_test, y_train, y_test = train_test_split(np.array(self.df['EMV']).reshape(-1, 1),
                                                            self.df['NinePtlead'].tolist(), test_size=0.4,
                                                            random_state=101)
        lm = LinearRegression()
        lm.fit(X_train, y_train)
        predictions = lm.predict(X_test)
        plt.scatter(y_test, predictions)
        plt.show()

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
        print('EMV white: ' + str(average_white_emv) + ' white average is: ' + str(average_black_emv))
        print('MoveValuePlayed white: ' + str(average_white_mvp) + ' black: ' + str(average_black_mvp))
        return [{average_white_emv, average_white_mvp}, {average_black_emv, average_black_mvp}]

    def graph_(self, feature, target):
        self.clean_df()
        X = np.array(self.df[str(feature)])
        y = np.array(self.df[str(target)])
        X_test, X_train, y_train, y_test = train_test_split(X, y)
        print('split data')
        model = LinearRegression()
        model.fit(X_train, y_train)
        print('ran fit')
        print('model score on given data:' + str(model.score(X_test, y_test)))

        # plot a line, a perfit predict would all fall on this line

    def group_emv(self):  # the way i see it is every emv can be grouped together by a variance of 30
        grouped = self.df.groupby(['EMV', 'MoveValuePlayed'])

    def make_hist(self):
        self.df.plot.hist()
        name = input('enter name for histogram: ')
        self.save(name)

    def linear_regression(self, feature, target):
        self.clean_df()
        X = pd.to_numeric(self.df[str(feature)])
        y = pd.to_numeric(self.df[str(target)])
        X_train, X_test, y_train, y_test = train_test_split(np.array(X).reshape(-1, 1), y, test_size=0.4, random_state=101)
        lm = LinearRegression()
        lm.fit(X_train, y_train)
        predictions = lm.predict(X_test)
        plt.scatter(y_test, predictions)
        plt.xlabel(feature)
        plt.ylabel(target)
        name = input('file name: ')
        self.save(name)

    def save(self, name):
        plt.savefig(name)
