# Lottery analysis program

The aim of the project is to predict winning lottery tickets.  This should be
impossible but I have a hunch that there are patterns in the results that can
be used to improve the chances of winning.

The ultimate goal is to predict big winners, getting wins of 4 balls or more.

DISCLAIMER: I take no responsibility whatsoever for the use of this code.  Use
at your own risk.

## TODO

Lotto is more complicated to predict as there are a number of ball sets in use.
EuroMillions is two sets of balls and machines.  Predict each set independently
to line generation need to be significantly different from Lotto.
Maybe one of the smaller lotteries might be more use, Thunderball?

Is date range in the output useful?  Are the dates of the draws useful?

Create several different ticket generation methods to evaluate using the scores.
Each line generator creates one line that is add to a ticket.  Things to try:

* Look at short term (less than n) results to pick up "hot" numbers.
* Look at longer term (more than n) results for numbers that haven't  come up in a long time.
* Look at winning results and look for patterns in previous draws.

Create more analysis tools to improve ticket generation.

Focus efforts on Euromillions main balls as there appears to be only one set
of balls and one machine (less variables to consider).  Then roll out to Lucky
Stars and Lotto.

Looking at this problem from the other direction.

* Generate stats on a block of results.
* Use the results of the next draw to evaluate the stats generation methods.
* Use the results of the evaluation to improve the stats generation methods.

Decide what to do about merging results CSV files for better analysis.

Is there some way to predict the big winners?
What has to be done to predict the big winners?
Is there a pattern to the winning balls?
Should I concentrate my efforts on the Thunderball as it is cheaper?

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

Move line generation classes into a separate file for each lottery.

## Decisions

### Leave old methods in the code

This is the better approach for now as it is easier to compare old and new methods.
It also means that old methods keep the same names so it makes comparison easier.
This means that the LineGeneration classes need to be moved into their own files
to avoid the enevitable clutter many classes will cause.

Pythin project structure:  http://docs.python-guide.org/en/latest/writing/structure/

## Status

20180608  Best: Euro1Euro2, Lotto1Lotto1.  Worst: Euro1Euro3,  Lotto1Lotto2

## Done

20180628 Improved directory structure in preparation for moving LineGeneration classes
into their own directories.
20180607 Noticed that removing the alternate path in ticket generation reduced number
of winners.  This was shown to be due to halving the number of lines being tested.
20180606 Removed num_lines from ticket generation methods.
Change names of ticket generation to line generation.
20180510 Run eval-test.sh.  Lotto ticket generation method 2 generates 0 winners.
Looks like a bug.
Analysis of the log file shows that ticket method 2 only generates 1 ball
matches.  This is useful data as it shows how not to win.
20180426 Lotto evaluation and ticket generation working again.
20180405 next_ticket works for EuroMillions and MerseyWorld.
20180402 Added new EuroMillions ticket generation method, most for main and least for lucky stars and reverse.
20180401 Added importer utility.  Downloads 6 months of results for Lotto and Euromillions.
