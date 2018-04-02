#!/usr/bin/python3.6

"""
This file generates the next ticket from the lottery CSV file that is passed
as a command line argument.

The analysis is done elsewhere,
"""

import argparse
import datetime
import logging
import os

from lottery_results import LotteryResults
from lottery_utils import frequency, most_common_balls, least_common_balls


def handle_parameters():
    """ Process the command line arguments.  Returns the values of the
    arguments in a argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(
        description=''' Suggests a lottery tickets based on the data in the'''
                    '''given CSV files.''')
    parser.add_argument(
        "filename", help='CSV file or files to process')
    return parser.parse_args()


def ball_stats_in_date_range(results, date_from, date_to):
    """ Returns the statistics about the balls for all ball sets for the given
        range.
    """
    # logging.info("Ball frequency from", date_from, "to", date_to)
    balls = results.get_lottery().get_balls_in_date_range(date_from, date_to)
    sets_of_balls = results.get_lottery().get_sets_of_balls()
    iterator = 0
    ball_stats = []
    logging.info(balls)
    for ball_set in sets_of_balls:
        # logging.info("Set of balls:", ball_set.get_name())
        num_balls = ball_set.get_num_balls()
        str_log = "NUM BALLS " + str(num_balls) + " iterator " + str(iterator)
        logging.info(str_log)
        frequency_of_balls = frequency(num_balls, balls[iterator])
        # logging.info(frequency_of_balls)
        num_likley = 3
        if num_balls > 20:
            num_likley = 6
        most_likely = most_common_balls(frequency_of_balls, num_likley)
        # logging.info("Most likely", most_likely)
        least_likely = least_common_balls(frequency_of_balls, num_likley)
        # logging.info("Least likely", least_likely)
        iterator += 1
        ball_stats.append(frequency_of_balls)
        ball_stats.append(most_likely)
        ball_stats.append(least_likely)
    return ball_stats


def generate_ticket_next_lottery(next_lottery_date, results, stats):
    """ Prints a ticket with a number of lines for the next draw. """
    # logging.info("Generate ticket for next lottery:")
    lottery = results.get_lottery()
    return lottery.generate_ticket(next_lottery_date, 5, stats)


def print_lottery_ticket(ticket, printout):
    """ Prints a ticket with a number of lines for the next draw. """
    log_str = "Ticket for next lottery:"
    if printout:
        print(log_str)
    else:
        logging.info(log_str)
    ticket.print_ticket(printout)


def print_matches_draws_date_range(results, date_from, date_to, ticket,
                                   winning_draws):
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
            logging.info("Best score" + str(best_score) + "for lines")
            winning_draws.append((draw, best_score[3]))
        else:
            logging.info("No winners")
        for line in winning_lines:
            logging.info(line.as_string())


def process_data_in_range(results, analysis_start, analysis_end, winning_draws,
                          printout):
    """ Process data in the given range. """
    next_lottery_date = analysis_end + datetime.timedelta(days=1)
    # Print ball stats of balls in range
    stats = ball_stats_in_date_range(results, analysis_start, analysis_end)
    # Print numbers for tickets
    ticket = generate_ticket_next_lottery(
        next_lottery_date, results, stats)
    # Always write to log
    print_lottery_ticket(ticket, False)
    if printout:
        print_lottery_ticket(ticket, True)
    if not printout:
        # Print draws after end of chosen range
        draw_date_to = analysis_end + datetime.timedelta(days=14)
        draw_date_from = analysis_end + datetime.timedelta(days=1)
        print_matches_draws_date_range(
            results, draw_date_from, draw_date_to, ticket, winning_draws)


def print_summary(winning_draws):
    """ Prints summary of winning draws. """
    _draws = list(sorted(set(winning_draws)))
    logging.info('.')
    logging.info("SUMMARY")
    logging.info(str(len(_draws)) + " winning draws:")
    for draw in _draws:
        log_str = draw[0].draw_date.isoformat()
        log_str += draw[1]
        logging.info(log_str)


def process_data(results):
    """ Print range of  """
    winning_draws = []
    # Print next ticket
    date_range = results.get_lottery().get_date_range()
    analysis_end = date_range[1]
    analysis_start = analysis_end - datetime.timedelta(35)
    process_data_in_range(results, analysis_start, analysis_end, winning_draws,
                          True)


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
