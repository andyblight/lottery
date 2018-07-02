#!/usr/bin/python3.6
""" Implementation classes for the EuroMillions lottery. """
import calendar
import datetime
import logging

from ..lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser, \
    LotteryTicketLineGenerator, LotteryStatsGenerationMethod
from ..lottery_utils import SetOfBalls, convert_str_to_date, frequency, \
    most_common_balls, least_common_balls

LOGGER = logging.getLogger('EuroMillionsLineBasics')


class EuroMillionsLine:
    """ Represents a line of lottery numbers. """

    def __init__(self):
        """ Creates two sets of balls with the right number of balls. """
        self.main_balls = []
        for _ in range(0, 5):
            self.main_balls.append(0)
        self.lucky_stars = []
        for _ in range(0, 2):
            self.lucky_stars.append(0)

    def as_string(self):
        """ Converts a line to a string. """
        # print("as_string, main, lucky", self.main_balls, self.lucky_stars)
        main_str = 'Main balls: {0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  ' \
            .format(
                self.main_balls[0], self.main_balls[1], self.main_balls[2],
                self.main_balls[3], self.main_balls[4])
        lucky_str = 'Lucky stars: {0:2d}  {1:2d} '.format(
            self.lucky_stars[0], self.lucky_stars[1])
        return main_str + lucky_str

    @staticmethod
    def _mark_ball(line_string, main, lucky):
        """ Mark winning balls with *. """
        main_balls_offset = 14
        lucky_stars_offset = main_balls_offset + 33
        if main > -1 and main < 5:
            index = main_balls_offset + (main * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        if lucky > -1 and lucky < 2:
            index = lucky_stars_offset + (lucky * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        LOGGER.info(line_string)
        return line_string

    def sort(self):
        """ Sorts the line into ascending numerical order. """
        self.main_balls.sort()
        self.lucky_stars.sort()

    @staticmethod
    def _is_winner(main_matched, lucky_matched):
        """ The rules for winning are
        Match 5 + 2 Lucky Stars - Jackpot
        Match 5 + 1 Lucky Star
        Match 5
        Match 4 + 2 Lucky Stars
        Match 4 + 1 Lucky Star
        Match 4
        Match 3 + 2 Lucky Stars
        Match 3 + 1 Lucky Star
        Match 3
        Match 2 + 2 Lucky Stars
        Match 2 + 1 Lucky Star
        Match 2
        Match 1 + 2 Lucky Stars
        """
        result = False
        if main_matched == 1 and lucky_matched == 2:
            result = True
        else:
            if main_matched >= 2:
                result = True
        return result

    def score(self, draw):
        """ Returns a tuple containing:
        0 - count of main plus lucky star matches
        1 - True if the line is a winner.
        2 - string of the line with the matching balls shown
        """
        main_matched = 0
        lucky_matched = 0
        matching_str = draw.line.as_string()
        for iterator in range(0, len(self.main_balls)):
            if self.main_balls[iterator] == draw.line.main_balls[iterator]:
                main_matched += 1
                matching_str = self._mark_ball(matching_str, iterator, -1)
        for iterator in range(0, len(self.lucky_stars)):
            if self.lucky_stars[iterator] == draw.line.lucky_stars[iterator]:
                lucky_matched += 1
                matching_str = self._mark_ball(matching_str, -1, iterator)
        return (main_matched + lucky_matched,
                self._is_winner(
                    main_matched,
                    lucky_matched,
                ), matching_str)


