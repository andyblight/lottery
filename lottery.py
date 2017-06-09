#!/usr/bin/python3.6

"""
GOAL
Generate statistics on the balls and the draws that can be fed into an
algorithm used to predict the next draw. 
Use 5 months of the 6 months of data to predict the remaining months draws. 

NOTES
Predicting the EuroMillions lucky star balls should be simplest with a 2 out 
of 12 choice.  Focus on that first.
Does the EuroMillions use multiple machines/balls sets?
 
TASKS
Print out rolling n days frequency figures.
Print out the most likely numbers for the next n draws.  

"""

import copy
import datetime

from lottery_results import LotteryResults
from lottery_utils import frequency

def most_likely_balls(ball_set_in, max_balls):
    """ Select most likely balls. """
    expected = [(9, 12), (3, 10), (2, 10)]
    print("expected", expected)
    # Copy the ball set to stop the given ball set being modified
    ball_set = copy.deepcopy(ball_set_in)
    most = []
    for num_balls in range(0, max_balls):
        # Find the highest ball value in the set
        highest_value = 0
        highest_index = 0
        for index in range(0, len(ball_set)):
            ball_set_info = ball_set[index]
            if highest_value < ball_set_info[1]:
                highest_value < ball_set_info[1]
                highest_index = index
        # Found the first ball in the list with the highest value
        print("Highest", ball_set[highest_index])
        most.append(ball_set[highest_index])
        del ball_set[highest_index]
    return most

def least_likely_balls(ball_set, max):
    """ Select least likely balls. """
    expected = [(1, 5), (7, 3), (10, 5)]
    print("expected", expected)
    best_list = []
    return best_list

def frequency_in_date_range(results, date_from, date_to):
    """ TODO """
    print("Ball frequency from", date_from, "to", date_to)
    balls = results.get_lottery().get_balls_in_date_range(date_from, date_to)
    ball_sets = results.get_lottery().get_ball_sets()
    ii = 0
    for ball_set in ball_sets:
        print("Set of balls:", ball_set.get_name())
        num_balls = ball_set.get_num_balls()
        frequency_of_balls = frequency(num_balls, balls[ii])
        print(frequency_of_balls)
        most_likely = most_likely_balls(frequency_of_balls, 2)
        print("Most likely", most_likely)
        least_likely = least_likely_balls(frequency_of_balls, 2)
        print("Least likely", least_likely)
        ii += 1

def print_draws_in_date_range(results, date_from, date_to):
    """ Prints the draws in the given date range. """
    print("Draws in range from", date_from, "to", date_to)
    lottery_draws = results.get_lottery().get_draws_in_date_range(date_from, date_to)
    for lottery_draw in lottery_draws:
        results.get_lottery().print_draw(lottery_draw)

def process_data(results):
    """ TODO """
    print("Lottery name:", results.get_lottery().get_name())
    date_range = results.get_lottery().get_date_range()
    print("Results in file from", date_range[0].isoformat(), "to", date_range[1].isoformat())
    # Print frequency of balls in range
    earliest_date = date_range[0]
    latest_date = earliest_date + datetime.timedelta(days=150)
    frequency_in_date_range(results, earliest_date, latest_date)
    # Print draws after end of chosen range
    draw_date_to = date_range[1]
    draw_date_from = latest_date + datetime.timedelta(days=1)
    print_draws_in_date_range(results, draw_date_from, draw_date_to)

def run(filename):
    """ Reads the data from the given file into the results instance """
    results = LotteryResults()
    results.load_file(filename)
    process_data(results)

if __name__ == "__main__":
    # execute only if run as a script
    run('euromillions-draw-history.csv')
