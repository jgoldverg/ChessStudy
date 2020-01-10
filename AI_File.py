import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
import matplotlib
from collections import Counter

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random as rnd

class CleanAndAnalyze(object):
    columns_list = ["FEN-Position", "#times", "Result", "WhiteR", "BlackR", "E", "EMove", "EMV", "MovePlayed",
                    "MovePlayedValue", "ValueDifference"]
    z_dictionary = {}

    def __init__(self, df):
        self.df = pd.DataFrame(df)  # need to create the dataframe to process before dont need to clean
        self.elems_game_dict = {}
        self.rating_group_dict_to_z = {}
        self.length_mate_frequencies = {4: 0, 5: 0, 7: 0, 9: 0, 11: 0, 15: 0}
        self.amount_of_games = 0


    def clean(self):  # cleaning method, it takes away all of the line information and drops them
        print('cleaning/preparing df: ')
        game_counter_list = []
        game_count = 0
        loc = []  # length of checkmate
        nine_pt_lead = []
        rating_group = []
        loc_grouped = []
        for idx, row in self.df.iterrows():
            fen = str(row['FEN-Position']).strip()
            if fen.startswith('#') or fen.__contains__(';'):
                game_count += 1
                self.elems_game_dict[game_count] = fen
                print(str(game_count) + ' :' + fen)
            elif list(pd.notna(row)).__contains__(False):
                print('null hahahahahahahahaha-----------------------')
            else:
                nine_pt_lead.append(self.nine_enhanced(row))
                rating_group.append(self.rating_group_create(row['WhiteR']))
                loc.append(self.length_of_checkmate_create(row))
                loc_grouped.append(self.loc_group_column(loc[-1]))
            game_counter_list.append(game_count)
        self.amount_of_games = game_count
        self.df['Game'] = game_counter_list  # index of game in the file
        self.df.dropna(inplace=True, axis=0)
        self.df['NinePtLead'] = nine_pt_lead
        self.df['Rating_Group'] = rating_group
        self.df['length_of_checkmate'] = loc
        self.df['loc_group'] = loc_grouped
        print('\n' + 'size of cleaned df is ' + str(self.df['FEN-Position'].size))
        print(self.df.head())

    # This method is a function more or less, meant to be called from .apply but using a loop instead same with the few methods below that just create columns the extra bloat aint great
    def rating_group_create(self, white_rating):
        val = isinstance(white_rating, str)
        if isinstance(white_rating, str):
            return
        return round(white_rating / 25) * 25

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
    def length_of_checkmate_create(self, row):
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

    def rating_to_found_checkmate(self):
        ratings = np.unique(self.df['Rating_Group'])
        rating_to_found_mates = dict.fromkeys(np.fromiter(ratings, dtype=np.float64), 0)
        rating_all_mates = rating_to_found_mates
        for idx, row in self.df[['Rating_Group', 'EMV', 'NinePtLead', 'MovePlayedValue']].iterrows():
            if abs(int(row['EMV'])) >= 10000 and abs(int(row['MovePlayedValue'])) >= 10000:
                rating_to_found_mates[row['Rating_Group']] += 1
            if row['EMV'] >= 80000:
                #there is a checkmate not sure if found or not found tho.
                rating_all_mates[row['Rating_Group']] += 1
        numerator = np.array(np.fromiter(rating_to_found_mates.values(), dtype=np.float64))
        denominator = np.array(np.fromiter(rating_all_mates.values(), dtype=np.float64))
        print(numerator/denominator)
        return [ratings, numerator/denominator]

    # make a hist passing the method to a list
    def make_hist(self, t):
        print(self.df.head())
        plt.hist(self.df[t])
        plt.xlabel(t)
        plt.ylabel('Count')
        plt.title(input('Enter title for graph: '))
        self.save()
    
    def make_hist_no_zero(self, t):
        plt.hist(self.df[t][self.df[t] > 0], color="grey")
        plt.xlabel(t)
        plt.ylabel('Count')
        plt.title(input('Enter title for graph: '))
        self.save()

    # NinePtLead code:
    # 0 == move in a game such that the move is not a big lead, OR it is a big lead and the player won.
    # 1 == move in a game where player had a big lead (not forced mate) but did not win the game.
    # 2 == move in a game where player had a forced checkmate but did not win the game.
    # 
    # This z rating that is working of y against z regression
    # Returns a pair of NumPy arrays [bucket_ratings], [frequency of (1 or 2) relative to all moves].
    def ratings_to_game_counts(self):
        rating_keys = np.unique(self.df['Rating_Group']).tolist()
        rating_move_count_all = {}
        rating_missed_mate_counter = {}
        for idx, row in self.df[['Rating_Group', 'Game', 'NinePtLead']].iterrows():  # looping through relevant data
            current_rating = int(row['Rating_Group'])
            nine_pt_lead = int(row['NinePtLead'])
            if not rating_move_count_all.__contains__(current_rating):
                rating_missed_mate_counter[current_rating] = 0
                rating_move_count_all[current_rating] = 0
            elif rating_move_count_all.__contains__(current_rating) and (nine_pt_lead == 1 or nine_pt_lead == 0):
                #all other moves
                rating_move_count_all[current_rating] += 1
            if nine_pt_lead == 2:
                #missed mate and lost
                rating_missed_mate_counter[current_rating] += 1
        missed_mate_numerator = np.array(np.fromiter(rating_missed_mate_counter.values(), dtype=np.float64))
        all_denominator = np.array(np.fromiter(rating_move_count_all.values(), dtype=np.float64))
        return [rating_keys, (missed_mate_numerator / all_denominator)]

    def ratings_to_game_counts_old(self):
        rating_keys = np.unique(self.df['Rating_Group'])
        rating_game_count_all = dict.fromkeys(np.fromiter(rating_keys, dtype=np.float64), 0)
        previous_game = -1
        rating_missed_mate_counter = rating_game_count_all
        for idx, row in self.df[['Rating_Group', 'Game', 'NinePtLead']].iterrows():  # looping through relevant data
            game_count = int(row['Game'])
            missed_mate_in_game = False
            current_rating = int(row['Rating_Group'])
            nine_pt_lead = int(row['NinePtLead'])
            if game_count != previous_game:
                rating_game_count_all[current_rating] += 1
                previous_game = game_count
            if nine_pt_lead == 2 and not missed_mate_in_game:
                rating_missed_mate_counter[current_rating] += 1
        missed_mate_numerator = np.array(np.fromiter(rating_missed_mate_counter.values(), dtype=np.float64))
        all_denominator = np.array(np.fromiter(rating_game_count_all.values(), dtype=np.float64))
        return [np.unique(self.df['Rating_Group']), missed_mate_numerator / all_denominator]

    def rating_frequency_calculate(self):
        ninptlead_rating_group = self.df[['NinePtLead', 'Rating_Group']]
        (denominator_keys, denominator_freq) = np.unique(ninptlead_rating_group['Rating_Group'], return_counts=True)
        (numerator_keys, numerator_freq) = np.unique(ninptlead_rating_group[ninptlead_rating_group['NinePtLead'] != 0]['Rating_Group'], return_counts=True)
        denominator_dict = dict(zip(denominator_keys, denominator_freq))
        numerator_dict = dict(zip(numerator_keys, numerator_freq))
        for i in denominator_dict.keys():
            if i not in numerator_dict.keys():
                numerator_dict[i] = 0
        numerator = np.array(np.fromiter(numerator_dict.values(), dtype=np.float64))
        denominator = np.array(np.fromiter(denominator_dict.values(), dtype=np.float64))
        z = numerator / denominator  # array op
        return [denominator_keys, z]

    def lengthCheckMatesSeenAndNotSeen(self):
        checkmates = self.df[self.df['EMV'] > 90000]
        rows_checkmates = checkmates['Rating_Group', 'loc_group']
        rating_group = np.unique(self.df['Rating_Group'])

    # This is the z rating for x against z
    def length_of_checkmate_frequency(self):
        data = self.df[self.df['NinePtLead'] == 2]
        numerator_x, numerator_freq = np.unique(data['loc_group'], return_counts=True)
        denominator_y, denominator_freq = np.unique(list(self.df['loc_group']), return_counts=True)
        denominator_y = np.delete(denominator_y, [0])  # delete chomps off initial 0 for no-checkmate
        denominator_freq = np.delete(denominator_freq, [0])
        z = numerator_freq / denominator_freq
        return [denominator_y, z]

    def overallLengthOfCheckmate(self):
        data = self.df[self.df['EMV']> 90000]
        numerator_x, numerator_freq = np.unique(data['loc_group'], return_counts=True)
        denominator_y, denominator_freq = np.unique(list(self.df['loc_group']), return_counts=True)
        denominator_y = np.delete(denominator_y, [0])  # delete chomps off initial 0 for no-checkmate
        denominator_freq = np.delete(denominator_freq, [0])
        z = numerator_freq / denominator_freq
        return [denominator_y, z]

    def overallLengthOfCheckmateAndRatingGroup(self):
        data = self.df[self.df['EMV']> 90000]
        numerator_x, numerator_freq = np.unique(data['Rating_Group'], return_counts=True)
        denominator_y, denominator_freq = np.unique(list(self.df['Rating_Group']), return_counts=True)
        denominator_y = np.delete(denominator_y, [0])  # delete chomps off initial 0 for no-checkmate
        denominator_freq = np.delete(denominator_freq, [0])
        z = numerator_freq / denominator_freq
        return [denominator_y, z]

    def length_of_checkmate_frequency_nonregpositions(self):
        data = self.df[self.df['NinePtLead'] != 0]
        numerator_x, numerator_freq = np.unique(data['loc_group'], return_counts=True)
        denominator_y, denominator_freq = np.unique(self.df['loc_group'], return_counts=True)
        return [denominator_y, numerator_freq/denominator_freq]

    # this is the first method to use linear regression, this one makes a graph frequency of length of checkmate
    def linear_regression(self, t):
        print(self.df.head())
        self.df = self.df.dropna()
        z = []
        x_value_graph = ''
        y_value_graph = ''
        titlename = ""
        if int(t) == 1:
            z = self.rating_frequency_calculate()
            titlename = 'Games that Could have been Won'
            y_value_graph = 'Missed Mate Frequency'
            x_value_graph = 'Rating Groups'
        elif int(t) == 2:
            z = self.length_of_checkmate_frequency()
            titlename = 'Length of Checkmate to High Risk Positions Frequency'
            y_value_graph = 'Missed Mate Frequency'
            x_value_graph = 'Length of Checkmate'
        elif int(t) == 3:
            z = self.ratings_to_game_counts_old()
            titlename = 'Rating Group to Missed Mate Frequency using Game Count'
            y_value_graph = 'Game Count'
            x_value_graph = 'Rating Groups'
        elif int(t) == 4:
            z = self.length_of_checkmate_frequency()
            titlename = 'Rating Group to Missed Mate Frequency'
            y_value_graph = 'Length of Checkmate'
            x_value_graph = 'Rating Groups'
            print(z)
        elif int(t) == 5:
            z = self.length_of_checkmate_frequency_nonregpositions()
            titlename = 'Length of Checkmate to Lost Positions Frequency'
            y_value_graph = 'Missed Mate Frequency'
            x_value_graph = 'Length of Checkmate'
        elif int(t) == 6:
            z = self.rating_to_found_checkmate()
            titlename = 'Rating to Found Checkmates'
            y_value_graph = 'Found Checkmate Frequency'
            x_value_graph = 'Rating Group'
        elif int(t) == 7:
            z = self.overallLengthOfCheckmate()
            titlename = 'Overall Length of Checkmate '
            y_value_graph = 'Rating Group'
            x_value_graph = 'Length of Checkmate'
        elif int(t) == 8:
            z = self.overallLengthOfCheckmate()
            titlename = 'Overall Length of Checkmate To Rating Group'
            y_value_graph = 'Rating Group'
            x_value_graph = 'Length of Checkmate'

        x = np.array(z[0]).reshape(-1, 1)
        y = np.array(z[1]).reshape(-1, 1)
        print(x)
        print(y)
        lm.fit(X=x, y=y)
        pred = lm.predict(X=np.array(z[0]).reshape(-1, 1))
        plt.scatter(z[0], pred)
        plt.plot(z[0], pred, color='green', linewidth='3')
        plt.xlabel(x_value_graph)
        plt.ylabel(y_value_graph)
        plt.title(titlename)
        plt.savefig(titlename + x_value_graph + y_value_graph+'.png', bbox_inches="tight")
        plt.close()

    def multiple_regression(self):
        data = self.df[self.df['EMV'] > 90000]
        data.dropna(inplace=True)
        X = data[['Rating_Group', 'loc_group', 'NinePtLead']]
        lm.fit([X['Rating_Group'], X['loc_group']], np.array(X['NinePtLead']).reshape(-1,1))
        pred = lm.predict(X=X[['Rating_Group','loc_group']])
        plt.plot(X['Rating_Group'], pred, color='green', linewidth='3')
        plt.legend()
        plt.xlabel('Rating Group')
        plt.ylabel('Length of Checkmate Group')
        plt.title('Rating Group against Length of Checkmate Group')
        plt.savefig('Rating Group against LOC.png', bbox_inches="tight")
        plt.close()

    def multiRegressionRatingLoc(self):
        self.df = self.df.dropna()
        rating_loc = self.df[['Rating_Group', 'loc_group', 'NinePtLead']]
        ratings_keys, rating_counts_all = np.unique(rating_loc['Rating_Group'], return_counts=True)
        rating_keys_missedMate, rating_count_missedMate = np.unique(rating_loc[rating_loc['NinePtLead'] == 2]['Rating_Group'], return_counts=True)
        numerator_dict = dict(zip(rating_keys_missedMate, rating_count_missedMate))
        denominator_dict = dict(zip(ratings_keys, rating_counts_all))
        for key in denominator_dict.keys():
            if not numerator_dict.__contains__(key):
                numerator_dict[key] = 0
        numerator = np.array(np.fromiter(numerator_dict.values(), dtype=np.float64))
        denominator = np.array(np.fromiter(denominator_dict.values(), dtype=np.float64))
        return[numerator/denominator]

    # save the current plot call after every time u plot to close and ping for filename
    def save(self):
        name = input('Enter name for file, sorry if this is the second time:')
        name = name.strip()
        plt.savefig(name + '.png', bbox_inches="tight")
        plt.close()

    def write_nineptlead_moves(self, name):
        temp = self.df[self.df['NinePtLead'] == 2]
        temp.to_csv(name)
