import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random as rnd


class CleanAndAnalyze(object):
    columns_list = ["FEN-Position", "Result", "WhiteR", "BlackR", "EMV", "MovePlayed"]
    z_dictionary = {}

    def __init__(self, df):
        self.df = pd.DataFrame(df)  # need to create the dataframe to process before dont need to clean
        self.elems_game_dict = {}
        self.rating_group_dict_to_z = {}
        self.length_mate_frequencies = {4: 0, 5: 0, 7: 0, 9: 0, 11: 0, 15: 0}

    def clean(self):  # cleaning method, it takes away all of the line information and drops them
        print('cleaning/preparing df: ')
        self.df.dropna(inplace=True, axis=0)
        arr_games = []
        indexs = []
        game_count = 0
        loc = []  # length of checkmate
        nine_pt_lead = []
        rating_group = []
        loc_grouped = []
        for idx, row in self.df.iterrows():
            if str(row['FEN-Position']).__contains__('#') or str(row['FEN-Position']).__contains__(';'):
                game_count += 1
                indexs.append(idx)  # store idx
                print(str(row['FEN-Position']))
                self.elems_game_dict[game_count] = str(row['FEN-Position'])
                arr_games.append(game_count)
                # this should only be checking the FEN-Position but a bug in file AA1650 stored the #/and ; in a different row segment had to do this long check
            else:
                loc.append(self.length_of_checkmate(row))
                loc_grouped.append(int(self.loc_group_column(loc[-1])))
                nine_pt_lead.append(self.nine_enhanced(row))
                rating_group.append(self.rating_group(row['WhiteR'], row['BlackR']))

            arr_games.append(game_count)
        self.df['Game'] = arr_games #index of game in the file
        self.df.drop(self.df.index[indexs], inplace=True)
        self.df['NinePtLead'] = nine_pt_lead
        self.df['Rating_Group'] = rating_group
        self.df['length_of_checkmate'] = loc
        self.df['loc_group'] = loc_grouped
        print('\n' + 'size of cleaned df is ' + str(self.df['FEN-Position'].size))
        print(self.df.head())

    # This method is a function more or less, meant to be called from .apply but using a loop instead same with the few methods below that just create columns the extra bloat aint great
    def rating_group(self, white, black):
        avg = (float(white) + float(black))/2
        return round(avg / 25) * 25

    # takes in move value played engine move value and result
    # EMV -- engine move value
    # result column 0-1, 1-0, 1/2
    def nine_enhanced(self, row):
        EMV = int(row['EMV'])
        result = str(row['Result'])
        if EMV >= 90000 and result != '1-0' or EMV <= -90000 and result != '0-1':
            return 2
        elif EMV >= 900 and result != '1-0' or EMV <= -900 and result != '0-1':
            return 1
        else:
            return 0

    # calculate the length of checkmate column for that row supplied
    def length_of_checkmate(self, row):
        EMV = int(row['EMV'])
        if abs(EMV) >= 99000:
            return 100000 - abs(EMV)
        else:
            return 0

    # This calculates out loc_group column value and is my groups esentially for the real length_of_checkmate
    def loc_group_column(self, loc):
        if loc == 0:
            return 0
        elif 4 > loc > 0:
            return 4
        elif 6 > loc > 3:
            return 5
        elif 9 > loc > 5:
            return 7
        elif 11 > loc > 8:
            return 9
        elif 16 > loc > 10:
            return 11
        elif 20 > loc > 15:
            return 15
        else:
            return 20

    # make a hist passing the method to a list
    def make_hist(self, column):
        # self.df.plot.hist() #local copy cant run on metallica
        print(self.df.head())
        t = str(input('To look at MissedMate:2, lostBigLead:1, useless:0, or just press enter for full df'))
        if t != '':
            x = self.df[self.df['NinePtLead'] == int(t)]
            plt.hist(x[column])
        else:
            plt.hist(self.df[column])

        plt.xlabel(input('Enter x axis label:'))
        plt.ylabel(input('Enter y axis label:'))
        plt.title(input('Enter title for graph: '))
        self.save()

    def game_analysis(self):
        data = self.df[self.df['NinePtLead'] == 'missedMate']
        self.df.groupby('Game')

    # NinePtLead code: 
    # 0 == move in a game such that the move is not a big lead, OR it is a big lead and the player won.
    # 1 == move in a game where player had a big lead (not forced mate) but did not win the game.
    # 2 == move in a game where player had a forced checkmate but did not win the game.
    # 
    # This z rating that is working of y against z regression
    # Returns a pair of NumPy arrays [bucket_ratings], [frequency of (1 or 2) relative to all moves].
    def rating_frequency_calculate(self):
        ninptlead_rating_group = self.df[['NinePtLead', 'Rating_Group']]

        (denominator_keys, denominator_freq) = np.unique(ninptlead_rating_group['Rating_Group'], return_counts=True)
        # returns pair of arrays; note that second array are absolute counts, not yet frequencies

        numerator_keys, numerator_freq = np.unique(ninptlead_rating_group[ninptlead_rating_group['NinePtLead'] != 0]['Rating_Group'], return_counts=True)

        denominator_dict = dict(zip(denominator_keys, denominator_freq))
        numerator_dict = dict(zip(numerator_keys, numerator_freq))
        for i in denominator_dict.keys():
            if i not in numerator_dict.keys():
                numerator_dict[i] = 0
        numerator = np.array(np.fromiter(numerator_dict.values(), dtype=np.float64))
        denominator = np.array(np.fromiter(denominator_dict.values(), dtype=np.float64))
        print(numerator_dict)
        print(denominator_dict)
        z = numerator/denominator   # array op
        print(z)
        return [denominator_keys, z]

    # This is the z rating for x against z
    def length_of_checkmate_frequency(self):
        data = self.df[self.df['NinePtLead'] == 2]
        numerator_x, numerator_freq = np.unique(data['loc_group'], return_counts=True)
        denominator_y, denominator_freq = np.unique(list(self.df['loc_group']), return_counts=True)
        print(numerator_x, numerator_freq)
        print(denominator_y, denominator_freq)
        denominator_y = np.delete(denominator_y, [0])  # delete chomps off initial 0 for no-checkmate
        denominator_freq = np.delete(denominator_freq, [0])
        z = numerator_freq/denominator_freq
        return [denominator_y, z]

    def multi_reg(self):
        z_loc = self.length_of_checkmate_frequency()
        z_rating = self.rating_frequency_calculate()
        lm = LinearRegression()
        lm.fit(X=self.df[['Rating_Group', 'loc_group']], y= self.df['NinePtLead'])
        #plt.scatter(X= z_loc[0], ))

    # this is the first method to use linear regression, this one makes a graph frequency of length of checkmate
    def linear_regression(self, t):
        print(self.df.head())
        z = self.length_of_checkmate_frequency()
        if int(t) == 1:
            z = self.rating_frequency_calculate()
        lm = LinearRegression()
        x = np.array(z[0]).reshape(-1, 1)
        y = np.array(z[1]).reshape(-1, 1)
        print(x)
        print(y)
        lm.fit(X=x, y=y)
        pred = lm.predict(X=np.array(z[0]).reshape(-1,1))
        plt.scatter(z[0], z[1])
        plt.plot(z[0], pred, color='green', linewidth='3')
        plt.xlabel(input('xlabel'))
        plt.ylabel(input('ylabel'))
        plt.title(input('enter title for graph"'))
        self.save()
        print('end of linear regression')


    def multi_regression(self):
        z_rating = self.rating_frequency_calculate()
        z_rating = self.length_of_checkmate_frequency()
        no_nine = self.df[self.df['NinePtLead' == 2]]['Rating_Group', 'loc_group', 'NinePtLead']
        lm = LinearRegression()
        lm.fit(X=np.unique(np.array(self.df[['Rating_Group', 'loc_group', 'NinePtLead']])), y=np.array(no_nine['NinePtLead']).reshape(-1,1))
        lm.predict(np.unique(np.array(self.df[['Rating_Group', 'loc_group', 'NinePtLead']])))

    # save the current plot call after every time u plot to close and ping for filename
    def save(self):
        name = input('Enter name for file, sorry if this is the second time:')
        name = name.strip()
        plt.savefig(name + '.png', bbox_inches="tight")
        plt.close()

    # dumb ignore more of a reference
    def other_z(self):
        rows_lost = self.df[self.df['length_of_checkmate'] != 0]  # rows that dont have a checkmate at that position
        missed_mates = rows_lost[rows_lost['NinePtLead'] == 2]  # get all missed checkmates
        numerator = missed_mates[missed_mates['length_of_checkmate'] > 0]
        ratings = np.array(numerator['Group_Rating'])
        ratings = np.unique(ratings, return_index=True)
        print(ratings)
        denominator = self.df[self.df['length_of_checkmate'] > 0]  # get all mate value moves and group by the group_rating which returns a series of frequency
        print(denominator)
        z = numerator / denominator
        return z

    def write_nineptlead_moves(self, name):
        temp = self.df[self.df['NinePtLead'] == 2]
        temp.to_csv(name, header=False)
