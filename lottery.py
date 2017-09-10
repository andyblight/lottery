#!/usr/bin/python3.6

""" Generic lottery class """
import datetime
import logging
import sys

from lottery_utils import SetOfBalls


class LotteryDraw:

    """ One draw from the CSV file. """

    def __init__(self):
        self.draw_date = datetime.date(2000, 1, 1)

    def __lt__(self, other):
        """ Returns True when self < other.  Test is on draw date. """
        result = False
        if self.draw_date < other.draw_date:
            result = True
        return result

    def as_string(self):
        """ Return the draw date as a string. """
        return self.draw_date.isoformat()


class LotteryParser:

    """ Parses the CSV data.
    There may be many parsers for each lottery.
    Each lottery has one or more parsers.
    """

    def __init__(self):
        self.name = 'default'

    def check_header(self):
        """ Prints error and returns False. """
        print("ERROR: Default check header called")
        return False

    def parse_row(self):
        """ Returns empty draw. """
        return LotteryDraw()


class LotteryTicket:

    """ Represents a lottery ticket.
    Defines the API for a lottery ticket.
    Implements all common operations for a lottery ticket.
    """

    def __init__(self, draw_date):
        # logging.info("Set date EM", draw_date)
        self._draw_date = draw_date
        self.lines = []

    def generate_lines(self, num_lines, ball_stats):
        """ Generates the given number of lines from the ball stats. """
        logging.info('TODO' + str(num_lines) + str(ball_stats[0][0]))

    def print_ticket(self, printout):
        """ Prints the ticket. """
        logging.info('Called print_ticket')
        for line in self.lines:
            if printout:
                print(line.as_string())
            else:
                logging.info('print_ticket line')
                logging.info(line.as_string())


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
        self._get_date_index = 0
        self._parser = None
        self._available_parsers = []

    def get_name(self):
        """ Returns the name of the lottery. """
        return self._name

    def reverse_results(self):
        """ Reverses the order of the results. """
        self.results.reverse()

    def check_header(self, row):
        """ Returns True if the header row is for this lottery. """
        result = False
        for parser in self._available_parsers:
            logging.info("Checking parser " + parser.name)
            if parser.check_header(row):
                self._parser = parser
                result = True
                break
        if self._parser:
            logging.info("Parser " + self._parser.name)
        else:
            print("ERROR: Lottery.check_header found no parser.")
            sys.exit()
        return result

    def get_sets_of_balls(self):
        """ Returns a list containing all sets of balls for this lottery. """
        return [self._balls]

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the
        results. """
        first_date = self.results[0].draw_date
        last_date = self.results[self._num_draws - 1].draw_date
        return (first_date, last_date)

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date
        range. """
        logging.info("TODO")
        return 0

    def get_draws_in_date_range(self, date_from, date_to):
        """ Returns a tuple of lottery_draws in the give date range. """
        lottery_draws = []
        # logging.info(date_from, date_to)
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from \
                    and lottery_draw.draw_date <= date_to:
                # logging.info("Matched", lottery_draw.draw_date)
                lottery_draws.append(lottery_draw)
        return lottery_draws

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        logging.info("TODO", num_lines, ball_stats)
        return LotteryTicket(next_lottery_date)

    def get_first_lottery_date(self):
        """ Returns the first lottery date.
        Resets the next lottery date to the first lottery date.
        """
        self._get_date_index = 0
        return self.results[0].draw_date

    def get_next_lottery_date(self):
        """ Returns the next lottery date. """
        result = datetime.date(3000, 1, 1)  # Return out of range date!
        self._get_date_index += 1
        if self._get_date_index < self._num_draws:
            result = self.results[self._get_date_index].draw_date
        return result
