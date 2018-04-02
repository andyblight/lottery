#!/usr/bin/python3.6
""" Provides methods for queriing data loaded from a CSV file of lottery
    results.
"""

import csv
import logging

from euro_millions import LotteryEuroMillions
from lotto import LotteryLotto


LOGGER = logging.getLogger('LotteryResults')


class LotteryResults:
    """
    The LotteryResults class reads a lottery results CSV file into an internal
    lottery instance and provides methods to access the data in the Lottery.
.   """

    def __init__(self):
        self._lottery = None
        LOGGER.info("Lottery.__init__")
        self._available_lotteries = []
        self._available_lotteries.append(LotteryEuroMillions())
        self._available_lotteries.append(LotteryLotto())
        # Debug
        LOGGER.info("Initialised lotteries:")
        for lottery in self._available_lotteries:
            LOGGER.info(lottery.get_name())

    def parse_header(self, row):
        """ Parse the header row to work out the file type.
        There are two sources, national lottery and
        http://lottery.merseyworld.com.
        Each has a different header row so it is easy to call the correct row
        parser.
        Each parser is hidden in the lottery class instance.
        """
        for lottery in self._available_lotteries:
            LOGGER.info("Checking lottery " + lottery.get_name())
            result = lottery.check_header(row)
            LOGGER.info("Result " + str(result))
            if result:
                LOGGER.info("Found parser in " + lottery.get_name())
                self._lottery = lottery
                break
        if self._lottery is None:
            LOGGER.info("Using default lottery")

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
