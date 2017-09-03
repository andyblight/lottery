#!/usr/bin/python3.6
""" STUFF!!! """

import csv

from euro_millions import LotteryEuroMillions
from lottery import Lottery
from lotto import LotteryLotto


class LotteryResults:

    """
    The LotteryResults class reads a lottery results CSV file into an internal
    cache and provides methods to access the data in the internal cache.
.   """

    def __init__(self):
        self._lottery = None
        self._default_lottery = Lottery()
        self._euro_millions = LotteryEuroMillions()
        self._lotto = LotteryLotto()

    def parse_header(self, row):
        """ Parse the header row to work out the file type. 
        There are two sources, national lottery and 
        http://lottery.merseyworld.com.
        Each has a different header row so it is easy to call the correct row
        parser.
        Each parser is hidden in the lottery class instance.
        """
        if self._euro_millions.check_header(row):
            self._lottery = self._euro_millions
        elif self._lotto.check_header(row):
            self._lottery = self._lotto
        else:
            print("Using default lottery")

    def parse_row(self, row):
        """ Parse row data and append """
        self._lottery.parse_row(row)

    def load_file(self, filename):
        """ Load data from CSV file in the results.  The data is the file is
        most recent data first, so reverse order of list when loaded.
        """
        with open(filename, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            ignore_header = True
            for row in filereader:
                if ignore_header:
                    self.parse_header(row)
                    ignore_header = False
                    continue
                self._lottery.parse_row(row)
        self._lottery.reverse_results()

    def get_lottery(self):
        """ Returns the lottery instance. """
        return self._lottery
