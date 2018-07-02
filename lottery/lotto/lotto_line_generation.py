#!/usr/bin/python3.6
""" National Lottery Lotto 
TODO
"""

import calendar
import datetime
import logging

from ..lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser, \
    LotteryTicketLineGenerator, LotteryStatsGenerationMethod
from ..lottery_utils import SetOfBalls, convert_str_to_date, frequency, \
    most_common_balls, least_common_balls
from .lotto_basics import LottoTicketLine

LOGGER = logging.getLogger('LottoLineGeneration')

class LotteryTicketLineGeneratorLotto1(LotteryTicketLineGenerator):
    """ Line generation method concrete class.
        Use most common stats.
    """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Lotto1")

    def generate(self, stats_method):
        """ Generate a line. """
        line = LottoTicketLine()
        # List of tuples containing (ball num, frequency)
        most_probable = stats_method.get_most_probable()
        LOGGER.info(most_probable)
        if most_probable[0]:
            max_balls = len(line.main_balls)
            LOGGER.info("LTLGL1: max balls %d", max_balls)
            for iterator in range(0, max_balls):
                line.main_balls[iterator] = most_probable[iterator][0]
            LOGGER.info("LTLGL1: %s", line.as_string())
            line.sort()
        else:
            LOGGER.error("LTLGL1: most probable is empty")
        return line


class LotteryTicketLineGeneratorLotto1A(LotteryTicketLineGenerator):
    """ Line generation method concrete class.
        Use most common stats alternative last number.
    """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Lotto1A")

    def generate(self, stats_method):
        """ Generate a line. """
        line = LottoTicketLine()
        # List of tuples containing (ball num, frequency)
        most_probable = stats_method.get_most_probable()
        LOGGER.info(most_probable)
        if most_probable[0]:
            max_balls = len(line.main_balls)
            mp_length = len(most_probable)
            LOGGER.info("LTLGL1A: max balls %d", max_balls)
            for iterator in range(0, max_balls - 1):
                line.main_balls[iterator] = most_probable[iterator][0]
            line.main_balls[max_balls - 1] = most_probable[mp_length - 1][0]
            LOGGER.info("LTLGL1A: %s", line.as_string())
            line.sort()
        else:
            LOGGER.error("LTLGL1A: most probable is empty")
        return line


class LotteryTicketLineGeneratorLotto2(LotteryTicketLineGenerator):
    """ Ticket generation method concrete class.
        Use least common stats.
    """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Lotto2")

    def generate(self, stats_method):
        """ Generate a line. """
        line = LottoTicketLine()
        # List of tuples containing (ball num, frequency)
        least_probable = stats_method.get_least_probable()
        LOGGER.info(least_probable)
        if least_probable[0]:
            max_balls = len(line.main_balls)
            LOGGER.info("LTLGL2: max balls %d", max_balls)
            for iterator in range(0, max_balls):
                line.main_balls[iterator] = least_probable[iterator][0]
            LOGGER.info("LTLGL2: %s", line.as_string())
            line.sort()
        else:
            LOGGER.error("LTLGL2: most probable is empty")
        return line


class LotteryTicketLineGeneratorLotto2A(LotteryTicketLineGenerator):
    """ Line generation method concrete class.
        Use least common stats alternative last number.
    """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Lotto2A")

    def generate(self, stats_method):
        """ Generate a line. """
        line = LottoTicketLine()
        # List of tuples containing (ball num, frequency)
        least_probable = stats_method.get_least_probable()
        LOGGER.info(least_probable)
        if least_probable[0]:
            max_balls = len(line.main_balls)
            lp_length = len(least_probable)
            LOGGER.info("LTLGL2A: max balls %d", max_balls)
            for iterator in range(0, max_balls - 1):
                line.main_balls[iterator] = least_probable[iterator][0]
            line.main_balls[max_balls - 1] = least_probable[lp_length - 1][0]
            LOGGER.info("LTLGL2A: %s", line.as_string())
            line.sort()
        else:
            LOGGER.error("LTLGL2A: most probable is empty")
        return line


