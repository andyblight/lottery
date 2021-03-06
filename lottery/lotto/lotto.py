#!/usr/bin/python3.6
""" National Lottery Lotto classes.

NOTE: fewer winners on this lottery than Euro-millions.
Consider individual ball sets?
More data needs to be analysed to get enough statistical data.
Possibly consider machines as well.
"""

import calendar
import datetime
import logging

from ..lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser, \
    LotteryTicketLineGenerator, LotteryStatsGenerationMethod
from ..lottery_utils import SetOfBalls, convert_str_to_date, frequency, \
    most_common_balls, least_common_balls
from .lotto_basics import LottoTicketLine

# TODO Import one function instead of each function?
from .lotto_line_generation import LotteryTicketLineGeneratorLotto1, \
    LotteryTicketLineGeneratorLotto1A, LotteryTicketLineGeneratorLotto2, \
    LotteryTicketLineGeneratorLotto2A

LOGGER = logging.getLogger('Lotto')


class LottoDraw(LotteryDraw):
    """ Groups draw date and lottery line."""

    def __init__(self):
        super(LottoDraw, self).__init__()
        self.main_balls = []
        self.ball_set = None
        self.machine = ""
        # 6 main balls
        for _ in range(0, 6):
            self.main_balls.append(0)
        self.bonus_ball = 0

    def as_string(self):
        """ Returns this draw as a string. """
        str1 = '{0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  {5:2d}'.format(
            self.main_balls[0], self.main_balls[1], self.main_balls[2],
            self.main_balls[3], self.main_balls[4], self.main_balls[5])
        str2 = 'Bonus ball {0:2d}  Ball set {1:2d}  Machine {2} '.format(
            self.bonus_ball, self.ball_set, self.machine)
        return self.draw_date.isoformat() + ' Main balls: ' + str1 + '  ' + str2


class LotteryParserLottoNL(LotteryParser):
    """ Parses the CSV data from the National Lottery. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserLottoNL, self).__init__()
        self.name = 'Lotto National Lottery'

    def check_header(self, row):
        """ Returns True if the header row is for this lottery.
            Distinct items are "Bonus Ball", "Ball Set", "Machine", "Raffles"
         """
        LOGGER.info(self.name + row[7])
        return row[7] == 'Bonus Ball'

    @staticmethod
    def parse_row(row, draw):
        """ Read row data and copy into the LottoDraw class.
            Header row looks like this:
            DrawDate,Ball 1,Ball 2,Ball 3,Ball 4,Ball 5,Ball 6,Bonus Ball,
            Ball Set,Machine,Raffles,DrawNumber
        """
        draw.draw_date = convert_str_to_date(str(row[0]))
        draw.main_balls[0] = int(row[1])
        draw.main_balls[1] = int(row[2])
        draw.main_balls[2] = int(row[3])
        draw.main_balls[3] = int(row[4])
        draw.main_balls[4] = int(row[5])
        draw.main_balls[5] = int(row[6])
        draw.bonus_ball = int(row[7])
        draw.ball_set = int(row[8])
        draw.machine = row[9]
        # print("AJB: NL:", draw.main_balls)
        # print("AJB: NL:", draw.bonus_ball)
        return draw


class LotteryParserLottoMW(LotteryParser):
    """ Parses the CSV data from http://lottery.merseyworld.com/. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserLottoMW, self).__init__()
        self.name = 'Lotto MerseyWorld'

    def check_header(self, row):
        """ Returns True if this is merseyworld lotto.
        Unique values are Draw number and N1. """
        LOGGER.info(" %s '%s' '%s'", self.name, row[0], row[5])
        return row[0] == 'No.' and row[5] == ' N1'

    @staticmethod
    def parse_row(row, draw):
        ''' Read row data and copy into LottoDraw class.
        0  - No.,Day,DD,MMM,YYYY,
        5  - N1,N2,N3,N4,N5,
        10 - N6,BN,Jackpot,Wins,Machine,
        15 - Set
        Day of week is ignored as this can be obtained from the date.
        '''
        draw.draw_number = int(row[0])
        day_num = int(row[2])
        month_num = list(calendar.month_abbr).index(row[3])
        year_num = int(row[4])
        draw.draw_date = datetime.date(year_num, month_num, day_num)
        # print("AJB: " + draw.draw_date.isoformat())
        draw.main_balls[0] = int(row[5])
        draw.main_balls[1] = int(row[6])
        draw.main_balls[2] = int(row[7])
        draw.main_balls[3] = int(row[8])
        draw.main_balls[4] = int(row[9])
        draw.main_balls[5] = int(row[10])
        draw.bonus_ball = int(row[11])
        #print("AJB: MW:", draw.main_balls)
        #print("AJB: MW:", draw.bonus_ball)
        draw.jackpot = int(row[12])
        draw.jackpot_wins = int(row[13])
        draw.machine = row[14]
        draw.ball_set = int(row[15])
        return draw


