#!/usr/bin/python3.6

""" Generic lottery class """
import datetime
import logging

from lottery_utils import SetOfBalls

logger = logging.getLogger('Lottery')


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

    @staticmethod
    def parse_row(row):
        """ Returns empty draw. """
        draw = LotteryDraw()
        return draw


class LotteryTicket:

    """ Represents a lottery ticket.
        Implements all common operations for a lottery ticket.
    """

    def __init__(self, draw_date):
        # logger.info("Set date EM", draw_date)
        self._draw_date = draw_date
        self.lines = []

    def print(self, printout):
        """ Prints the ticket. """
        logger.info('Called print_ticket')
        for line in self.lines:
            if printout:
                print(line.as_string())
            else:
                logger.info('print_ticket line')
                logger.info(line.as_string())


class LotteryTicketGenerationMethod:
    """ Ticket generation method base class """

    def __init__(self, name):
        self.name = name

    def generate(self, draw_date, num_lines, ball_stats):
        """ """
        logger.info('TODO' + str(num_lines) + str(ball_stats[0][0]))
        return LotteryTicket(draw_date)


class LotteryStatsGenerationMethod:
    """ Statistics generation method base class """

    def __init__(self):
        self.name = "Base class"

    def analyse(self, lottery_results, date_range):
        """ """
        logger.info("TODO")

    def get_most_probable(self):
        """ """
        return []

    def get_least_probable(self):
        """ """
        return []


class Lottery:

    """ The base class for all lotteries.
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
        # Generation methods are added by the concrete classes.
        self._ticket_generation_methods = []
        self._stats_generation_methods = []

    def get_name(self):
        """ Returns the name of the lottery. """
        return self._name

    def check_header(self, row):
        """ Returns True if the header row is for this lottery. """
        logger.info("Called Lottery ch. Num parsers %d",
                    len(self._available_parsers))
        result = False
        for parser in self._available_parsers:
            logger.info("Checking parser %s", parser.name)
            if parser.check_header(row):
                self._parser = parser
                logger.info("Selected %s", parser.name)
                result = True
                break
        return result

    def reverse_results(self):
        """ Reverses the order of the results. """
        self.results.reverse()

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
            range. 
        """
        logger.debug("TODO, %s, %s", date_from, date_to)
        return 0

    def get_draws_in_date_range(self, date_from, date_to):
        """ Returns a tuple of lottery_draws in the give date range. """
        lottery_draws = []
        # logger.info(date_from, date_to)
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from \
                    and lottery_draw.draw_date <= date_to:
                # logger.info("Matched", lottery_draw.draw_date)
                lottery_draws.append(lottery_draw)
        return lottery_draws

    def get_ticket_generation_methods(self):
        """ Returns the list of ticket generation methods owned by this class. 
        """
        return self._ticket_generation_methods

    def get_stats_generation_methods(self):
        """ Returns the list of ticket generation methods owned by this class. 
        """
        return self._stats_generation_methods
