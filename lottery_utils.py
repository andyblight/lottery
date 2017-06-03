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
