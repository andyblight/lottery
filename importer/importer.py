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
from bs4 import BeautifulSoup

LOG_FILE = "importer.log"
MERSEYWORLD_BASE_URL = "http://lottery.merseyworld.com/cgi-bin/lottery?"
LOTTO = "days=2&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV"
LOTTO_URL = MERSEYWORLD_BASE_URL + LOTTO
EUROMILLIONS = "days=20&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV"
EUROMILLIONS_URL = MERSEYWORLD_BASE_URL + EUROMILLIONS



def write_csv_file(filename, soup_data):
    """ Write soup data to CSV file.  """
    with open(filename, newline='') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=',')
        first_line = True
        for line in soup_data:
            # TODO add parsing
            if first_line:
                file_writer.write_header(line)
                first_line = False
            else:
                file_writer.write_row(line)


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


def fetch_and_process(url):
    """ Todo """
    logging.info("Fetching info from: %s", url)
    content = urlopen(url).read()
    soup_data = BeautifulSoup(content, "lxml")
    logging.info(soup_data.prettify())
    # FiXME hardcoded file name
    write_csv_file("filename.csv", soup_data)

def run():
    """ Todo """
    args = handle_parameters()
    setup_logging(args)
    fetch_and_process(LOTTO_URL)
    fetch_and_process(EUROMILLIONS_URL)


if __name__ == "__main__":
    run()
