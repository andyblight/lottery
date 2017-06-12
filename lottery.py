#!/usr/bin/python3.6

from set_of_balls import SetOfBalls

class LotteryDraw:
    """
    A lottery draw is the sets or sets of balls.
    """
    # def __init__(self):
    
    def print_draw(self, draw):
        print("TODO")

    def get_draw(self):
        print("TODO")
        return []

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


