"""
Utility functions for dealing with Lottery csv files.
"""

import copy
import datetime

class SetOfBalls:
    """ Information about the set of balls. """
    _num_balls = 0
    _name = ""

    def __init__(self, name, num_balls):
        """ Initialises the class. """
        self._num_balls = num_balls
        self._name = name

    def get_num_balls(self):
        """ Return the number of balls in the set. """
        return self._num_balls

    def get_name(self):
        """ Return the number of balls in the set. """
        return self._name


def convert_str_to_date(date_str):
    """ Converts a string to a date type """
    # print("date_str", date_str)
    formatter_string = "%d-%b-%Y"
    date_object = datetime.datetime.strptime(date_str, formatter_string).date()
    return date_object

def frequency(max_num, ball_list):
    """ Creates a list of frequencies from the given ball list """
    # print(ball_list)
    frequency_of_balls = []
    for ball_number in range(1, max_num + 1):
        ball_count = 0
        for ball in ball_list:
            # print(ball_number, ball_count, ball)
            if ball_number == ball:
                ball_count += 1
        frequency_of_balls.append((ball_number, ball_count))
    return frequency_of_balls

def most_likely_balls(ball_set_in, max_balls):
    """ Select most likely balls. """
    # expected = [(9, 12), (2, 10), (3, 10)]
    # print("expected", expected)
    # Copy the ball set to stop the given ball set being modified
    ball_set = copy.deepcopy(ball_set_in)
    most = []
    for num_balls in range(0, max_balls + 1):
        # Find the highest ball value in the set
        highest_value = 0
        highest_index = 0
        for index in range(0, len(ball_set)):
            ball_set_info = ball_set[index]
            if highest_value < ball_set_info[1]:
                highest_value = ball_set_info[1]
                highest_index = index
        # Found the first ball in the list with the highest value
        # print("Highest", ball_set[highest_index])
        most.append(ball_set[highest_index])
        del ball_set[highest_index]
    return most

def least_likely_balls(ball_set_in, max_balls):
    """ Select least likely balls. """
    # expected = [(1, 5), (7, 3), (10, 5)]
    # print("expected", expected)
    # Copy the ball set to stop the given ball set being modified
    ball_set = copy.deepcopy(ball_set_in)
    least_likely = []
    for num_balls in range(0, max_balls + 1):
        # Find the lowest ball value in the set
        lowest_value = 1000
        lowest_index = 0
        for index in range(0, len(ball_set)):
            ball_set_info = ball_set[index]
            if lowest_value > ball_set_info[1]:
                lowest_value = ball_set_info[1]
                lowest_index = index
        # Found the first ball in the list with the highest value
        # print("Lowest", ball_set[lowest_index])
        least_likely.append(ball_set[lowest_index])
        del ball_set[lowest_index]
    return least_likely

