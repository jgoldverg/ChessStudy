import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random as rnd


class CleanAndAnalyze(object):
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    z_dictionary = {}

    def __init__(self, df):
        self.df = pd.DataFrame(df)  # need to create the dataframe to process before dont need to clean
        self.elems_game_start = []
        self.df_relevant = pd.DataFrame
        self.rating_group_dict_to_z = {}

    def clean(self):  # cleaning method, it takes away all of the line information and drops them
        arr = np.array(self.df['FEN-Position'].tolist())
        arr_games = []
        indexs = []
        game_count = 0
        for idx, row in self.df.iterrows():
            if str(row['FEN-Position']).__contains__('#'):
                game_count += 1
                indexs.append(idx)
                self.elems_game_start.append({row['FEN-Position'], arr[idx + 1]})
                arr_games.append(game_count)
            else:
                arr_games.append(game_count)

        self.df['NewGame'] = np.array(arr_games)
        self.drop_extra(indexs)
        print('size of cleaned df is ' + str(self.df['FEN-Position'].size))
        print(self.df.head())

    def drop_extra(self, indexs_to_drop):
        self.df.drop(self.df.index[indexs_to_drop], inplace=True, axis=0)
        self.df.drop(['#times', 'E', 'EMove', 'MovePlayed', 'ValueDifference'], inplace=True, axis=1)
        self.df.dropna(inplace=True)

    def group_games(self):
        new_game_col = self.df['NewGame'].values.tolist()
        new_game_np = np.array(new_game_col)

    def create_all_columns(self):
        # slowest way to iterate over a dataframe but it makes sense currently
        average_rating = []  # this is the average rating but skewed to be more of a group
        loc = []  # length of checkmate
        nine_pt_lead = []
        rating_group = []
        for idx, row in self.df.iterrows():
            if pd.isna(row['WhiteR']):
                print('dropping this row')
                print(row['FEN-Position'])
                self.df.drop(row, inplace=True)
            average_rating.append(self.average_rating(row['WhiteR'], row['BlackR']))
            loc.append(self.y_length_of_checkmate(row))
            nine_pt_lead.append(self.nine_enhanced(row))
            rating_group.append(self.rating_group(row['WhiteR'], row['BlackR']))

        self.df['NinePtLead'] = nine_pt_lead
        self.df['AverageRating'] = average_rating
        self.df['Rating_Group'] = rating_group
        self.df['length_of_checkmate'] = loc

    def average_rating(self, white, black):  # Average rating to 25
        avg = (float(white) + float(black)) / 2
        return int(round(avg / 25) * 25)

    def rating_group(self, white, black):
        avg = float(white) + float(black)
        avg = avg / 2
        return int(round(avg) / 200) * 200

    # creating two columns nineptlead column and the average rating column, taking the average of the row and rounding to the highest multiple of 25
    # def nine_pt_lead_and_average_rating(self):
    #     # calculate the average rating of every single line
    #     self.df['AverageRating'] = self.df.apply(lambda row: self.average_rating(row['WhiteR'], row['BlackR']), axis=1)
    #     # apply calc_nine_pt_lead to every single row of the dataframe
    #     self.df['NinePtLead'] = self.df.apply(lambda row: self.nine_pt_lead(row), axis=1)
    #     # calculate the length of checkmate every single row of the dataframe
    #     self.df['length_of_checkmate'] = self.df.apply(lambda row: self.y_length_of_checkmate(row), axis=1)
    #     print(self.df.head())  # print the head everytime so i know it hasnt frozen

    # takes in move value played engine move value and result
    # EMV -- engine move value
    # result column 0-1, 1-0, 1/2
    def nine_pt_lead(self, row):
        EMV = int(row['EMV'])
        result = str(row['Result'])
        if (EMV >= 10000) or (EMV <= -10000):
            if result == '1/2-1/2':
                return 'mate'
            elif result == '0-1' and EMV > 0:
                return 'choked'
            elif EMV < 0 and result == '1-0':
                return 'choked'
            else:
                return 'mate'
        elif (901 < EMV < 10000) or (-901 > EMV > -10000):
            return 'weird'
        else:
            return 'useless'

    def nine_enhanced(self, row):
        EMV = int(row['EMV'])
        result = str(row['Result'])
        if EMV >= 90000 and result != '1-0' or EMV <= -90000 and result != '0-1':
            return 'missedMate'
        elif EMV >= 900 and result != '1-0' or EMV <= -900 and result != '0-1':
            return 'lostBigLead'
        else:
            return 'useless'

    def y_length_of_checkmate(self, row):
        EMV = int(row['EMV'])
        if abs(EMV) >= 99000:
            return 100000-abs(EMV)
        else:
            return 0

    # grouping function for  class specific dataframe
    def group_mates(self, target):  # the way i see it is every emv can be grouped together by a variance of 30
        nine_group = self.df[str(target)].value_counts().to_dict()
        return nine_group

    # make a hist passing the method to a list
    def make_hist(self):
        # self.df.plot.hist() #local copy cant run on metallica
        print(self.df.head())
        col_hist = input('Enter column to do histogram of: ')
        plt.hist(self.df[col_hist])
        plt.xlabel(input('x-label'))
        plt.ylabel(input('Enter y label'))
        plt.title(input('Enter Title Name for this Histogram!'))
        self.save('histogram_nineptlead')

    # This returns a list of relelvant rows to the current program so where ever there is a value
    def create_relevant_list(self):
        index_drop = self.df[self.df['length_of_checkmate'] == 0].index
        self.df.drop(index_drop, inplace=True)

    #
    def make_z(self):
        temp = self.df[self.df['length_of_checkmate'] > 0]
        x = temp['Rating_Group'].value_counts().to_dict()
        y = temp['length_of_checkmate'].value_counts().to_dict()
        z = temp[ temp['NinePtLead'] == 'choked'] #all positions where the player choked and had a length of checkmate greater than 0
        print(pd.crosstab(temp['Rating_Group'].values, temp['length_of_checkmate'].values))
        print(y)
        print(temp.groupby(['Rating_Group', 'length_of_checkmate']))

    # single var regression of specified feature and target will get from user input
    def linear_regression(self):
        self.create_relevant_list()
        self.make_z()
        print(self.df.head())
#        lm = LinearRegression().fit(X = self.df[])

        print('end of linear regression')

    # multi var linear regression
    def multi_linear_reg(self, feature, target):
        X = self.df[feature]
        y = self.df[target]
        lm = LinearRegression()
        lm.fit(X, y)
        predictions = lm.predict(y)
        plt.scatter(X, predictions)
        plt.title(feature + ' ' + target)
        plt.xlabel(feature)
        plt.ylabel(target)
        name = input('file name: ')
        self.save(name + 'multilinearreg')

    # function needed for metallica
    def save(self, name):
        name = name.strip()
        plt.savefig(name + '.png')

    def get_train_test_inds(self, y, train_proportion=0.7):
        '''Generates indices, making random stratified split into training set and testing sets
        with proportions train_proportion and (1-train_proportion) of initial sample.
        y is any iterable indicating classes of each observation in the sample.
        Initial proportions of classes inside training and
        testing sets are preserved (stratified sampling).
        '''
        y = np.array(y)
        train_inds = np.zeros(len(y), dtype=bool)
        test_inds = np.zeros(len(y), dtype=bool)
        values = np.unique(y)
        for value in values:
            value_inds = np.nonzero(y == value)[0]
            np.random.shuffle(value_inds)
            n = int(train_proportion * len(value_inds))

            train_inds[value_inds[:n]] = True
            test_inds[value_inds[n:]] = True

        return train_inds, test_inds
