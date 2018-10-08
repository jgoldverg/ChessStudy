class Parser(object):
    blackPointsDictionary = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9}
    whitePointsDictionary = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9}
    result_options = {'1/2': .5, '0-1': -1, '1-0': -1}

    def __init__(self, row):
        self.row = row

    def parse_fen(self, row):
        fen_str_no_space = str(row).split(' ')[0]
        white_points = 0
        black_points = 0
        #    positions_to_calculate = str(row).split('\n')
        if '#' in str(row):
            return {'new game'}
        for c in fen_str_no_space:
            if str(c) in self.blackPointsDictionary.keys():
                black_points += self.blackPointsDictionary.get(c)
            elif str(c) in self.whitePointsDictionary.keys():
                white_points += self.whitePointsDictionary.get(c)
            else:
                continue
        return {white_points, black_points}

    def parse_result(self, row):
        temp = row
        if str(temp) in self.result_options.keys():
            return self.result_options.get(temp)
        else:
            return None


