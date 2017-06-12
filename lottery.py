#!/usr/bin/python3.6

from lottery_utils import SetOfBalls

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
    
class LotteryTicket:
    """
    """
    _draw_date = 0
    _lines = []
    
    def generate_ticket(self, draw_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        print("TODO")
        return (_draw_date, _lines)

    def print_ticket(self, ticket):
        """ Prints the given ticket. """
        print("Ticket date", _draw_date)
        for line in lines:
            print('Main {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}  Lucky stars {6:2d} {7:2d}'.format( \
                line.main_1, line.main_2, line.main_3, line.main_4, line.main_5, \
                line.lucky_1, line.lucky_2))
        return (0)
    

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

    def generate_ticket(self, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        return (0)

    def print_ticket(self, ticket):
        """ Prints the given ticket. """
        return (0)

