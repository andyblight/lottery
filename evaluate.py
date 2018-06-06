#!/usr/bin/python3.6
"""
This file generates statistics about range of results and evaluates the
effectiveness of the generation methods by comparing against future results.

"""

import argparse
import datetime
import logging
import os

from lottery_results import LotteryResults

NUMBER_OF_WEEKS = 4


class EvaluationResult:
    """ Info about how each method performed. """

    def __init__(self, stats_method="", ticket_method="", draw=(), score=()):
        self.stats_method = stats_method
        self.ticket_method = ticket_method
        self.draw = draw
        self.score = score


def handle_parameters():
    """ Process the command line arguments.  Returns the values of the
    arguments in a argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(
        description=''' Generates statistics and suggests tickets to buy based
                        on the given CSV files.''')
    parser.add_argument('-v', '--verbose', help='''verbose output.''')
    parser.add_argument("filename", help='CSV file or files to process')
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
    draws_in_range = results.get_lottery().get_draws_in_date_range(
        results_full_range[0], results_full_range[1])
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


def evaluate_line(start_date, num_weeks, stats_name, line_name, line,
                  lottery_results):
    """ Evaluates one ticket line against the next four draws. """
    line_results = []
    end_date = start_date + datetime.timedelta(weeks=num_weeks)
    four_weeks_results = lottery_results.get_lottery().get_draws_in_date_range(
        start_date, end_date)
    logging.debug("el: printing draws")
    for draw in four_weeks_results:
        logging.debug(draw.draw_date)
        score = line.score(draw)
        logging.debug("el: winner %s", score[2])
        eval_result = EvaluationResult(stats_name, line_name, draw, score)
        line_results.append(eval_result)
    return line_results


def setup_logging(args):
    """ Set up logging. """
    split_filename = os.path.splitext(args.filename)
    log_filename = split_filename[0] + '-eval.log'
    logging.basicConfig(
        filename=log_filename, filemode='w', level=logging.DEBUG)
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
        stats_methods = lottery_results.get_lottery(
        ).get_stats_generation_methods()
        # print("gae", stats_methods)
        for stats_method in stats_methods:
            logging.debug("gae: stats %s", stats_method.name)
            stats_method.analyse(lottery_results, date_range)
            line_methods = lottery_results.get_lottery(
            ).get_line_generation_methods()
            for line_method in line_methods:
                logging.debug("gae: ticket %s", line_method.name)
                line = line_method.generate(stats_method)
                line_result = evaluate_line(date_range[0], NUMBER_OF_WEEKS,
                                        stats_method.name, line_method.name,
                                        line, lottery_results)
                eval_results.append(line_result)
        evaluation_results.append((range, eval_results))
    return evaluation_results


def collate_evaluation_results(evaluation_results):
    """ Collate the evaluation results into results for each combination of
        stats and ticket methods.
    """
    # Each entry: key = stats method + ticket method, value =
    # (number of wins, biggest win, [2 ball wins, 3 ball wins, 4 ball wins,...])
    method_combination_scores = {}
    # evaluation_results is a
    # list of eval_results which is a
    # list of line_results which is a
    # list of EvaluationResult
    for eval_results in evaluation_results:
        ## FIXME AAAAAAA
        # The date range is  NOT PRESSENT
        # print("cer: Date range: ",  eval_results)
        # logging.info("cer: Date range: from %s to %s", eval_results[0][0],
        #               eval_results[0][1])
        for line_result in eval_results[1]:
            for result in line_result:
                key = result.stats_method
                key += result.ticket_method
                # eval_result.draw
                # print(key, eval_result.score)
                logging.info("cer: key: %s, score: %s", str(key),
                             str(result.score))
                # Add new entry if key not found.
                if not method_combination_scores.get(key):
                    method_combination_scores[key] = [0, 0, []]
                # Count of winners
                if result.score[1]:
                    method_combination_scores[key][0] += 1
                    # print("Inc winner count")
                    # Biggest winner (number of matched balls)
                    if result.score[0] > method_combination_scores[key][1]:
                        method_combination_scores[key][1] = result.score[0]
                        # print("Inc biggest winner")
                    # Add to list of number of winning balls.
                    method_combination_scores[key][2].append(result.score[0])
    return method_combination_scores


def print_collated_results(collated_results):
    """ Print the collated results. """
    print("")
    print("Collated results")
    # What date range do I need to show?  What is useful to help understand 
    print("stats method + ticket method, total number of wins, num of balls "
          "of biggest win, [num winning balls, ...])")
    # AJB dict iterator
    for key, score in collated_results.items():
        print(key, score)


def run():
    """ Reads the data from the given file into the results instance """
    args = handle_parameters()
    setup_logging(args)
    results = LotteryResults()
    results.load_file(args.filename)
    log_results_info(results)
    evaluation_results = generate_and_evaluate(results)
    collated_results = collate_evaluation_results(evaluation_results)
    print_collated_results(collated_results)


if __name__ == "__main__":

    run()
