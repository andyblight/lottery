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

EURO_STATS_NAME = "Euro1"
LOTTO_STATS_NAME = "Lotto1"


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
    end_index = len(lottery_dates) - 1
    most_recent = lottery_dates[end_index]
    short_range = lottery_dates[end_index - short_range_offset]
    long_range = lottery_dates[end_index - long_range_offset]
    return (most_recent, short_range, long_range)


def generate_ticket(lottery_results, chosen_stats_method, line_method_names):
    """ Generate a ticket using the selected stats method and line generation
        methods.
    """
    # Use one date range.
    date_range = generate_date_range(lottery_results)
    logging.debug("gt: date_range %s", str(date_range))
    stats_methods = lottery_results.get_lottery().\
        get_stats_generation_methods()
    # Select stats generation method.
    for stats_method in stats_methods:
        logging.debug("gt: stats %s", stats_method.name)
        if stats_method.name == chosen_stats_method:
            # Analyse results
            stats_method.analyse(lottery_results, date_range)
            # Generate ticket
            ticket = lottery_results.generate_ticket(stats_method,
                                                     line_method_names)
            ticket.print(True)
            break


def run():
    """ Reads the data from the given file into the results instance """
    args = handle_parameters()
    setup_logging(args)
    results = LotteryResults()
    results.load_file(args.filename)
    lottery_name = results.get_lottery().get_name()
    if lottery_name == "EuroMillions":
        euro_line_method_names = []
        euro_line_method_names.append("Euro1")
        euro_line_method_names.append("Euro2")
        euro_line_method_names.append("Euro3")
        euro_line_method_names.append("Euro4")
        generate_ticket(results, EURO_STATS_NAME, euro_line_method_names)
    elif lottery_name == "Lotto":
        lotto_line_method_names = []
        lotto_line_method_names.append("Lotto1")
        lotto_line_method_names.append("Lotto2")
        generate_ticket(results, LOTTO_STATS_NAME, lotto_line_method_names)
    else:
        logging.error("Unknown lottery %s", lottery_name)


if __name__ == "__main__":
    run()
