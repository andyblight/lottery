#!/bin/bash


exec_func()
{
	echo
	echo "*************************************************************************"
	echo $1
	echo "*************************************************************************"
	$1
}

# Delete all log files
rm *.log

cd importer
./importer.py
cd ..
./next_ticket.py lotto.csv
./next_ticket.py euromillions-2017.csv
