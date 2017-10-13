#!/usr/bin/python3.6
""" National Lottery Lotto classes.

NOTE: fewer winners on this lottery than Euro-millions.
Consider individual ball sets?
More data needs to be analysed to get enough statistical data.
Possibly consider machines as well.

1. Read ball set and machine data into the draw class. DONE.
2. Work out how to process with the extra info.
   a. Does the ball set make a difference?
   b. Does the machine make a difference?
   c. Do both the machine and the ball set make a difference?

TODO
Ball marking is not working right.
Log winning lines under the line of the ticket it came from.
"""

import calendar
import datetime
import logging

from lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser
from lottery_utils import SetOfBalls, convert_str_to_date


class LottoDraw(LotteryDraw):

    """ Groups draw date and lottery line."""

    def __init__(self):
        super(LottoDraw, self).__init__()
        self.main_balls = []
        self.ball_set = 0
        self.machine = ""
        # 6 main balls
        for _ in range(0, 6):
            self.main_balls.append(0)
        self.bonus_ball = 0;

    def as_string(self):
        """ Returns this draw as a string. """
        str1 = '{0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  {5:2d}'.format(
            self.main_balls[0], self.main_balls[1], self.main_balls[2],
            self.main_balls[3], self.main_balls[4], self.main_balls[5])
        str2 = 'Bonus ball {0:2d}  Ball set {1:2d}  Machine {2}'.format(
            self.bonus_ball, self.ball_set, self.machine)
        return self.draw_date.isoformat() + ' Main balls: ' + str1 + '  ' + str2


class LottoTicketLine:

    """ Represents a line of lottery numbers on a ticket. """

    def __init__(self):
        """ Creates one sets of balls with the right number of balls. """
        self.main_balls = []
        # 6 main balls
        for _ in range(0, 6):
            self.main_balls.append(0)

    @staticmethod
    def _mark_ball(line_string, main):
        """ Mark winning balls with *. """
        main_ball_offset = 8
        if main >= 0 and main <= 5:
            index = main_ball_offset + (main * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        # logging.info(line_string)
        return line_string

    def sort(self):
        """ Sorts the line into ascending numerical order. """
        self.main_balls.sort()

    def as_string(self):
        """ Return this line as a string. """
        return 'Line: {0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  {5:2d}'.format(
            self.main_balls[0], self.main_balls[1], self.main_balls[2],
            self.main_balls[3], self.main_balls[4], self.main_balls[5])

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
        1 - 0 as not applicable
        2 - True if the line is a winner.
        3 - string of the line with the matching balls shown
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
        return (main_matched, 0, self._is_winner(main_matched), matching_str)


class LotteryTicketLotto(LotteryTicket):

    """ Class representing a LottoTicket.
        Only implements lottery specific functions.
    """
    def generate_line_most_frequent_main(self, ball_stats):
        """ Generates one line from the ball stats.
            Uses the most frequently occurring balls.
        """
        line = LottoTicketLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[1][iterator][0]
        line.sort()
        return line

    def generate_line_most_frequent_alternate(self, ball_stats):
        """ Generates one line from the ball stats.
            Uses the most frequently occurring balls.
        """
        line = LottoTicketLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[1][iterator][0]
        line.main_balls[5] = ball_stats[1][5][0]
        line.sort()
        return line

    def generate_line_least_frequent_main(self, ball_stats):
        """ Generates one line from the ball stats.
        Uses the least frequently occurring balls.
        """
        # Use least common balls
        line = LottoTicketLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[2][iterator][0]
        line.sort()
        return line

    def generate_line_least_frequent_alternate(self, ball_stats):
        """ Generates one line from the ball stats.
        Uses the least frequently occurring balls with an alternate.
        """
        line = LottoTicketLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[2][iterator][0]
        line.main_balls[5] = ball_stats[2][5][0]
        line.sort()
        return line

    def generate_lines(self, num_lines, ball_stats):
        """ Generates the given number of lines from the ball stats. """
        debug_on = True
        if debug_on:
            logging.info("Gen lines EM " + str(num_lines) + " Ignored!")
            # for iterator in range(0, num_lines):
            logging.info(ball_stats[0])
            logging.info(ball_stats[1])  # Most
            logging.info(ball_stats[2])  # Least
        self.lines.append(self.generate_line_most_frequent_main(ball_stats))
        self.lines.append(self.generate_line_most_frequent_alternate(ball_stats))
        self.lines.append(self.generate_line_least_frequent_main(ball_stats))
        self.lines.append(self.generate_line_least_frequent_alternate(ball_stats))


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
        logging.info(self.name + row[7])
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


class LotteryParserLottoMW(LotteryParser):

    """ Parses the CSV data from http://lottery.merseyworld.com/Winning_index.html. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserLottoMW, self).__init__()
        self.name = 'Lotto MerseyWorld'

    def check_header(self, row):
        """ Returns True if this is merseyworld lotto. 
        Unique values are Draw number and N1. """
        logging.info(self.name + " '" + row[0] + "'" + row[5] + "'")
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
        draw.jackpot = int(row[12])
        draw.jackpot_wins = int(row[13])
        draw.machine = row[14]
        draw.ball_set = int(row[15])


class LotteryLotto(Lottery):

    """ The Euro Millions lottery. """

    def __init__(self):
        super(LotteryLotto, self).__init__()
        self._name = "Lotto"
        self._sets_of_balls = 1
        self._main_balls = SetOfBalls("main", 59)
        self._available_parsers.append(LotteryParserLottoNL())
        self._available_parsers.append(LotteryParserLottoMW())
        # Debug
        logging.info("Initialised parsers:")
        for parser in self._available_parsers:
            logging.info(parser.name)

    def parse_row(self, row):
        """ Read row data and copy into LottoCSV class.
        """
        draw = LottoDraw()
        if self._parser:
            self._parser.parse_row(row, draw)
        else:
            print("ERROR: parser is", self._parser)
            sys.exit()
        self.results.append(draw)
        self._num_draws += 1

    def get_sets_of_balls(self):
        """ Returns a list containing all sets of ball info for this lottery.
        """
        return [self._main_balls]

    def get_balls_in_date_range(self, date_from, date_to):
        """ Return a tuple containing the sets of balls in the give date
            range.
            This info is used for frequency analysis.  The bonus ball is 
            selected using the same machine and is the last one selected.
            Therefore there is nothing special about the bonus ball.
        """
        main_balls = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and \
                    lottery_draw.draw_date <= date_to:
                main_balls.append(lottery_draw.main_balls[0])
                main_balls.append(lottery_draw.main_balls[1])
                main_balls.append(lottery_draw.main_balls[2])
                main_balls.append(lottery_draw.main_balls[3])
                main_balls.append(lottery_draw.main_balls[4])
                main_balls.append(lottery_draw.main_balls[5])
                main_balls.append(lottery_draw.bonus_ball)
        return (main_balls, [])

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        ticket = LotteryTicketLotto(next_lottery_date)
        ticket.generate_lines(num_lines, ball_stats)
        # Add lines here
        return ticket

    @staticmethod
    def test_draw_against_ticket(lottery_draw, ticket):
        """ Returns the number of matches for each line of the given ticket
            against the given draw.
        """
        best_score = (0, 0, False, [])
        winning_lines = []

        for line in ticket.lines:
            score = line.score(lottery_draw)
            # logging.info(score)
            if score == best_score:
                winning_lines.append(line)
            if score[0] > best_score[0] or score[1] > best_score[1]:
                best_score = score
                winning_lines.clear()
                winning_lines.append(line)
        return (best_score, winning_lines, lottery_draw)
