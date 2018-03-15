#!/usr/bin/python3.6

"""
This file imports CSV data from the merseyworld web site.  Pages are:
Lotto:
http://lottery.merseyworld.com/cgi-bin/lottery?days=2&Machine=Z&Ballset=0&order=1&show=1&year=-1&display=CSV
Euromillions
http://lottery.merseyworld.com/cgi-bin/lottery?days=20&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV
"""

import argparse
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup

LOG_FILE = "importer.log"
URL = "http://lottery.merseyworld.com/cgi-bin/lottery?days=20&Machine=Z&Ballset=0&order=0&show=1&year=-1&display=CSV"

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


def run():
    """ Todo """
    args = handle_parameters()
    setup_logging(args)
    content = urlopen(URL).read()
    soup = BeautifulSoup(content, "lxml")
    print(soup.prettify())

if __name__ == "__main__":
    run()
