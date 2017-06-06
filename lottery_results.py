#!/usr/bin/python3.6

import collections
import csv
import sys

from lottery_utils import convert_str_to_date, frequency


class SetOfBalls:
    """ Information about the set of balls. """
    _num_balls = 0
    _name = ""

    def __init__(self, name, num_balls):
        """ Initialises the class. """
        self._num_balls = num_balls
        self._name = name

    def get_num_balls(self):
        """ Return the number of balls in the set. """
        return self._num_balls

    def get_name(self):
        """ Return the number of balls in the set. """
        return self._name


class Lottery:
    """ 
    The base class for all lotteries.
    This class implements the functions for a single set of balls (the most
    common type of lottery). 
    """
    _name = ""
    results = []
    _num_draws = 0

    def __init__(self):
        """ Initialises the class. """
        self._name = 'default'
        self.results = []
        self._num_draws = 0
        self._balls = SetOfBalls('default', 10)

    def get_name(self):
        """ Returns the name of the lottery. """
        return self._name

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        return False

    def get_ball_sets(self):
        """ Returns all sets of balls for this lottery. """
        return (self._balls)

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the results. """
        return (0, 0)

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date 
        range. """
        return (0)

    def get_draws_in_date_range(self, date_from, date_to):
        """ Returns a tuple of lottery_draws in the give date range. """
        return (0)

    def print_draw(self, draw):
        print("TODO")


EuroMillionsDraw = collections.namedtuple('EuroMillionsDraw', \
        ['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
        'lucky_1', 'lucky_2'])


class LotteryEuroMillions(Lottery):
    """ The Euro Millions lottery. """
    _main_balls = SetOfBalls("main", 50)
    _lucky_star_balls = SetOfBalls("lucky stars", 12)

    def __init__(self):
        self._name = "EuroMillions"
        self._sets_of_balls = 2

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        return str(row[6]) == 'Lucky Star 1'

    def get_ball_sets(self):
        """ Returns all sets of balls for this lottery. """
        return (self._main_balls, self._lucky_star_balls)

    def parse_row(self, row):
        """ Read row data and copy into EuroMillions tuple """
        euro = EuroMillionsDraw(convert_str_to_date(str(row[0])), \
                                int(row[1]), int(row[2]), int(row[3]), \
                                int(row[4]), int(row[5]), int(row[6]), \
                                int(row[7]))
        self.results.append(euro)
        self._num_draws += 1

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date 
        range. """
        main_balls = []
        lucky_stars = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                """ Appends all main balls to the given list """
                main_balls.append(lottery_draw.main_1)
                main_balls.append(lottery_draw.main_2)
                main_balls.append(lottery_draw.main_3)
                main_balls.append(lottery_draw.main_4)
                main_balls.append(lottery_draw.main_5)
                """ Appends all lucky star balls to the given list """
                lucky_stars.append(lottery_draw.lucky_1)
                lucky_stars.append(lottery_draw.lucky_2)
        return (main_balls, lucky_stars)

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the results. """
        latest = self.results[0].draw_date
        earliest = self.results[self._num_draws - 1].draw_date
        return (earliest, latest)

    def get_draws_in_date_range(self, date_from, date_to):
        """ Returns a tuple of lottery_draws in the give date range. """
        lottery_draws = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                lottery_draws.append(lottery_draw)
        return lottery_draws

    def print_draw(self, lottery_draw):
        """ Print the given draw. """
        print("Date", lottery_draw.draw_date, \
              "main", lottery_draw.main_1, lottery_draw.main_2, \
              lottery_draw.main_3, lottery_draw.main_4, \
              lottery_draw.main_5, "lucky stars", \
              lottery_draw.lucky_1, lottery_draw.lucky_2)


class LotteryResults:
    """
    The LotteryResults class reads a lottery results CSV file into an internal 
    cache and provides methods to access the data in the internal cache. 
.   """
    _lottery = Lottery()
    _euro_millions = LotteryEuroMillions()

    def __init__(self):
        self.type = ""

    def parse_header(self, row):
        """ Parse the header row to work out the file type. """
        self.type = ""
        if self._euro_millions.check_header(row):
            self._lottery = self._euro_millions
        elif str(row[7]) == 'Bonus Ball':
            print("FIXME: Using default lottery")
        else:
            print("Using default lottery")

    def parse_row(self, row):
        """ Parse row data and append """
        self._lottery.parse_row(row)

    def load_file(self, filename):
        with open(filename, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            ignore_header = True
            for row in filereader:
                if ignore_header:
                    self.parse_header(row)
                    ignore_header = False
                    continue
                self._lottery.parse_row(row)

    def get_lottery(self):
        """ Returns the lottery instance. """
        return self._lottery
