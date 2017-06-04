#!/usr/bin/python3.6

from _thread import _count
import collections
import csv
import sys

from lottery_utils import convert_str_to_date, frequency


class SetOfBalls:
    """ Information about the set of balls. """
    _count = 0

    def __init__(self, count):
        """ Initialises the class. """
        _count = count

    def get_count(self):
        """ Return the number of balls in the set. """
        return _count


class Lottery:
    """ 
    The base class for all lotteries.
    This class implements the functions for a single set of balls (the most
    common type of lottery). 
    """
    _name = ""
    results = []
    _num_rows = 0

    def __init__(self):
        """ Initialises the class. """
        self._name = 'default'
        self.results = []
        self._num_rows = 0
        self._main_balls = SetOfBalls(10)

    def get_name(self):
        """ Returns the name of the lottery. """
        return self._name

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        return False

    def get_set_of_balls(self):
        """ Returns a set of balls.. """
        return self._set_of_balls

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the results. """
        return (0, 0)

    def get_balls_in_date_range(self, date_from, date_to):
        """ Gets the a tuple containing the sets of balls in the give date 
        range. """
        return (0)

EuroMillionsRow = collections.namedtuple('EuroMillionsRow', \
        ['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
        'lucky_1', 'lucky_2'])


class LotteryEuroMillions(Lottery):
    """ The Euro Millions lottery. """
    _main_balls = SetOfBalls(50)
    _lucky_star_balls = SetOfBalls(12)

    def __init__(self):
        self._name = "EuroMillions"
        self._sets_of_balls = 2

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        return str(row[6]) == 'Lucky Star 1'

    def get_balls(self):
        """ Returns a set of balls.. """
        return (self._main_balls, self._lucky_star_balls)

    def parse_row(self, row):
        """ Read row data and copy into EuroMillions tuple """
        euro = EuroMillionsRow(convert_str_to_date(str(row[0])), \
                               int(row[1]), int(row[2]), int(row[3]), \
                               int(row[4]), int(row[5]), int(row[6]), \
                               int(row[7]))
        self.results.append(euro)
        self._num_rows += 1

    def get_balls_in_date_range(self, date_from, date_to):
        """ Gets the a tuple containing the sets of balls in the give date 
        range. """
        main_balls = []
        lucky_stars = []
        for row in self.results:
            if row.draw_date >= date_from and row.draw_date <= date_to:
                """ Appends all main balls to the given list """
                main_balls.append(row.main_1)
                main_balls.append(row.main_2)
                main_balls.append(row.main_3)
                main_balls.append(row.main_4)
                main_balls.append(row.main_5)
                """ Appends all lucky star balls to the given list """
                lucky_stars.append(row.lucky_1)
                lucky_stars.append(row.lucky_2)
        return (main_balls, lucky_stars)

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the results. """
        earliest = self.results[0].draw_date
        latest = self.results[self._num_rows - 1].draw_date
        return (earliest, latest)


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
