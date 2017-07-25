#!/usr/bin/python3.6
""" """

import collections
from lottery import Lottery, LotteryTicket
from lottery_utils import SetOfBalls, convert_str_to_date, frequency

# TODO Add sort to this class
# TODO Add function to compare results with ticket and produce scores.


class EuroMillionsLine:
    """ Represents a line of lottery numbers. """

    def __init__(self):
        """ Creates two sets of balls with the right number of balls. """
        self.main_balls = []
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.main_balls.append(0)
        self.lucky_stars = []
        self.lucky_stars.append(0)
        self.lucky_stars.append(0)

    def as_string(self):
        """ """
        return 'Main {0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  Lucky stars {5:2d}  {6:2d} '.format(
            self.main_balls[0], self.main_balls[1], self.main_balls[2], self.main_balls[3], self.main_balls[4],
            self.lucky_stars[0], self.lucky_stars[1])

    def _mark_ball_in_string(self, line_string, main, lucky):
        """ """
        if main > -1 and main < 5:
            index = 7 + (main * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        if lucky > -1 and lucky < 2:
            index = 39 + (lucky * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        # print(line_string)
        return line_string

    def sort(self):
        """ Sorts the line into ascending numerical order. """
        self.main_balls.sort()
        self.lucky_stars.sort()

    def _is_winner(self, main_matched, lucky_matched):
        """ The rules for winning are
        Match 5 + 2 Lucky Stars - Jackpot
        Match 5 + 1 Lucky Star
        Match 5
        Match 4 + 2 Lucky Stars
        Match 4 + 1 Lucky Star
        Match 4
        Match 3 + 2 Lucky Stars
        Match 3 + 1 Lucky Star
        Match 3
        Match 2 + 2 Lucky Stars
        Match 2 + 1 Lucky Star
        Match 2
        Match 1 + 2 Lucky Stars
        """
        result = False
        if main_matched == 1 and lucky_matched == 2:
            result = True
        else:
            if main_matched >= 2:
                result = True
        return result

    def score(self, line):
        """ Returns a tuple containing:
        0 - count of main ball matches
        1 - count of lucky star matches
        2 - True if the line is a winner.
        3 - string of the line with the matching balls shown
        """
        main_matched = 0
        lucky_matched = 0
        matching_str = line.as_string()
        for ii in range(0, len(self.main_balls)):
            if self.main_balls[ii] == line.main_balls[ii]:
                main_matched += 1
                matching_str = self._mark_ball_in_string(matching_str, ii, -1)
        for ii in range(0, len(self.lucky_stars)):
            if self.lucky_stars[ii] == line.lucky_stars[ii]:
                lucky_matched += 1
                matching_str = self._mark_ball_in_string(matching_str, -1, ii)
        return (main_matched, lucky_matched,
                self._is_winner(main_matched, lucky_matched,), matching_str)


class EuroMillionsCSVDraw:
    """ Groups draw date and lottery line."""

    def __init__(self):
        self.draw_date = 0
        self.line = EuroMillionsLine()

    def __lt__(self, other):
        """ Returns True when self < other.  Test is on draw date. """
        result = False
        if self.draw_date < other.draw_date:
            result = True
        return result


class LotteryTicketEuroMillions(LotteryTicket):
    """ Class representing a EuroMillionsTicket.
    Only implements lottery specific functions.
    """

    def generate_lines(self, num_lines, ball_stats):
        """ Generates the given number of lines from the ball stats. """
        debug_on = False
        if debug_on:
            print("Gen lines EM", num_lines, "Ignored!")
            # for ii in range(0, num_lines):
            print(ball_stats[0])
            print(ball_stats[1])  # Most
            print(ball_stats[2])  # Least
            print(ball_stats[3])
            print(ball_stats[4])  # Most
            print(ball_stats[5])  # Least
        # Use least common balls
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[2][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[5][ii][0]
        line.sort()
        self.lines.append(line)
        # Use the same line but with the alternatives
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[2][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[5][ii][0]
        line.main_balls[4] = ball_stats[2][5][0]
        line.lucky_stars[1] = ball_stats[5][2][0]
        line.sort()
        self.lines.append(line)
        # Use most common balls
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[1][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[4][ii][0]
        line.sort()
        self.lines.append(line)
        # Use the same line but with the alternatives
        line = EuroMillionsLine()
        for ii in range(0, len(line.main_balls)):
            line.main_balls[ii] = ball_stats[1][ii][0]
        for ii in range(0, len(line.lucky_stars)):
            line.lucky_stars[ii] = ball_stats[4][ii][0]
        line.main_balls[4] = ball_stats[1][5][0]
        line.lucky_stars[1] = ball_stats[4][2][0]
        line.sort()
        self.lines.append(line)

    def print_ticket(self):
        """ Prints the ticket. """
        # print("Ticket date EM:", self._draw_date, "Num Lines", len(self.lines))
        for line in self.lines:
            print(line.as_string())


class LotteryEuroMillions(Lottery):
    """ The Euro Millions lottery. """

    def __init__(self):
        self._name = "EuroMillions"
        self.results = []
        self._num_draws = 0
        self._sets_of_balls = 2
        self._main_balls = SetOfBalls("main", 50)
        self._lucky_star_balls = SetOfBalls("lucky stars", 12)

    def check_header(self, row):
        """ Returns True if the header row is for this lottery """
        return str(row[6]) == 'Lucky Star 1'

    def get_ball_sets(self):
        """ Returns all sets of balls for this lottery. """
        return (self._main_balls, self._lucky_star_balls)

    def parse_row(self, row):
        """ Read row data and copy into EuroMillionsCSV class """
        draw = EuroMillionsCSVDraw()
        draw.draw_date = convert_str_to_date(str(row[0]))
        line = EuroMillionsLine()
        line.main_balls[0] = int(row[1])
        line.main_balls[1] = int(row[2])
        line.main_balls[2] = int(row[3])
        line.main_balls[3] = int(row[4])
        line.main_balls[4] = int(row[5])
        line.lucky_stars[0] = int(row[6])
        line.lucky_stars[1] = int(row[7])
        draw.line = line
        self.results.append(draw)
        self._num_draws += 1

    def get_balls_in_date_range(self, date_from, date_to):
        """ Returns a tuple containing the sets of balls in the give date
        range. """
        main_balls = []
        lucky_stars = []
        for lottery_draw in self.results:
            if lottery_draw.draw_date >= date_from and lottery_draw.draw_date <= date_to:
                """ Appends all main balls to the given list """
                main_balls.append(lottery_draw.line.main_balls[0])
                main_balls.append(lottery_draw.line.main_balls[1])
                main_balls.append(lottery_draw.line.main_balls[2])
                main_balls.append(lottery_draw.line.main_balls[3])
                main_balls.append(lottery_draw.line.main_balls[4])
                """ Appends all lucky star balls to the given list """
                lucky_stars.append(lottery_draw.line.lucky_stars[0])
                lucky_stars.append(lottery_draw.line.lucky_stars[1])
        return (main_balls, lucky_stars)

    def get_draw(self, draw_date, main_1, main_2, main_3,
                 main_4, main_5, lucky_1, lucky_2):
        lottery_draw = EuroMillionsCSVDraw(draw_date, main_1, main_2,
                                           main_3, main_4, main_5,
                                           lucky_1, lucky_2)
        return lottery_draw

    def print_draw(self, lottery_draw):
        """ Print the given draw. """
        line = lottery_draw.line
        print('Date', lottery_draw.draw_date, lottery_draw.line.as_string())

    def generate_ticket(self, next_lottery_date, num_lines, ball_stats):
        """ Generates a new ticket with the given number of lines. """
        ticket = LotteryTicketEuroMillions(next_lottery_date)
        ticket.generate_lines(num_lines, ball_stats)
        # Add lines here
        return ticket

    def test_draw_against_ticket(self, lottery_draw, ticket):
        """ Prints out the number of matches for each line of the given ticket against the given draw. """
        best_score = (0, 0, False, [])
        winning_lines = []

        for line in ticket.lines:
            score = line.score(lottery_draw.line)
            # print(score)
            if score == best_score:
                winning_lines.append(line)
            if score[0] > best_score[0] or score[1] > best_score[1]:
                best_score = score
                winning_lines.clear()
                winning_lines.append(line)
        return (best_score, winning_lines, lottery_draw)
