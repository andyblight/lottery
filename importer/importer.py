#!/usr/bin/python3.6
"""
This file imports CSV data from the merseyworld web site.  Pages are:
Lotto:
http://lottery.merseyworld.com/cgi-bin/lottery?days=2&Machine=Z&Ballset=0&order=1&show=1&year=-1&display=CSV
Euromillions
http://lottery.merseyworld.com/cgi-bin/lottery?days=20&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV
"""

import argparse
import csv
import logging
from urllib.request import urlopen

LOG_FILE = "importer.log"
MERSEYWORLD_BASE_URL = "http://lottery.merseyworld.com/cgi-bin/lottery?"
LOTTO = "days=2&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV"
LOTTO_URL = MERSEYWORLD_BASE_URL + LOTTO
LOTTO_FILENAME = "lotto.csv"
EUROMILLIONS = "days=20&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV"
EUROMILLIONS_URL = MERSEYWORLD_BASE_URL + EUROMILLIONS
EURO_MILLIONS_FILENAME = "euromillions.csv"


def parse_list(content):
    """ Load CSV data into a list.  """
    csv_list = []
    # Convert into a list of strings
    unicode = content.decode()
    content_list = unicode.split('\n')
    state = 0
    for line in content_list:
        # print("state, line:", state, line)
        if state == 0:
            # Look for first <PRE>
            if line.startswith('<PRE>'):
                state = 1
        elif state == 1:
            # Look for header
            if line.startswith('No., Day,DD,MMM,YYYY,'):
                csv_list.append(line.split(','))
                state = 2
        elif state == 2:
            # Process rows until blank line
            if line:
                csv_list.append(line.split(','))
            else:
                # Processed all rows so quit
                break
        else:
            continue
    return csv_list


def write_csv_file(filename, csv_list):
    """ Write the dict to given CSV file.  """
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in csv_list:
            writer.writerow(line)


def handle_parameters():
    """ Process the command line arguments.  Returns the values of the
    arguments in a argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(
        description='''Scrapes data from the Merseyworld website and outputs
        the data as CSV file.''')
    parser.add_argument('-v', '--verbose', help='''verbose output.''')
    return parser.parse_args()


def setup_logging(args):
    """ Set up logging. """
    logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.DEBUG)
    logging.info('Started')
    logging.info(args)


def fetch_and_process(url, filename):
    """ Writes a CSV file from the page at the given URL. """
    logging.info("Fetching info from: %s", url)
    content = urlopen(url).read()
    logging.info(content)
    csv_list = parse_list(content)
    # print(csv_list)
    logging.info("Writing data to: %s", filename)
    write_csv_file(filename, csv_list)


def run():
    """ Todo """
    args = handle_parameters()
    setup_logging(args)
    fetch_and_process(LOTTO_URL, LOTTO_FILENAME)
    fetch_and_process(EUROMILLIONS_URL, EURO_MILLIONS_FILENAME)


if __name__ == "__main__":
    run()
