#!/bin/bash

echo "*************************************************************************"
echo  "Help"
echo "*************************************************************************"
./go.py -h
echo 
echo "*************************************************************************"
echo "Help"
echo "*************************************************************************"
./go.py --help
echo 
echo "*************************************************************************"
echo "Lotto"
echo "*************************************************************************"
echo 
./go.py lotto-draw-history.csv
echo 
echo "*************************************************************************"
echo "Euromillions"
echo "*************************************************************************"
echo 
./go.py euromillions-draw-history.csv
