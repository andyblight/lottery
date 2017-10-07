#!/usr/bin/python3.6
""" Implementation classes for the EuroMillions lottery. """
import calendar
import logging
import sys

from lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser
from lottery_utils import SetOfBalls, convert_str_to_date


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
        main_str = 'Main {0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  '.format(
            self.main_balls[0], self.main_balls[1], self.main_balls[
                2], self.main_balls[3], self.main_balls[4])
        lucky_str = 'Lucky stars {0:2d}  {1:2d} '.format(
            self.lucky_stars[0], self.lucky_stars[1])
        return main_str + lucky_str

    @staticmethod
    def _mark_ball_in_string(line_string, main, lucky):
        """ Mark winning balls with *. """
        if main > -1 and main < 5:
            index = 7 + (main * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        if lucky > -1 and lucky < 2:
            index = 39 + (lucky * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        logging.info(line_string)
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

    def score(self, line):
        """ Returns a tuple containing:
        0 - count of main ball matches
        1 - count of lucky star matches
        2 - True if the line is a winner.
        3 - string of the line with the matching balls shown
        """
        main_matched = 0
        lucky_matched = 0
        matching_str = line.as_string()
        for iterator in range(0, len(self.main_balls)):
            if self.main_balls[iterator] == line.main_balls[iterator]:
                main_matched += 1
                matching_str = self._mark_ball_in_string(
                    matching_str, iterator, -1)
        for iterator in range(0, len(self.lucky_stars)):
            if self.lucky_stars[iterator] == line.lucky_stars[iterator]:
                lucky_matched += 1
                matching_str = self._mark_ball_in_string(
                    matching_str, -1, iterator)
        return (main_matched, lucky_matched,
                self._is_winner(main_matched, lucky_matched,), matching_str)


class EuroMillionsDraw(LotteryDraw):

    """ Groups draw date and lottery line."""

    def __init__(self):
        """ Initialises the class. """
        super(EuroMillionsDraw, self).__init__()
        self.draw_number = 0
        self.line = EuroMillionsLine()
        self.jackpot = 0
        self.jackpot_wins = 0

    def __lt__(self, other):
        """ Returns True when self < other.  Test is on draw date. """
        result = False
        if self.draw_date < other.draw_date:
            result = True
        return result


class LotteryTicketEuroMillions(LotteryTicket):

    """ Class representing a EuroMillionsTicket.
    Only implements lottery specific functions.
    """

    def generate_lines(self, num_lines, ball_stats):
        """ Generates the given number of lines from the ball stats. """
        logging.info("Gen lines EM" + str(num_lines) + "Ignored!")
        # for iterator in range(0, num_lines):
        logging.info(ball_stats[0])
        logging.info(ball_stats[1])  # Most
        logging.info(ball_stats[2])  # Least
        logging.info(ball_stats[3])
        logging.info(ball_stats[4])  # Most
        logging.info(ball_stats[5])  # Least
        # Use least common balls
        line = EuroMillionsLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[2][iterator][0]
        for iterator in range(0, len(line.lucky_stars)):
            line.lucky_stars[iterator] = ball_stats[5][iterator][0]
        line.sort()
        self.lines.append(line)
        # Use the same line but with the alternatives
        line = EuroMillionsLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[2][iterator][0]
        for iterator in range(0, len(line.lucky_stars)):
            line.lucky_stars[iterator] = ball_stats[5][iterator][0]
        line.main_balls[4] = ball_stats[2][5][0]
        line.lucky_stars[1] = ball_stats[5][2][0]
        line.sort()
        self.lines.append(line)
        # Use most common balls
        line = EuroMillionsLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[1][iterator][0]
        for iterator in range(0, len(line.lucky_stars)):
            line.lucky_stars[iterator] = ball_stats[4][iterator][0]
        line.sort()
        self.lines.append(line)
        # Use the same line but with the alternatives
        line = EuroMillionsLine()
        for iterator in range(0, len(line.main_balls)):
            line.main_balls[iterator] = ball_stats[1][iterator][0]
        for iterator in range(0, len(line.lucky_stars)):
            line.lucky_stars[iterator] = ball_stats[4][iterator][0]
        line.main_balls[4] = ball_stats[1][5][0]
        line.lucky_stars[1] = ball_stats[4][2][0]
        line.sort()
        self.lines.append(line)


class LotteryParserEuromillionsNL(LotteryParser):

    """ Parses the CSV data from the National Lottery. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserEuromillionsNL, self).__init__()
        self.name = 'EuroMillions National Lottery'

    def check_header(self, row):
        """ Returns True if the header matches """
        logging.info(self.name + " " + str(row[6]))
        return str(row[6]) == 'Lucky Star 1'

    @staticmethod
    def parse_row(row, draw):
        """ Read row data and copy into EuroMillionsCSV class """
        draw.draw_date = convert_str_to_date(str(row[0]))
        line = EuroMillionsLine()
        line.main_balls[0] = int(row[1])
        line.main_balls[1] = int(row[2])
        line.main_balls[2] = int(row[3])
        line.main_balls[3] = int(row[4])
        line.main_balls[4] = int(row[5])
        line.lucky_stars[0] = int(row[6])
        line.lucky_stars[1] = int(row[7])
        draw.line = line


class LotteryParserEuromillionsMW(LotteryParser):

    """ Parses the CSV data from merseyworld.com. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserEuromillionsMW, self).__init__()
        self.name = 'EuroMillions MerseyWorld'

    def check_header(self, row):
        """ Returns True if the header matches """
        logging.info(self.name + " " + str(row[10]))
        return str(row[10]) == 'L1'

    @staticmethod
    def parse_row(row, draw):
        ''' Read row data and copy into EuroMillionsCSV class.
        0  - No.,Day,DD,MMM,YYYY,
        5  - N1,N2,N3,N4,N5,
        10 - L1,L2,Jackpot,Wins
        Day of week is ignored as this can be obtained from the date.
        '''
        month_num = list(calendar.month_abbr).index(row[3])
        draw.draw_date.replace(
            year=int(row[4]), month=month_num, day=int(row[2]))
        line = EuroMillionsLine()
        line.main_balls[0] = int(row[5])
        line.main_balls[1] = int(row[6])
        line.main_balls[2] = int(row[7])
        line.main_balls[3] = int(row[8])
        line.main_balls[4] = int(row[9])
        line.lucky_stars[0] = int(row[10])
        line.lucky_stars[1] = int(row[11])
        draw.line = line
        draw.jackpot = int(row[12])
        draw.jackpot_wins = int(row[13])


class LotteryEuroMillions(Lottery):

    """ The Euro Millions lottery. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryEuroMillions, self).__init__()
        self._name = "EuroMillions"
        self._sets_of_balls = 2
        self._main_balls = SetOfBalls("main", 50)
        self._lucky_star_balls = SetOfBalls("lucky stars", 12)
        self._available_parsers.append(LotteryParserEuromillionsNL())
        self._available_parsers.append(LotteryParserEuromillionsMW())
        # Debug
        logging.info("Initialised parsers:")
        for parser in self._available_parsers:
            logging.info(parser.name)

    def get_sets_of_balls(self):
        """ Returns all sets of balls for this lottery. """
        return [self._main_balls, self._lucky_star_balls]

    def parse_row(self, row):
        """ Read row data and copy into EuroMillionsCSV class. """
        draw = EuroMillionsDraw()
        if self._parser:
            self._parser.parse_row(row, draw)
        else:
            print("ERROR: parser is", self._parser)
            sys.exit()
        self.results.append(draw)
        self._num_draws += 1

    def get_balls_in_date_range(self, date_from, date_to):
        """ Return a tuple containing the sets of balls in the give date
        range. """
        main_balls = []
        lucky_stars = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and \
                    lottery_draw.draw_date <= date_to:
                # Append all main balls to the given list
                main_balls.append(lottery_draw.line.main_balls[0])
                main_balls.append(lottery_draw.line.main_balls[1])
                main_balls.append(lottery_draw.line.main_balls[2])
                main_balls.append(lottery_draw.line.main_balls[3])
                main_balls.append(lottery_draw.line.main_balls[4])
                # Append all lucky star balls to the given list
                lucky_stars.append(lottery_draw.line.lucky_stars[0])
                lucky_stars.append(lottery_draw.line.lucky_stars[1])
        return (main_balls, lucky_stars)

    @staticmethod
    def print_draw(lottery_draw):
        """ Print the given draw. """
        logging.info('Date' + lottery_draw.draw_date.isoformat() +
                     lottery_draw.line.as_string())

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        ticket = LotteryTicketEuroMillions(next_lottery_date)
        ticket.generate_lines(num_lines, ball_stats)
        # Add lines here
        return ticket

    # FIXME This is identical to Lotto except for lottery_draw.line.
    @staticmethod
    def test_draw_against_ticket(lottery_draw, ticket):
        """ Prints out the number of matches for each line of the given ticket
            against the given draw.
        """
        best_score = (0, 0, False, [])
        winning_lines = []

        for line in ticket.lines:
            score = line.score(lottery_draw.line)
            logging.info(score)
            if score == best_score:
                winning_lines.append(line)
            if score[0] > best_score[0] or score[1] > best_score[1]:
                best_score = score
                winning_lines.clear()
                winning_lines.append(line)
        return (best_score, winning_lines, lottery_draw)
