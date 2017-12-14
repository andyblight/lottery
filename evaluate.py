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
from lottery_utils import frequency, most_common_balls, least_common_balls


class EvaluationResult:
    """ Info about how each method performed. """

    def __init__(self):
        self.name = ""
        self.score = 0
        self.loop = 0

    def __init__(self, name, score, loop):
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


def ball_stats_in_date_range(results, date_from, date_to):
    """ Returns the statistics about the balls for all ball sets for the given
        range.
    """
    logging.debug("Ball frequency from", date_from, "to", date_to)
    balls = results.get_lottery().get_balls_in_date_range(date_from, date_to)
    sets_of_balls = results.get_lottery().get_sets_of_balls()
    iterator = 0
    ball_stats = []
    logging.info(balls)
    for ball_set in sets_of_balls:
        logging.debug("Set of balls:", ball_set.get_name())
        num_balls = ball_set.get_num_balls()
        str_log = "NUM BALLS " + str(num_balls) + " iterator " + str(iterator)
        logging.info(str_log)
        frequency_of_balls = frequency(num_balls, balls[iterator])
        logging.debug(frequency_of_balls)
        num_likley = 3
        if num_balls > 20:
            num_likley = 6
        most_likely = most_common_balls(frequency_of_balls, num_likley)
        logging.debug("Most likely", most_likely)
        least_likely = least_common_balls(frequency_of_balls, num_likley)
        logging.debug("Least likely", least_likely)
        iterator += 1
        ball_stats.append(frequency_of_balls)
        ball_stats.append(most_likely)
        ball_stats.append(least_likely)
    return ball_stats


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
    # test_start = [100, 90, 80, 70, 60, 40]
    # test_delta = [60, 70, 80, 90, 100, 120]
    # Start range
    # for iterator in range(0, len(test_start)):
    #    logging.info()  # Blank line to separate output
    #    logging.info("Start", test_start[iterator], "delta",
    #                 test_delta[iterator])
    #    analysis_start = date_range[0] + \
    #        datetime.timedelta(test_start[iterator])
    #    analysis_end = analysis_start + \
    #        datetime.timedelta(test_delta[iterator])
    #    process_data_in_range(results, analysis_start, analysis_end)
    logging.debug("Not appeared in delta")
    test_delta = [20, 25, 30, 35, 40, 45, 50, 55, 60]
    end_date = date_range[0] + datetime.timedelta(120)
    analysis_start = results.get_lottery().get_first_lottery_date()
    while analysis_start < end_date:
        for delta in range(0, len(test_delta)):
            logging.info('.')
            logging.info("Start " + analysis_start.isoformat() + ", delta " +
                         str(test_delta[delta]))
            analysis_end = analysis_start + \
                datetime.timedelta(test_delta[delta])
            process_data_in_range(results, analysis_start, analysis_end,
                                  winning_draws, False)
        analysis_start = results.get_lottery().get_next_lottery_date()
    print_summary(winning_draws)
    # Print next ticket
    analysis_end = date_range[1]
    analysis_start = analysis_end - datetime.timedelta(35)
    process_data_in_range(results, analysis_start, analysis_end, winning_draws,
                          True)

## OLD CODE ABOVE ############################################################


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
    excluded_draws = 4
    # FIXME Each lottery may need different settings.
    short_range_offset = 4  # 2 draws per week * 2 weeks
    long_range_offset = 40  # 2 draws per week * 20 weeks
    # Generate list of lottery dates
    lottery_dates = []
    results_range = results.get_lottery().get_date_range()
    date_iterator = results.get_lottery().get_next_lottery_date()
    logging.info('Generating dates from ' + date_iterator.isoformat() +
                 ' to ' + results_range[1].isoformat())
    while date_iterator < results_range[1]:
        lottery_dates.append(date_iterator)
        date_iterator = results.get_lottery().get_next_lottery_date()
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
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    logging.info('Started')
    logging.info(args)


def log_results_info(results):
    """ Logs information about the results. """
    logging.info("Lottery name:" + results.get_lottery().get_name())
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
        # TODO Implement get_stats_generation_methods() and stats class
        stats_methods = lottery_results.get_lottery().get_stats_generation_methods()
        for stats_method in stats_methods:
            stats_method.analyse(lottery_results, date_range)
            num_lines = 4  ## HACK!!!!
            ticket_methods = lottery_results.get_lottery().get_ticket_generation_methods()
            for ticket_method in ticket_methods:
                ticket = ticket_method.generate(date_range[0], num_lines, stats_method)
                results = evaluate_ticket(method, ticket, lottery_results)
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
