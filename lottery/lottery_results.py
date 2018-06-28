#!/usr/bin/python3.6
""" Provides methods for queriing data loaded from a CSV file of lottery
    results.
"""

import csv
import datetime
import logging

from .euromillions.euro_millions import LotteryEuroMillions
from .lotto.lotto import LotteryLotto


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
        Each parser is hidden in the lottery class instance.
        """
        for lottery in self._available_lotteries:
            LOGGER.info("Checking lottery %s", lottery.get_name())
            result = lottery.check_header(row)
            LOGGER.info("Result %s", str(result))
            if result:
                LOGGER.info("Found parser in %s", lottery.get_name())
                self._lottery = lottery
                break
        if self._lottery is None:
            LOGGER.info("Using default lottery")

    def load_file(self, filename):
        """ Load data from CSV file in the results.  The data is the file is
        most recent data first, so reverse order of list when loaded.
        """
        with open(filename, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            is_header = True
            for row in filereader:
                if is_header:
                    self.parse_header(row)
                    is_header = False
                else:
                    # Get new draw,
                    draw = self._lottery.get_new_draw()
                    # Parse raw into a LotteryDraw object and adds to list of
                    # draws.
                    self._lottery.parse_row(draw, row)
        self._lottery.reverse_results()

    def get_lottery(self):
        """ Returns the lottery instance. """
        return self._lottery

    def generate_ticket(self, ball_stats, line_method_names):
        """ Generates a ticket using the chosen line methods. """
        ticket_datetime = datetime.datetime.now()
        ticket = self.get_lottery().get_new_ticket(ticket_datetime)
        line_methods = self.get_lottery().get_line_generation_methods()
        for line_name in line_method_names:
            for line_method in line_methods:
                logging.debug("LR.gt: line %s", line_method.name)
                if line_method.name == line_name:
                    line = line_method.generate(ball_stats)
                    ticket.lines.append(line)
                    break
        return ticket