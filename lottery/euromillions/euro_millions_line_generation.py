#!/usr/bin/python3.6
""" Implementation classes for the EuroMillions lottery. """
import calendar
import datetime
import logging

from ..lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser, \
    LotteryTicketLineGenerator, LotteryStatsGenerationMethod
from ..lottery_utils import SetOfBalls, convert_str_to_date, frequency, \
    most_common_balls, least_common_balls

from .euro_millions_basics import EuroMillionsLine

LOGGER = logging.getLogger('EuroMillionsLineGeneration')

class LotteryTicketLineGeneratorEuro1(LotteryTicketLineGenerator):
    """ Ticket line generation method concrete class.
        Use most common stats.
    """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Euro1")

    def generate(self, stats_method):
        """ Generate a line. """
        line = EuroMillionsLine()
        most_probable = stats_method.get_most_probable()
        LOGGER.info(most_probable[0])
        LOGGER.info(most_probable[1])
        if most_probable[0] and most_probable[1]:
            num_main_balls = len(line.main_balls)
            num_lucky_stars = len(line.lucky_stars)
            for iterator in range(0, num_main_balls):
                line.main_balls[iterator] = most_probable[0][iterator][0]
            for iterator in range(0, num_lucky_stars):
                line.lucky_stars[iterator] = most_probable[1][iterator][0]
            line.sort()
        else:
            LOGGER.error("LTLGE1: most probable is empty")
        return line


class LotteryTicketLineGeneratorEuro2(LotteryTicketLineGenerator):
    """ Ticket line generation method concrete class.
        Use least common balls.
     """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Euro2")

    def generate(self, stats_method):
        """ Generate a line. """
        line = EuroMillionsLine()
        # Debug
        least_probable = stats_method.get_least_probable()
        LOGGER.info(least_probable[0])
        LOGGER.info(least_probable[1])
        if least_probable[0] and least_probable[1]:
            num_main_balls = len(line.main_balls)
            num_lucky_stars = len(line.lucky_stars)
            for iterator in range(0, num_main_balls):
                line.main_balls[iterator] = least_probable[0][iterator][0]
            for iterator in range(0, num_lucky_stars):
                line.lucky_stars[iterator] = least_probable[1][iterator][0]
            line.sort()
        else:
            LOGGER.error("LTLGE2: least probable is empty")
        return line


class LotteryTicketLineGeneratorEuro3(LotteryTicketLineGenerator):
    """ Ticket line generation method concrete class.
        Use mixture of most for main and least for luck stars.
     """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Euro3")

    def generate(self, stats_method):
        """ """
        line = EuroMillionsLine()
        # Most probable
        most_probable = stats_method.get_most_probable()
        LOGGER.info(most_probable[0])
        LOGGER.info(most_probable[1])
        if most_probable[0] and most_probable[1]:
            least_probable = stats_method.get_least_probable()
            LOGGER.info(least_probable[0])
            LOGGER.info(least_probable[1])
            if least_probable[0] and least_probable[1]:
                num_main_balls = len(line.main_balls)
                num_lucky_stars = len(line.lucky_stars)
                # Use most probable for main balls and least probable for
                # lucky stars
                for iterator in range(0, num_main_balls):
                    line.main_balls[iterator] = most_probable[0][iterator][0]
                for iterator in range(0, num_lucky_stars):
                    line.lucky_stars[iterator] = least_probable[1][iterator][0]
                line.sort()
            else:
                LOGGER.error("LTLGE3: least probable is empty")
        else:
            LOGGER.error("LTLGE3: most probable is empty")
        return line


class LotteryTicketLineGeneratorEuro4(LotteryTicketLineGenerator):
    """ Ticket line generation method concrete class.
        Use mixture of most and least.
     """

    def __init__(self):
        LotteryTicketLineGenerator.__init__(self, "Euro4")

    def generate(self, stats_method):
        """ """
        line = EuroMillionsLine()
        # Most probable
        most_probable = stats_method.get_most_probable()
        LOGGER.info(most_probable[0])
        LOGGER.info(most_probable[1])
        if most_probable[0] and most_probable[1]:
            least_probable = stats_method.get_least_probable()
            LOGGER.info(least_probable[0])
            LOGGER.info(least_probable[1])
            if least_probable[0] and least_probable[1]:
                num_main_balls = len(line.main_balls)
                num_lucky_stars = len(line.lucky_stars)
                # Use least probable for main balls and most probable for
                # lucky stars
                for iterator in range(0, num_main_balls):
                    line.main_balls[iterator] = least_probable[0][iterator][0]
                for iterator in range(0, num_lucky_stars):
                    line.lucky_stars[iterator] = most_probable[1][iterator][0]
                line.sort()
            else:
                LOGGER.error("LTLGE4: least probable is empty")
        else:
            LOGGER.error("LTLGE4: most probable is empty")
        return line


