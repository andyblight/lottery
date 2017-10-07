# Lottery analysis program
The aim of the project is to predict winning lottery tickets.  This should be
impossible but I have a hunch that there are patterns in the results that can
be used to improve the chances of winning.

DISCLAIMER: I take no responsibility whatsoever for the use of this code.  Use
at your own risk.



## TODO
Add feedback that allows learning of patterns.
 * Score for each line on each ticket.  The higher the better.
 * Compare scores against methods.

Create more analysis tools to improve ticket generation.
 * Things to try:
   * Look at short term (less than n) results to pick up "hot" numbers.
   * Look at longer term (more than n) results for numbers that haven't come
     up in a long time.
   * Look at winning results and look for patterns in previous draws.

Create new ticket generation class.
 * Create several different ticket generation methods to evaluate using the
   scores.
 
Focus efforts on Euromillions main balls as there appears to be only one set
of balls.  Then roll out to Lucky Stars and Lotto.


## Future
Read merseyworld.co.uk website data using mini-app.
Pages are:
http://lottery.merseyworld.com/cgi-bin/lottery?days=2&Machine=Z&Ballset=0&order=1&show=1&year=-1&display=CSV
http://lottery.merseyworld.com/cgi-bin/lottery?days=19&Machine=Z&Ballset=0&order=1&show=1&year=-1&display=CSV


## Bugs
None.