class LotteryStatsGenerationMethodLotto1(LotteryStatsGenerationMethod):
    """ Generates most and least probable balls from the lottery results. """

    def __init__(self):
        LotteryStatsGenerationMethod.__init__(self, "Lotto1")
        self._main_balls_most_probable = []
        self._main_balls_least_probable = []

    def analyse(self, lottery_results, date_range):
        """ Sets internal stores of information from the given results in the
            given date range.
        """
        # A date range is (most_recent, short_range, long_range)
        date_to = date_range[0]
        date_from = date_range[2]  # FIXME What about short_range???
        lottery = lottery_results.get_lottery()
        balls_in_range_tuple = lottery.get_balls_in_date_range(
            date_from, date_to)
        LOGGER.debug("LSGML1:a %d", len(balls_in_range_tuple[0]))
        LOGGER.debug("LSGML1:a1 %s", str(balls_in_range_tuple[0]))
        sets_of_balls = lottery.get_sets_of_balls()
        # Returns one set in a list
        num_balls = sets_of_balls[0].get_num_balls()
        LOGGER.info("LSGML1:a: NUM BALLS %d", num_balls)
        frequency_of_balls = frequency(num_balls, balls_in_range_tuple[0])
        LOGGER.debug(frequency_of_balls)
        num_likley = 3
        if num_balls > 20:
            num_likley = 7
        self._main_balls_most_probable = most_common_balls(
            frequency_of_balls, num_likley)
        # print("Most likely", self._main_balls_most_probable)
        self._main_balls_least_probable = least_common_balls(
            frequency_of_balls, num_likley)
        # print("Least likely", self._main_balls_least_probable)

    def get_most_probable(self):
        """ Returns a tuple of (main stats_method).
            NOTE: Must return list of at least 6 for ticket
            generation methods to work.
        """
        LOGGER.debug("LSGML1:gmp: returning...")
        LOGGER.debug(self._main_balls_most_probable)
        return (self._main_balls_most_probable)

    def get_least_probable(self):
        """ Returns a tuple of (main stats_method).
            NOTE: Must return list of at least 6 for ticket
            generation methods to work.
        """
        LOGGER.debug("LSGML1:glp: returning...")
        LOGGER.debug(self._main_balls_least_probable)
        return (self._main_balls_least_probable)


class LotteryLotto(Lottery):
    """ The UK Lotto lottery. """

    def __init__(self):
        super(LotteryLotto, self).__init__()
        self._name = "Lotto"
        self._sets_of_balls = 1
        self._main_balls = SetOfBalls("main", 59)
        # Parsers
        self._available_parsers.append(LotteryParserLottoNL())
        self._available_parsers.append(LotteryParserLottoMW())
        # Ticket generation methods
        self._line_generation_methods.append(
            LotteryTicketLineGeneratorLotto1())
        self._line_generation_methods.append(
            LotteryTicketLineGeneratorLotto1A())
        self._line_generation_methods.append(
            LotteryTicketLineGeneratorLotto2())
        self._line_generation_methods.append(
            LotteryTicketLineGeneratorLotto2A())
        # Stats
        self._stats_generation_methods.append(
            LotteryStatsGenerationMethodLotto1())
        # Debug
        LOGGER.info("Initialised parsers:")
        for parser in self._available_parsers:
            LOGGER.info(parser.name)

    def get_new_draw(self):
        """ Return a new draw. """
        return LottoDraw()

    def get_sets_of_balls(self):
        """ Returns a list containing all sets of ball info for this lottery.
        """
        return [self._main_balls]

    def get_balls_in_date_range(self, oldest_date, newest_date):
        """ Return a tuple containing the sets of balls in the give date
            range.
            This info is used for frequency analysis.  The bonus ball is
            selected using the same machine and is the last one selected.
            Therefore there is nothing special about the bonus ball.
        """
        LOGGER.debug("LL:gbidr, len %d, from %s to %s", len(self.draws),
                     str(oldest_date), str(newest_date))
        main_balls = []
        for lottery_draw in self.draws:
            LOGGER.debug("LL:gbidr, lottery draw date %s",
                         str(lottery_draw.draw_date))
            gt_oldest = lottery_draw.draw_date >= oldest_date
            lt_newest = lottery_draw.draw_date <= newest_date
            LOGGER.debug("LL:gbidr, lottery draw date %s, gt %d, lt %d",
                         str(lottery_draw.draw_date), gt_oldest, lt_newest)
            if gt_oldest and lt_newest:
                LOGGER.debug("LL:gbidr, draw: %d", lottery_draw.main_balls[0])
                # Append all main balls to the given list
                main_balls.append(lottery_draw.main_balls[0])
                main_balls.append(lottery_draw.main_balls[1])
                main_balls.append(lottery_draw.main_balls[2])
                main_balls.append(lottery_draw.main_balls[3])
                main_balls.append(lottery_draw.main_balls[4])
                main_balls.append(lottery_draw.main_balls[5])
                main_balls.append(lottery_draw.bonus_ball)
        return (main_balls, [])
