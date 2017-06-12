#!/usr/bin/python3.6

import collections
from lottery import Lottery, LotteryDraw
from lottery_utils import convert_str_to_date, frequency
from set_of_balls import SetOfBalls

EuroMillionsDraw = collections.namedtuple('EuroMillionsDraw', \
        ['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
        'lucky_1', 'lucky_2'])
    
class LotteryDrawEuroMillions:
    """
    A lottery draw is the sets or sets of balls.
    """
    # def __init__(self): 
    

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

