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

exec_func "./go.py -h"
exec_func "./go.py --help"
exec_func "./go.py lotto-draw-history.csv"
exec_func "./go.py euromillions-draw-history.csv"
exec_func "./go.py lotto-2017.csv"
exec_func "./go.py euromillions-2017.csv"
exec_func "./next_ticket.py lotto-draw-history.csv"
exec_func "./next_ticket.py euromillions-draw-history.csv"
exec_func "./next_ticket.py lotto-2017.csv"
exec_func "./next_ticket.py euromillions-2017.csv"
