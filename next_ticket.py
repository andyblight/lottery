#!/usr/bin/python3.6
"""
This file generates a lottery ticket based on the results file given on
the command line.  It uses the same methods as the program evaluate.py but
does no evaluation.
"""

import argparse
import logging
import os

from lottery_results import LotteryResults

STATS_NAME = "Euro1"
TICKET_NAME = "Euro3"


def setup_logging(args):
    """ Set up logging. """
    split_filename = os.path.splitext(args.filename)
    log_filename = split_filename[0] + '-next-ticket.log'
    logging.basicConfig(
        filename=log_filename, filemode='w', level=logging.DEBUG)
    logging.info('Started')
    logging.info(args)


def handle_parameters():
    """ Process the command line arguments.  Returns the values of the
    arguments in a argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(
        description=''' Generates tickets based on the given CSV files.''')
    parser.add_argument('-v', '--verbose', help='''verbose output.''')
    parser.add_argument("filename", help='The CSV file to process')
    return parser.parse_args()


def generate_date_range(results):
    """ Returns the range of dates to use for stats generation.
    The dates are generated backwards from the most recent results.
    The range of dates has the format:
        [(most_recent, short_range, long_range), ...]
    where:
        most_recent = The date of the most "recent" draw.  This date moves from
                      the past to the future to simulate real life.
        short_range = The date in the last few weeks.  Used for most often
                      tests.
        long_range = The date longest in the past.  Used for least often tests.
    """
    # FIXME Each lottery may need different settings.
    short_range_offset = 4  # 2 draws per week * 2 weeks
    long_range_offset = 40  # 2 draws per week * 20 weeks
    # Generate one set of lottery dates
    lottery_dates = []
    results_full_range = results.get_lottery().get_date_range()
    logging.info('Generating dates from ' + results_full_range[0].isoformat() +
                 ' to ' + results_full_range[1].isoformat())
    draws_in_range = results.get_lottery().get_draws_in_date_range(
        results_full_range[0], results_full_range[1])
    # Create list of dates from all results
    for lottery_draw in draws_in_range:
        lottery_dates.append(lottery_draw.draw_date)
    # Generate date tuples
    end_index = len(lottery_dates) - long_range_offset
    most_recent = lottery_dates[end_index]
    short_range = lottery_dates[end_index - short_range_offset]
    long_range = lottery_dates[end_index - long_range_offset]
    return (most_recent, short_range, long_range)


def generate_ticket(lottery_results):
    """ Generate a ticket using the selected stats and ticket generation
    method.
    """
    # Change to one date range.
    date_range = generate_date_range(lottery_results)
    stats_methods = lottery_results.get_lottery().\
        get_stats_generation_methods()
    # Select stats generation method.
    for stats_method in stats_methods:
        logging.debug("gt: stats %s", stats_method.name)
        if stats_method.name == STATS_NAME:
            stats_method.analyse(lottery_results, date_range)
            # Select ticket generation method.
            ticket_methods = lottery_results.get_lottery().\
                get_ticket_generation_methods()
            for ticket_method in ticket_methods:
                logging.debug("gt: ticket %s", ticket_method.name)
                num_lines = 4  # FIXME HACK!!!!
                ticket = ticket_method.generate(date_range[0], num_lines,
                                                stats_method)
                ticket.print(True)
            break


def run():
    """ Reads the data from the given file into the results instance """
    args = handle_parameters()
    setup_logging(args)
    results = LotteryResults()
    results.load_file(args.filename)
    generate_ticket(results)


if __name__ == "__main__":
    run()
