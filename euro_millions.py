#!/usr/bin/python3.6

import collections
from lottery import Lottery, LotteryDraw
from lottery_utils import SetOfBalls, convert_str_to_date, frequency

EuroMillionsDraw = collections.namedtuple('EuroMillionsDraw', \
        ['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
        'lucky_1', 'lucky_2'])
    
class LotteryDrawEuroMillions:
    """
    A lottery draw is the sets or sets of balls.
    """
    # def __init__(self): 
    
class LotteryTicketEuroMillions:
    """
    """
    _draw_date = 0
    _lines = []
    
    def __init__(self, draw_date):
        _draw_date = draw_date

    def add_lines(self, num_lines, ball_stats):
        """ Adds the given lines to the ticket using the ball_stats. """
        for ii in range(0, num_lines):
            main_1 = 0
            main_2 = 0
            main_3 = 0
            main_4 = 0
            main_5 = 0
            lucky_1 = 0
            lucky_2 = 0
            line = EuroMillionsDraw(_draw_date, main_1, main_2, \
                                    main_3, main_4, main_5, \
                                    lucky_1, lucky_2)
            ticket.append(lottery_draw)
        return (ticket)

    def print_ticket(self, ticket):
        """ Prints the given ticket. """
        print("Ticket date", _draw_date)
        for line in lines:
            print('Main {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}  Lucky stars {6:2d} {7:2d}'.format( \
                line.main_1, line.main_2, line.main_3, line.main_4, line.main_5, \
                line.lucky_1, line.lucky_2))
        return (0)


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
        euro = EuroMillionsDraw(convert_str_to_date(str(row[0])), \
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

    def get_date_range(self):
        """ Returns a tuple containing the earliest and latest dates in the results. """
        latest = self.results[0].draw_date
        earliest = self.results[self._num_draws - 1].draw_date
        return (earliest, latest)

    def get_draws_in_date_range(self, date_from, date_to):
        """ Returns a tuple of lottery_draws in the give date range. """
        lottery_draws = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                lottery_draws.append(lottery_draw)
        return lottery_draws

    def get_draw(self, draw_date, main_1, main_2, main_3, main_4, main_5, lucky_1, lucky_2):
        lottery_draw = EuroMillionsDraw(draw_date, main_1, main_2, \
                                        main_3, main_4, main_5, \
                                        lucky_1, lucky_2)
        return lottery_draw
        
    def print_draw(self, lottery_draw):
        """ Print the given draw. """
        print('Date {0}: Main {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}  Lucky stars {6:2d} {7:2d}'.format(\
            lottery_draw.draw_date, lottery_draw.main_1, lottery_draw.main_2, \
            lottery_draw.main_3, lottery_draw.main_4, lottery_draw.main_5, \
            lottery_draw.lucky_1, lottery_draw.lucky_2))

