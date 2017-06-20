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
D Print out rolling n days frequency figures.
D Print out the most likely numbers for the next n draws.  
Print out lottery ticket numbers using various different methods so they can be compared
against the real results. 
"""

import datetime

from lottery_results import LotteryResults
from lottery_utils import frequency, most_likely_balls, least_likely_balls

def ball_stats_in_date_range(results, date_from, date_to):
    """ Prints the statistics about the balls for all ball sets for the given range. """
    # print("Ball frequency from", date_from, "to", date_to)
    balls = results.get_lottery().get_balls_in_date_range(date_from, date_to)
    ball_sets = results.get_lottery().get_ball_sets()
    ii = 0
    ball_stats = []
    for ball_set in ball_sets:
        # print("Set of balls:", ball_set.get_name())
        num_balls = ball_set.get_num_balls()
        frequency_of_balls = frequency(num_balls, balls[ii])
        # print(frequency_of_balls)
        most_likely = most_likely_balls(frequency_of_balls, 2)
        # print("Most likely", most_likely)
        least_likely = least_likely_balls(frequency_of_balls, 2)
        # print("Least likely", least_likely)
        ii += 1
        ball_stats.append((ball_set, frequency_of_balls, most_likely, least_likely))
    return ball_stats

def print_ticket_for_next_lottery(next_lottery_date, results, stats):
    """ Prints a ticket with a number of lines for the next draw. """
    print("Ticket for next lottery:")
    lottery = results.get_lottery()
    ticket = lottery.generate_ticket(next_lottery_date, 5, stats)
    lottery.print_ticket(ticket)

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
    earliest_date = date_range[0]
    latest_date = earliest_date + datetime.timedelta(days=150)
    next_lottery_date = latest_date + datetime.timedelta(days=1)
    # Print ball stats of balls in range
    stats = ball_stats_in_date_range(results, earliest_date, latest_date)
    # Print numbers for tickets
    print_ticket_for_next_lottery(next_lottery_date, results, stats)
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
