#!/usr/bin/python3.6

"""
TODO

"""

import csv
import datetime

from lottery_results import LotteryResults


def process_data(results):
    """ TODO """
    latest_date = results.get_latest_date()
    earliest_date = latest_date + datetime.timedelta(days=-30)
    results.frequency_in_date_range(earliest_date, latest_date)

def run(filename):
    """ Reads the data from the given file into the results instance """
    results = LotteryResults()
    with open(filename, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        ignore_header = True
        for row in filereader:
            if ignore_header:
                results.parse_header(row)
                ignore_header = False
                continue
            results.parse_row(row)
    process_data(results)

if __name__ == "__main__":
    # execute only if run as a script
    run('euromillions-draw-history.csv')
