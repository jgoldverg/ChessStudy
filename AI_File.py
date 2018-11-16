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
        print('hello')
        self.df['Result'] = result_conv_series

    def clean_df(self):
        fen_clean = np.array(self.df['FEN-Position'].tolist())
        print('starting cleaning of dataframe post loading')
        for idx, elem in enumerate(fen_clean):
            if str(fen_clean[idx]).__contains__('#'):
                self.elems_game_start.append({idx, elem})
                self.df.drop(idx, inplace=True)
        print(len(self.elems_game_start))

    def graph_cols(self, feature, target):
        print(feature)
        print(type(feature))
        print(target)
        return

    def nine_pt_lead(self):
        self.df['NinePtlead'] = self.df.apply(lambda row: self.__nine_pt_calculate(row['MovePlayedValue'], row['Result']), axis=1)
        print(self.df.head())

    def __nine_pt_calculate(self, move_value_played, result):
        if str(result).__contains__(';'):
            return -1000
        elif move_value_played > 900 and result == -1.0:
            return 'black'
        elif move_value_played < -900 and result == 1.0:
            return 'white'
        else:
            return 'd.c'

#        list_feature = str(feature).split(',')
#
 #       for item in list_feature:
  ##     print('shape of X' + str(X.shape) + 'shape of y' + str(y.shape))
#        X_test, X_train, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)
 #       print('split data')
  #      model = LinearRegression()
   #     model.fit(X_train, y_train)
    #    print('ran fit')
     #   print('model score on given data:' + str(model.score(X_test, y_test)))
      #  y_pred = model.predict(X_test)
       # print('predicted data')
        #y_pred = model.predict(X_test)
        #plt.plot(y_test, y_pred, '.')

        # plot a line, a perfit predict would all fall on this line
        #x = np.linspace(0, 330, 100)
        #y = x
        #plt.plot(x, y)
        #plt.show()
