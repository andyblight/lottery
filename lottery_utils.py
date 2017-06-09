"""
Utility functions for dealing with Lottery csv files.
"""

import datetime


def convert_str_to_date(date_str):
    """ Converts a string to a date type """
    # print("date_str", date_str)
    formatter_string = "%d-%b-%Y"
    date_object = datetime.datetime.strptime(date_str, formatter_string).date()
    return date_object

def frequency(max_num, ball_list):
    """ TODO """
    # print(ball_list)
    frequency_of_balls = []
    for ball_number in range(1, max_num + 1):
        ball_count = 0
        for ball in ball_list:
            # print(ball_number, ball_count, ball)
            if ball_number == ball:
                ball_count += 1
        frequency_of_balls.append((ball_number, ball_count))
    return frequency_of_balls
