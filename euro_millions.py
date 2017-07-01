#!/usr/bin/python3.6

import collections
from lottery import Lottery, LotteryDraw
from lottery_utils import SetOfBalls, convert_str_to_date, frequency

# TODO Add sort to this class
# TODO Add function to compare results with ticket and produce scores.
class EuroMillionsLine:
    """ """
    main_1 = 0
    main_2 = 0
    main_3 = 0
    main_4 = 0
    main_5 = 0
    lucky_1 = 0
    lucky_2 = 0

    def __init__(self):
        main_1 = 0
        main_2 = 0
        main_3 = 0
        main_4 = 0
        main_5 = 0
        lucky_1 = 0
        lucky_2 = 0


EuroMillionsCSVDraw = collections.namedtuple('EuroMillionsCSVDraw', \
        ['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
        'lucky_1', 'lucky_2'])

class LotteryTicketEuroMillions:
    """
    """
    _draw_date = 0
    _lines = []

    def __init__(self, draw_date):
        # print("Set date EM", draw_date)
        self._draw_date = draw_date

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
        line.main_1 = ball_stats[2][0][0]
        line.main_2 = ball_stats[2][1][0]
        line.main_3 = ball_stats[2][2][0]
        line.main_4 = ball_stats[2][3][0]
        line.main_5 = ball_stats[2][4][0]
        line.lucky_1 = ball_stats[5][0][0]
        line.lucky_2 = ball_stats[5][1][0]
        self._lines.append(line)
        line = EuroMillionsLine()
        line.main_1 = ball_stats[2][0][0]
        line.main_2 = ball_stats[2][1][0]
        line.main_3 = ball_stats[2][2][0]
        line.main_4 = ball_stats[2][3][0]
        line.main_5 = ball_stats[2][5][0]
        line.lucky_1 = ball_stats[5][0][0]
        line.lucky_2 = ball_stats[5][2][0]
        self._lines.append(line)
        # Use most common balls
        line = EuroMillionsLine()
        line.main_1 = ball_stats[1][0][0]
        line.main_2 = ball_stats[1][1][0]
        line.main_3 = ball_stats[1][2][0]
        line.main_4 = ball_stats[1][3][0]
        line.main_5 = ball_stats[1][4][0]
        line.lucky_1 = ball_stats[4][0][0]
        line.lucky_2 = ball_stats[4][1][0]
        self._lines.append(line)
        line = EuroMillionsLine()
        line.main_1 = ball_stats[1][0][0]
        line.main_2 = ball_stats[1][1][0]
        line.main_3 = ball_stats[1][2][0]
        line.main_4 = ball_stats[1][3][0]
        line.main_5 = ball_stats[1][5][0]
        line.lucky_1 = ball_stats[4][0][0]
        line.lucky_2 = ball_stats[4][2][0]
        self._lines.append(line)

    def print_ticket(self):
        """ Prints the ticket. """
        print("Ticket date EM:", self._draw_date, "Num Lines", len(self._lines))
        for line in self._lines:
            print('Main {0:2d} {1:2d} {2:2d} {3:2d} {4:2d}  Lucky stars {5:2d} {6:2d}'.format(\
                line.main_1, line.main_2, line.main_3, line.main_4, line.main_5, \
                line.lucky_1, line.lucky_2))


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
        """ Read row data and copy into EuroMillions tuple """
        euro = EuroMillionsCSVDraw(convert_str_to_date(str(row[0])), \
                                    int(row[1]), int(row[2]), int(row[3]), \
                                    int(row[4]), int(row[5]), int(row[6]), \
                                    int(row[7]))
        self.results.append(euro)
        self._num_draws += 1

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date 
        range. """
        main_balls = []
        lucky_stars = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                """ Appends all main balls to the given list """
                main_balls.append(lottery_draw.main_1)
                main_balls.append(lottery_draw.main_2)
                main_balls.append(lottery_draw.main_3)
                main_balls.append(lottery_draw.main_4)
                main_balls.append(lottery_draw.main_5)
                """ Appends all lucky star balls to the given list """
                lucky_stars.append(lottery_draw.lucky_1)
                lucky_stars.append(lottery_draw.lucky_2)
        return (main_balls, lucky_stars)

    def get_draw(self, draw_date, main_1, main_2, main_3, main_4, main_5, lucky_1, lucky_2):
        lottery_draw = EuroMillionsCSVDraw(draw_date, main_1, main_2, \
                                            main_3, main_4, main_5, \
                                            lucky_1, lucky_2)
        return lottery_draw

    def print_draw(self, lottery_draw):
        """ Print the given draw. """
        print('Date {0}: Main {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}  Lucky stars {6:2d} {7:2d}'.format(\
            lottery_draw.draw_date, lottery_draw.main_1, lottery_draw.main_2, \
            lottery_draw.main_3, lottery_draw.main_4, lottery_draw.main_5, \
            lottery_draw.lucky_1, lottery_draw.lucky_2))

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        ticket = LotteryTicketEuroMillions(next_lottery_date)
        ticket.generate_lines(num_lines, ball_stats)
        # Add lines here
        return ticket

