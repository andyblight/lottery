#!/bin/bash

SCRIPT=$(realpath -s $0)
BIN_DIR=$(dirname $SCRIPT)
TOP_DIR=${BIN_DIR}/..

exec_func()
{
	command="python3 $1"
	echo
	echo "*************************************************************************"
	echo "${command}"
	echo "*************************************************************************"
	${command}
}

# Delete all log files
rm -f *.log

echo "Starting import..."
${TOP_DIR}/importer/importer.py
echo "Analysing..."
${TOP_DIR}/next_ticket.py lotto.csv
${TOP_DIR}/next_ticket.py euromillions.csv
echo "Done!"
