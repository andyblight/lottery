#!/usr/bin/python3.6

"""
TODO

"""

import csv
import datetime

from lottery_results import LotteryResults
from lottery_utils import convert_str_to_date


def frequency(max_num, ball_list):
    """ TODO """
    # print(ball_list)
    frequency_of_balls = []
    for ball_number in range(1, max_num + 1):
        ball_count = 0
        for ball in ball_list:
            # print(ball_number, ball_count, ball)
            if ball_number == int(ball):
                ball_count += 1
        frequency_of_balls.append((ball_number, ball_count))
    print(frequency_of_balls)

def copy_row_data_to_lists(row, main_balls, lucky_stars):
    """ TODO """
    print(row)
    main_balls.append(row[1])
    main_balls.append(row[2])
    main_balls.append(row[3])
    main_balls.append(row[4])
    main_balls.append(row[5])
    lucky_stars.append(row[6])
    lucky_stars.append(row[7])

def frequency_in_date_range(filereader, date_from, date_to):
    """ TODO """
    print("From", date_from, "to", date_to)
    main_balls = []
    first_row = True
    lucky_stars = []
    for row in filereader:
        if first_row:
            first_row = False
            continue
        row_date_str = str(row[0])
        # print("row date", row_date_str)
        row_date = convert_str_to_date(row_date_str)
        # print("Converted: row date", row_date)
        if row_date >= date_from and row_date <= date_to:
            copy_row_data_to_lists(row, main_balls, lucky_stars)
    frequency(50, main_balls)
    frequency(12, lucky_stars)

def process_data(results):
    """ TODO """
    latest_date = results.get_latest_date()
    earliest_date = latest_date + datetime.timedelta(days=-30)
    frequency_in_date_range(file_data, earliest_date, latest_date)

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
