#!/usr/bin/python3.6

import collections
from lottery import Lottery, LotteryTicket, LotteryDraw
from lottery_utils import SetOfBalls, convert_str_to_date, frequency

# TODO Add sort to this class
# TODO Add function to compare results with ticket and produce scores.
class EuroMillionsLine:
    """ Represents a line of lottery numbers. """
    def __init__(self):
        """ Creates two sets of balls with the right number of balls. """
        self.main_balls = []
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.lucky_stars = []
        self.lucky_stars.append(0)
        self.lucky_stars.append(0)

    def sort(self):
        """ Sorts the line into ascending numerical order. """
        self.main_balls.sort()
        self.lucky_stars.sort()

    def score(self, line):
        """ Scores the given line against self.
            Returns a tuple of the number of matches for each ball set.
        """
        main_matched = 0
        for ii in range(0, len(self.main_balls)):
            if self.main_balls[ii] == line.main_balls[ii]:
                main_matched += 1
        lucky_matched = 0
        for ii in range(0, len(self.lucky_stars)):
            if self.lucky_stars[ii] == line.lucky_stars[ii]:
                lucky_matched += 1
        return (main_matched, lucky_matched)

class EuroMillionsCSVDraw:
    """ Groups draw date and lottery line."""
    def __init__(self):
        self.draw_date = 0
        self.line = EuroMillionsLine()

class LotteryTicketEuroMillions(LotteryTicket):
    """ Class representing a EuroMillionsTicket.
    Only implements lottery specific functions. 
    """

    def generate_lines(self, num_lines, ball_stats):
        """ Generates the given number of lines from the ball stats. """
        print("Gen lines EM", num_lines, "Ignored!")
        # for ii in range(0, num_lines):
        print(ball_stats[0])
        print(ball_stats[1])
        print(ball_stats[2])
        print(ball_stats[3])
        print(ball_stats[4])
        print(ball_stats[5])
        # Use least common balls
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[2][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[5][ii][0]
        line.sort()
        self._lines.append(line)
        # Use the same line but with the alternatives
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[2][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[5][ii][0]
        line.main_balls[4] = ball_stats[2][5][0]
        line.lucky_stars[1] = ball_stats[5][2][0]
        line.sort()
        self._lines.append(line)
        # Use most common balls
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[1][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[4][ii][0]
        line.sort()
        self._lines.append(line)
        # Use the same line but with the alternatives
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[1][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[4][ii][0]
        line.main_balls[4] = ball_stats[1][5][0]
        line.lucky_stars[1] = ball_stats[4][2][0]
        line.sort()
        self._lines.append(line)

    def print_ticket(self):
        """ Prints the ticket. """
        print("Ticket date EM:", self._draw_date, "Num Lines", len(self._lines))
        for line in self._lines:
            print('Main {0:2d} {1:2d} {2:2d} {3:2d} {4:2d}  Lucky stars {5:2d} {6:2d}'.format(\
                line.main_balls[0], line.main_balls[1], line.main_balls[2], line.main_balls[3], line.main_balls[4], \
                line.lucky_stars[0], line.lucky_stars[1]))


class LotteryEuroMillions(Lottery):
    """ The Euro Millions lottery. """
    _main_balls = SetOfBalls("main", 50)
    _lucky_star_balls = SetOfBalls("lucky stars", 12)

    def __init__(self):
        self._name = "EuroMillions"
        self._sets_of_balls = 2

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        return str(row[6]) == 'Lucky Star 1'

    def get_ball_sets(self):
        """ Returns all sets of balls for this lottery. """
        return (self._main_balls, self._lucky_star_balls)

    def parse_row(self, row):
        """ Read row data and copy into EuroMillionsCSV class """
        draw = EuroMillionsCSVDraw()
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
        self.results.append(draw)
        self._num_draws += 1

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date 
        range. """
        main_balls = []
        lucky_stars = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                """ Appends all main balls to the given list """
                main_balls.append(lottery_draw.line.main_balls[0])
                main_balls.append(lottery_draw.line.main_balls[1])
                main_balls.append(lottery_draw.line.main_balls[2])
                main_balls.append(lottery_draw.line.main_balls[3])
                main_balls.append(lottery_draw.line.main_balls[4])
                """ Appends all lucky star balls to the given list """
                lucky_stars.append(lottery_draw.line.lucky_stars[0])
                lucky_stars.append(lottery_draw.line.lucky_stars[1])
        return (main_balls, lucky_stars)

    def get_draw(self, draw_date, main_1, main_2, main_3, main_4, main_5, lucky_1, lucky_2):
        lottery_draw = EuroMillionsCSVDraw(draw_date, main_1, main_2, \
                                            main_3, main_4, main_5, \
                                            lucky_1, lucky_2)
        return lottery_draw

    def print_draw(self, lottery_draw):
        """ Print the given draw. """
        line = lottery_draw.line
        print('Date {0}: Main {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}  Lucky stars {6:2d} {7:2d}'.format(\
            lottery_draw.draw_date, \
            line.main_balls[0], line.main_balls[1], line.main_balls[2], line.main_balls[3], line.main_balls[4], \
            line.lucky_stars[0], line.lucky_stars[1]))

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        ticket = LotteryTicketEuroMillions(next_lottery_date)
        ticket.generate_lines(num_lines, ball_stats)
        # Add lines here
        return ticket

