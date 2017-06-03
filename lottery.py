#!/usr/bin/python3.6

"""
TODO

"""

import collections
import csv
import datetime


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

def convert_str_to_date(date_str):
    """ TODO """
    print("date_str", date_str)
    formatter_string = "%d-%b-%Y"
    date_object = datetime.datetime.strptime(date_str, formatter_string).date()
    return date_object

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

def get_latest_date(filereader):
    """ The latest date is the first element on the second row"""
    header = True
    for row in filereader:
        if header:
            header = False
            continue
        # Second row
        row_date_str = str(row[0])
        # print("row date", row_date_str)
        latest_date = convert_str_to_date(row_date_str)
        break
    return latest_date

def process_data(filereader):
    """ TODO """
    latest_date = get_latest_date(filereader)
    earliest_date = latest_date + datetime.timedelta(days=-30)
    frequency_in_date_range(filereader, earliest_date, latest_date)

def add_euro_millions_row(row):
    """ TODO """
    euro_millions_entry = collections.namedtuple('euro_millions_entry', \
			['draw_date', 'main_1', 'main_2', 'main_3', 'main_4', 'main_5', \
			'lucky_1', 'lucky_2'])
    euro_millions_entry.draw_date = convert_str_to_date(str(row[0]))
    euro_millions_entry.main_1 = int(row[1])
    euro_millions_entry.main_2 = int(row[2])
    euro_millions_entry.main_3 = int(row[3])
    euro_millions_entry.main_4 = int(row[4])
    euro_millions_entry.main_5 = int(row[5])
    euro_millions_entry.lucky_1 = int(row[6])
    euro_millions_entry.lucky_2 = int(row[7])
    return euro_millions_entry

def run(filename):
    """ TODO """
    with open(filename, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        file_data = []
        ignore_header = True
        for row in filereader:
            if ignore_header:
                ignore_header = False
                continue
            file_data.append(add_euro_millions_row(row))
        print(file_data)
        # process_data(filereader)

if __name__ == "__main__":
    # execute only if run as a script
    run('euromillions-draw-history.csv')
