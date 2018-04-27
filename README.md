# Lottery analysis program

The aim of the project is to predict winning lottery tickets.  This should be
impossible but I have a hunch that there are patterns in the results that can
be used to improve the chances of winning.

DISCLAIMER: I take no responsibility whatsoever for the use of this code.  Use
at your own risk.

## TODO

Create new ticket generation class. DONE.

* Create several different ticket generation methods to evaluate using the scores.

Create more analysis tools to improve ticket generation.

* Use each generator to create more than one line.  Things to try:
  * Look at short term (less than n) results to pick up "hot" numbers.
  * Look at longer term (more than n) results for numbers that haven't  come up in a long time.
  * Look at winning results and look for patterns in previous draws.

Focus efforts on Euromillions main balls as there appears to be only one set
of balls and one machine (less variables to consider).  Then roll out to Lucky
Stars and Lotto.

Looking at this problem from the other direction.

* Generate stats on a block of results.
* Use the results of the next draw to evaluate the stats generation methods.
* Use the results of the evaluation to improve the stats generation methods.

Decide what to do about merging results CSV files for better analysis.

## Bugs

Vary stats and ticket generation to improve evaluation.

* Both stats methods are identical!!!
* Ticket generation is very simple.

Look at the way date ranges are generated.  For the EuroMillions lottery, the
date ranges may need to be generated per ball set, so generating a range of
dates first thing may be wrong.  Certainly, I need to set a start date, so I
can use past data sets to test prediction methods.  How far to go back
depends on each lottery and each set of balls.

## In progress

Thinking!!!!

## Done

20180426 Lotto evaluation and ticket gneration working again.
20180405 next_ticket works for EuroMillions and MerseyWorld.
20180402 Added new EuroMillions ticket generation method, most for main and least for lucky stars and reverse.
20180401 Added importer utility.  Downloads 6 months of results for Lotto and Euromillions.
