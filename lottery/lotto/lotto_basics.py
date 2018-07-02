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

LOGGER = logging.getLogger('LottoTicketLine')

class LottoTicketLine:
    """ Represents a line of lottery numbers on a ticket. """

    def __init__(self):
        """ Creates one sets of balls with the right number of balls. """
        self.main_balls = []
        # 6 main balls
        for _ in range(0, 6):
            self.main_balls.append(0)

    def as_string(self):
        """ Return this line as a string. """
        ## Why is this print ball[0] as 0 all the time?
        return 'Line: {0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  {5:2d}'.format(
            self.main_balls[0], self.main_balls[1], self.main_balls[2],
            self.main_balls[3], self.main_balls[4], self.main_balls[5])

    @staticmethod
    def _mark_ball(line_string, main):
        """ Mark winning balls with *. """
        main_ball_offset = 8
        if main >= 0 and main <= 5:
            index = main_ball_offset + (main * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        # LOGGER.info(line_string)
        return line_string

    def sort(self):
        """ Sorts the line into ascending numerical order. """
        self.main_balls.sort()

    @staticmethod
    def _is_winner(main_matched):
        """ The rules for winning are:
            Match 6                 Jackpot
            Match 5 + bonus ball
            Match 4
            Match 3
            Match 2
        """
        result = False
        if main_matched >= 2:
            result = True
        return result

    def score(self, draw):
        """ Returns a tuple containing:
        The bonus ball is only used when 5 main balls are matched.
        https://www.national-lottery.co.uk/games/lotto/game-procedures#int_prizes
        0 - count of main ball matches
        1 - True if the line is a winner.
        2 - string of the line with the matching balls shown
        """
        main_matched = 0
        matching_str = self.as_string()
        for iterator in range(0, len(self.main_balls)):
            if self.main_balls[iterator] == draw.main_balls[iterator]:
                main_matched += 1
                matching_str = self._mark_ball(matching_str, iterator)
        # Deal with bonus ball, the last ball in the draw
        if main_matched == 5:
            for iterator in range(0, len(self.main_balls)):
                if self.main_balls[iterator] == draw.bonus_ball:
                    main_matched += 1
                    matching_str = self._mark_ball(matching_str, iterator)
        return (main_matched, self._is_winner(main_matched), matching_str)
