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

import datetime

from lottery_results import LotteryResults
from lottery_utils import frequency

def frequency_in_date_range(results, date_from, date_to):
    """ TODO """
    print("Ball frequency from", date_from, "to", date_to)
    balls = results.get_lottery().get_balls_in_date_range(date_from, date_to)
    ball_sets = results.get_lottery().get_ball_sets()
    ii = 0
    for ball_set in ball_sets:
        print("Set of balls:", ball_set.get_name())
        num_balls = ball_set.get_num_balls()
        frequency(num_balls, balls[ii])
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
    draw_date_from = date_range[1] - datetime.timedelta(days=30)
    print_draws_in_date_range(results, draw_date_from, draw_date_to)

def run(filename):
    """ Reads the data from the given file into the results instance """
    results = LotteryResults()
    results.load_file(filename)
    process_data(results)

if __name__ == "__main__":
    # execute only if run as a script
    run('euromillions-draw-history.csv')
