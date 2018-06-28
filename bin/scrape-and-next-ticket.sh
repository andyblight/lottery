#!/bin/bash

SCRIPT=$(realpath -s $0)
BIN_DIR=$(dirname $SCRIPT)
TOP_DIR=${BIN_DIR}/..

exec_func()
{
	echo
	echo "*************************************************************************"
	echo $1
	echo "*************************************************************************"
	$1
}

# Delete all log files
rm -f *.log

echo "Starting import..."
${TOP_DIR}/importer/importer.py
echo "Analysing..."
${TOP_DIR}/next_ticket.py lotto.csv
${TOP_DIR}/next_ticket.py euromillions.csv
echo "Done!"
