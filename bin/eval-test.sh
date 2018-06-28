#!/bin/bash

SCRIPT=$(realpath -s $0)
BIN_DIR=$(dirname $SCRIPT)
TOP_DIR=${BIN_DIR}/..
DRAW_HISTORY_DIR=${TOP_DIR}/draw_history
EUROMILLIONS_DRAWS_DIR=${DRAW_HISTORY_DIR}/euromillions
LOTTO_DRAWS_DIR=${DRAW_HISTORY_DIR}/lotto

exec_func()
{
	command="python3 ${TOP_DIR}/evaluate.py $1"
	echo
	echo "*************************************************************************"
	echo "${command}"
	echo "*************************************************************************"
	${command}
}

# Delete all log files
rm -f *.log

exec_func "${EUROMILLIONS_DRAWS_DIR}/euromillions-20180625.csv"
exec_func "${LOTTO_DRAWS_DIR}/lotto-20180625.csv"

exit 0
