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

Most likely seems to get it right more often than least likely.

Implement this "Choose from the balls that haven't come up in the last 8 weeks."
- Ball frequency for last 8 weeks.
- Create list of balls that do not appear in the ball frequency list.
- Create ticket from that list.
Seems to be some sort of sweet spot with delta 35-40.


TASKS
Fix TODO!!! output.
Route output to file instead of stdout.
One file per lottery. 
Do I change the script to just do one lottery at a time based on the input file?
Wrap the tool in a bash script that captures the output.

Need some way to summarise the methods and plot results against those methods.
Store the intermediate data and analyse afterwards. 
What info do I need?
 Date of draw.
 Method used to generate winning line.
 Number of matching balls. 
 
Seems like I need to create an analysis method class so I can print the method
out.

NOTES
Last two lines on ticket seem to come up more often than not.

"""

import argparse
import datetime
import logging
import os

from lottery_results import LotteryResults
from lottery_utils import frequency, most_common_balls, least_common_balls

_winning_draws = []


def handle_parameters():
    """ Process the command line arguments.  Returns the values of the 
    arguments in a argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(
        description=''' Generates statistics and suggests tickets to buy based
                        on the given CSV files.''')
    parser.add_argument('-v', '--verbose', help='''verbose output.''')
    parser.add_argument(
        "filename", help='CSV file or files to process')
    return parser.parse_args()


def ball_stats_in_date_range(results, date_from, date_to):
    """ Returns the statistics about the balls for all ball sets for the given range. """
    # print("Ball frequency from", date_from, "to", date_to)
    balls = results.get_lottery().get_balls_in_date_range(date_from, date_to)
    sets_of_balls = results.get_lottery().get_sets_of_balls()
    ii = 0
    ball_stats = []
    logging.info(balls)
    for ball_set in sets_of_balls:
        # print("Set of balls:", ball_set.get_name())
        num_balls = ball_set.get_num_balls()
        logging.info("NUM BALLS", num_balls, "ii", ii)
        frequency_of_balls = frequency(num_balls, balls[ii])
        # print(frequency_of_balls)
        num_likley = 3
        if num_balls > 20:
            num_likley = 6
        most_likely = most_common_balls(frequency_of_balls, num_likley)
        # print("Most likely", most_likely)
        least_likely = least_common_balls(frequency_of_balls, num_likley)
        # print("Least likely", least_likely)
        ii += 1
        ball_stats.append(frequency_of_balls)
        ball_stats.append(most_likely)
        ball_stats.append(least_likely)
    return ball_stats


def generate_ticket_for_next_lottery(next_lottery_date, results, stats):
    """ Prints a ticket with a number of lines for the next draw. """
    # print("Generate ticket for next lottery:")
    lottery = results.get_lottery()
    return lottery.generate_ticket(next_lottery_date, 5, stats)


def print_lottery_ticket(results, ticket):
    """ Prints a ticket with a number of lines for the next draw. """
    logging.info("Ticket for next lottery:")
    lottery = results.get_lottery()
    lottery.print_ticket(ticket)


def print_matches_for_draws_in_date_range(results, date_from, date_to, ticket):
    """ For each draw in the given data range,
            prints the draw
            prints the number of matches in each line of the ticket.
    """
    logging.info("Draws in range from " +
                 date_from.isoformat() + " to " + date_to.isoformat())
    lottery_draws = results.get_lottery().get_draws_in_date_range(
        date_from, date_to)
    for lottery_draw in lottery_draws:
        results.get_lottery().print_draw(lottery_draw)
        test_results = results.get_lottery().test_draw_against_ticket(
            lottery_draw, ticket)
        best_score = test_results[0]
        winning_lines = test_results[1]
        draw = test_results[2]
        if best_score[2]:
            logging.info("WINNER!!!!")
            logging.info("Best score", best_score, "for lines")
            _winning_draws.append((draw, best_score[3]))
        else:
            logging.info("No winners")
        for line in winning_lines:
            logging.info(line.as_string())


def process_data_in_range(results, analysis_start, analysis_end):
    """ """
    next_lottery_date = analysis_end + datetime.timedelta(days=1)
    # Print ball stats of balls in range
    stats = ball_stats_in_date_range(results, analysis_start, analysis_end)
    # Print numbers for tickets
    ticket = generate_ticket_for_next_lottery(
        next_lottery_date, results, stats)
    print_lottery_ticket(results, ticket)
    # Print draws after end of chosen range
    draw_date_to = analysis_end + datetime.timedelta(days=14)
    draw_date_from = analysis_end + datetime.timedelta(days=1)
    print_matches_for_draws_in_date_range(
        results, draw_date_from, draw_date_to, ticket)


def print_summary(results):
    """ Prints summary of results.
    Draw dates that contain winners.
    """
    _draws = list(sorted(set(_winning_draws)))
    logging.info('.')
    logging.info("SUMMARY")
    logging.info(len(_draws), "winning draws:")
    for draw in _draws:
        logging.info(draw[0].draw_date, draw[1])


def process_data(results):
    """ Print range of  """
    logging.info('.')
    logging.info("Lottery name:", results.get_lottery().get_name())
    date_range = results.get_lottery().get_date_range()
    logging.info("Results in file from", date_range[0].isoformat(
    ), "to", date_range[1].isoformat())
    #test_start = [100, 90, 80, 70, 60, 40]
    #test_delta = [60, 70, 80, 90, 100, 120]
    # Start range
    # for ii in range(0, len(test_start)):
    #    print()  # Blank line to separate output
    #    print("Start", test_start[ii], "delta", test_delta[ii])
    #    analysis_start = date_range[0] + + datetime.timedelta(test_start[ii])
    #    analysis_end = analysis_start + datetime.timedelta(test_delta[ii])
    #    process_data_in_range(results, analysis_start, analysis_end)
    #print("Not appeared in delta")
    test_delta = [20, 25, 30, 35, 40, 45, 50, 55, 60]
    end_date = date_range[0] + datetime.timedelta(120)
    analysis_start = results.get_lottery().get_first_lottery_date()
    while analysis_start < end_date:
        for delta in range(0, len(test_delta)):
            logging.info('.')
            logging.info("Start", analysis_start, "delta", test_delta[delta])
            analysis_end = analysis_start + \
                datetime.timedelta(test_delta[delta])
            process_data_in_range(results, analysis_start, analysis_end)
        analysis_start = results.get_lottery().get_next_lottery_date()
    print_summary(results)
    # Print next ticket
    analysis_end = date_range[1]
    analysis_start = analysis_end - datetime.timedelta(35)
    process_data_in_range(results, analysis_start, analysis_end)


def run():
    """ Reads the data from the given file into the results instance """
    args = handle_parameters()
    split_filename = os.path.splitext(args.filename)
    log_filename = split_filename[0] + '.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    logging.info('Started')
    logging.info(args)
    results = LotteryResults()
    results.load_file(args.filename)
    process_data(results)


if __name__ == "__main__":
    run()
