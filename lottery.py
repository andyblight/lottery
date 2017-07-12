#!/usr/bin/python3.6

from lottery_utils import SetOfBalls

class LotteryTicket:
    """ Represents a lottery ticket.
    Defines the API for a lottery ticket.
    Implements all common operations for a lottery ticket.
    """
    def __init__(self, draw_date):
        # print("Set date EM", draw_date)
        self._draw_date = draw_date
        self.lines = []

    def generate_lines(self, num_lines, ball_stats):
        """ Generates the given number of lines from the ball stats. """
        print('TODO')

    def print_ticket(self):
        """ Prints the ticket. """
        print("Ticket date", _draw_date)
        for line in lines:
            print('Line TODO')

class Lottery:
    """ 
    The base class for all lotteries.
    This class implements the functions for a single set of balls (the most
    common type of lottery). 
    """
    def __init__(self):
        """ Initialises the class. """
        self._name = 'default'
        self.results = []
        self._num_draws = 0
        self._balls = SetOfBalls('default', 10)

    def get_name(self):
        """ Returns the name of the lottery. """
        return self._name

    def reverse_results(self):
        """ Reverses the order of the results. """
        self.results.reverse()

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        print("TODO")
        return False

    def get_ball_sets(self):
        """ Returns all sets of balls for this lottery. """
        print("TODO")
        return (self._balls)

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the results. """
        first_date = self.results[0].draw_date
        last_date = self.results[self._num_draws - 1].draw_date
        return (first_date, last_date)

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date 
        range. """
        print("TODO")
        return (0)

    def get_draws_in_date_range(self, date_from, date_to):
        """ Returns a tuple of lottery_draws in the give date range. """
        lottery_draws = []
        # print(date_from, date_to)
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                # print("Matched", lottery_draw.draw_date)
                lottery_draws.append(lottery_draw)
        return lottery_draws

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        print("TODO")
        return LotteryTicket(next_lottery_date)

    def print_ticket(self, ticket):
        """ Prints the given ticket. """
        ticket.print_ticket()

