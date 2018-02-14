#!/usr/bin/python3.6

"""
This file generates statistics about range of results and evaluates the
effectiveness of the generation methods by comparing against future results.

"""

import argparse
import logging
import os

from lottery_results import LotteryResults


class EvaluationResult:
    """ Info about how each method performed. """

    def __init__(self, name="", score=0, loop=0):
        self.name = name
        self.score = score
        self.loop = loop


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


def generate_date_ranges(results):
    """ Returns the range of dates to use for stats generation.

    The most recent 4 draws are excluded to allow evaluation of the stats
    and generation methods.
    The range of dates has the format:
        [(most_recent, short_range, long_range), ...]
    where:
        most_recent = The date of the most "recent" draw.  This date moves from
                      the past to the future to simulate real life.
        short_range = The date in the last few weeks.  Used for most often
                      tests.
        long_range = The date longest in the past.  Used for least often tests.
    The number of tuples returned depends on the number of results given.
    """
    date_ranges = []
    # FIXME Each lottery may need different settings.
    short_range_offset = 4  # 2 draws per week * 2 weeks
    long_range_offset = 40  # 2 draws per week * 20 weeks
    # Generate list of lottery dates
    lottery_dates = []
    results_full_range = results.get_lottery().get_date_range()
    logging.info('Generating dates from ' + results_full_range[0].isoformat() +
                 ' to ' + results_full_range[1].isoformat())
    draws_in_range = results.get_lottery().get_draws_in_date_range(results_full_range[0],
                                                                   results_full_range[1])
    for lottery_draw in draws_in_range:
        lottery_dates.append(lottery_draw.draw_date)
    # Generate date tuples
    end_index = len(lottery_dates) - long_range_offset
    for i in range(end_index):
        most_recent = lottery_dates[i + long_range_offset]
        short_range = lottery_dates[i + long_range_offset - short_range_offset]
        long_range = lottery_dates[i]
        date_ranges.append((most_recent, short_range, long_range))
    # print("HACK", date_ranges)
    return date_ranges


def evaluate_ticket(method, ticket, lottery_results):
    """ Evaluates one ticket against the next four draws. """
    eval_result = EvaluationResult(method.name, 1, 0)
    return eval_result


def setup_logging(args):
    """ Set up logging. """
    split_filename = os.path.splitext(args.filename)
    log_filename = split_filename[0] + '-eval.log'
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)
    logging.info('Started')
    logging.info(args)


def log_results_info(results):
    """ Logs information about the results. """
    logging.info("Lottery name: %s", results.get_lottery().get_name())
    date_range = results.get_lottery().get_date_range()
    logging.info("Results in file from " + date_range[0].isoformat() + " to " +
                 date_range[1].isoformat())


def generate_and_evaluate(lottery_results):
    """ Execute the different evaluation methods.
    for each date in date ranges
        generate stats
        for each method in generation methods
            run method
            evaluate results
    """
    evaluation_results = []
    date_ranges = generate_date_ranges(lottery_results)
    for date_range in date_ranges:
        eval_results = []
        stats_methods = \
            lottery_results.get_lottery().get_stats_generation_methods()
        print("gae", stats_methods)
        for stats_method in stats_methods:
            logging.debug("gae: stats %s", stats_method.name)
            stats_method.analyse(lottery_results, date_range)
            num_lines = 4  ## FIXME HACK!!!!
            ticket_methods = \
                lottery_results.get_lottery().get_ticket_generation_methods()
            for ticket_method in ticket_methods:
                logging.debug("gae: ticket %s", ticket_method.name)
                ticket = ticket_method.generate(date_range[0], num_lines,
                                                stats_method)
                results = evaluate_ticket(ticket_method, ticket,
                                          lottery_results)
                eval_results.append(results)
        evaluation_results.append(("range", range, eval_results))
    return evaluation_results


def print_evaluation_results(evaluation_results):
    """ Print out the evaluation results. """
    for eval_results in evaluation_results:
        logging.info("Date range: " + eval_results[0])
        logging.info("loop: " + str(eval_results[1]))
        for method in eval_results[2]:
            logging.info("  Method name: " + method.name)
            logging.info("  Score: " + str(method.score))


def run():
    """ Reads the data from the given file into the results instance """
    args = handle_parameters()
    setup_logging(args)
    results = LotteryResults()
    results.load_file(args.filename)
    log_results_info(results)
    evaluation_results = generate_and_evaluate(results)
    print_evaluation_results(evaluation_results)


if __name__ == "__main__":

    run()
