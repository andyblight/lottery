#!/usr/bin/python3.6

"""
TODO
"""
import collections
import sys

from lottery_utils import convert_str_to_date

EuroMillionsRow = collections.namedtuple('EuroMillionsRow', \
        ['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
        'lucky_1', 'lucky_2'])

class LotteryResults:
    """ The base class for holding lottery results that have been parsed from
    a .csv file.
    """
    results = []
    type = ""
    num_rows = 0

    def __init__(self):
        self.results = []
        self.type = ""
        self.num_rows = 0

    def parse_header(self, row):
        """ Parse the header row to work out the file type. """
        self.type = ""
        if str(row[6]) == 'Lucky Star 1':
            self.type = 'euro'
        elif str(row[7]) == 'Bonus Ball':
            self.type = 'lotto'
        else:
            print("Unknown file type")
            sys.exit(1)

    def parse_euro_millions_row(self, row):
        """ Read row data and copy into EuroMillions tuple """
        euro = EuroMillionsRow(convert_str_to_date(str(row[0])), \
                               int(row[1]), int(row[2]), int(row[3]), \
                               int(row[4]), int(row[5]), int(row[6]), \
                               int(row[7]))
        self.results.append(euro)
        self.num_rows += 1

    def parse_row(self, row):
        """ Parse row data and append """
        if self.type == 'euro':
            self.parse_euro_millions_row(row)
        elif self.type == 'lotto':
            print("TODO")
        else:
            print("Unknown file type")
            sys.exit(1)

    def get_latest_date(self):
        """ The latest date is the first element on the first row of results """
        print("Latest: ", self.results[0].draw_date)
        return self.results[0].draw_date
