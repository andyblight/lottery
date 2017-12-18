#!/bin/bash


exec_func() 
{
	echo
	echo "*************************************************************************"
	echo "./evaluate.py $1"
	echo "*************************************************************************"
	./evaluate.py $1
}

# Delete all log files
rm *.log

exec_func "euromillions-2017.csv"
exit 1
