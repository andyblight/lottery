#!/usr/bin/python3.6
""" Implementation classes for the EuroMillions lottery. """
import calendar
import datetime
import logging

from lottery import Lottery, LotteryTicket, LotteryDraw, LotteryParser, \
    LotteryTicketGenerationMethod, LotteryStatsGenerationMethod
from lottery_utils import SetOfBalls, convert_str_to_date, frequency, \
    most_common_balls, least_common_balls

LOGGER = logging.getLogger('EuroMillions')


class EuroMillionsLine:
    """ Represents a line of lottery numbers. """

    def __init__(self):
        """ Creates two sets of balls with the right number of balls. """
        self.main_balls = []
        for _ in range(0, 5):
            self.main_balls.append(0)
        self.lucky_stars = []
        for _ in range(0, 2):
            self.lucky_stars.append(0)

    def as_string(self):
        """ Converts a line to a string. """
        # print("as_string, main, lucky", self.main_balls, self.lucky_stars)
        main_str = 'Main balls: {0:2d}  {1:2d}  {2:2d}  {3:2d}  {4:2d}  ' \
            .format(
                self.main_balls[0], self.main_balls[1], self.main_balls[2],
                self.main_balls[3], self.main_balls[4])
        lucky_str = 'Lucky stars: {0:2d}  {1:2d} '.format(
            self.lucky_stars[0], self.lucky_stars[1])
        return main_str + lucky_str

    @staticmethod
    def _mark_ball(line_string, main, lucky):
        """ Mark winning balls with *. """
        main_balls_offset = 14
        lucky_stars_offset = main_balls_offset + 33
        if main > -1 and main < 5:
            index = main_balls_offset + (main * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        if lucky > -1 and lucky < 2:
            index = lucky_stars_offset + (lucky * 4)
            line_string = line_string[:index] + '*' + line_string[index + 1:]
        LOGGER.info(line_string)
        return line_string

    def sort(self):
        """ Sorts the line into ascending numerical order. """
        self.main_balls.sort()
        self.lucky_stars.sort()

    @staticmethod
    def _is_winner(main_matched, lucky_matched):
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

    def score(self, draw):
        """ Returns a tuple containing:
        0 - count of main plus lucky star matches
        1 - True if the line is a winner.
        2 - string of the line with the matching balls shown
        """
        main_matched = 0
        lucky_matched = 0
        matching_str = draw.line.as_string()
        for iterator in range(0, len(self.main_balls)):
            if self.main_balls[iterator] == draw.line.main_balls[iterator]:
                main_matched += 1
                matching_str = self._mark_ball(matching_str, iterator, -1)
        for iterator in range(0, len(self.lucky_stars)):
            if self.lucky_stars[iterator] == draw.line.lucky_stars[iterator]:
                lucky_matched += 1
                matching_str = self._mark_ball(matching_str, -1, iterator)
        return (main_matched + lucky_matched,
                self._is_winner(
                    main_matched,
                    lucky_matched,
                ), matching_str)


class EuroMillionsDraw(LotteryDraw):
    """ Groups draw date and lottery line."""

    def __init__(self):
        """ Initialises the class. """
        super(EuroMillionsDraw, self).__init__()
        self.draw_number = 0
        self.line = EuroMillionsLine()
        self.jackpot = 0
        self.jackpot_wins = 0

    def as_string(self):
        """ Return the draw date and line as a string. """
        return self.draw_date.isoformat() + ' ' + self.line.as_string()


class LotteryTicketGenerationMethodEuro1(LotteryTicketGenerationMethod):
    """ Ticket generation method concrete class.
        Use most common stats.
    """

    def __init__(self):
        LotteryTicketGenerationMethod.__init__(self, "Euro1")

    def generate(self, draw_date, num_lines, ball_stats):
        """ Generate a ticket. """
        # FIXME Hardcoded lines
        if num_lines != 2:
            num_lines = 2
        ticket = LotteryTicket(draw_date)
        # Debug
        LOGGER.info("TGME1: %d", num_lines)
        most_probable = ball_stats.get_most_probable()
        LOGGER.info(most_probable[0])
        LOGGER.info(most_probable[1])
        if most_probable[0] and most_probable[1]:
            for num_lines_it in range(0, num_lines):
                line = EuroMillionsLine()
                num_main_balls = len(line.main_balls)
                num_lucky_stars = len(line.lucky_stars)
                for iterator in range(0, num_main_balls):
                    line.main_balls[iterator] = most_probable[0][iterator][0]
                for iterator in range(0, num_lucky_stars):
                    line.lucky_stars[iterator] = most_probable[1][iterator][0]
                # Use alternate numbers for second line
                if num_lines_it == 1:
                    line.main_balls[4] = most_probable[0][num_main_balls][0]
                    line.lucky_stars[1] = most_probable[1][num_lucky_stars][0]
                line.sort()
                ticket.lines.append(line)
        else:
            LOGGER.error("TGME1: most probable is empty")
        LOGGER.info("TGME1: ticket printout")
        ticket.print(False)
        return ticket


class LotteryTicketGenerationMethodEuro2(LotteryTicketGenerationMethod):
    """ Ticket generation method concrete class.
        Use least common balls.
     """

    def __init__(self):
        LotteryTicketGenerationMethod.__init__(self, "Euro2")

    def generate(self, draw_date, num_lines, ball_stats):
        """ """
        # HACK
        if num_lines != 2:
            num_lines = 2
        ticket = LotteryTicket(draw_date)
        # Debug
        LOGGER.info("TGME2: %d", num_lines)
        least_probable = ball_stats.get_least_probable()
        LOGGER.info(least_probable[0])
        LOGGER.info(least_probable[1])
        if least_probable[0] and least_probable[1]:
            for num_lines_it in range(0, num_lines):
                line = EuroMillionsLine()
                num_main_balls = len(line.main_balls)
                num_lucky_stars = len(line.lucky_stars)
                for iterator in range(0, num_main_balls):
                    line.main_balls[iterator] = least_probable[0][iterator][0]
                for iterator in range(0, num_lucky_stars):
                    line.lucky_stars[iterator] = least_probable[1][iterator][0]
                # Use alternate numbers for second line
                if num_lines_it == 1:
                    line.main_balls[4] = least_probable[0][num_main_balls][0]
                    line.lucky_stars[1] = least_probable[1][num_lucky_stars][0]
                line.sort()
            ticket.lines.append(line)
        else:
            LOGGER.error("TGME2: least probable is empty")
        LOGGER.info("TGME2: ticket printout")
        ticket.print(False)
        return ticket


class LotteryTicketGenerationMethodEuro3(LotteryTicketGenerationMethod):
    """ Ticket generation method concrete class.
        Use mixture of most for main and least for luck stars.
     """

    def __init__(self):
        LotteryTicketGenerationMethod.__init__(self, "Euro3")

    def generate(self, draw_date, num_lines, ball_stats):
        """ """
        ticket = LotteryTicket(draw_date)
        # Debug
        LOGGER.info("TGME3: %d", num_lines)
        # Most probable
        most_probable = ball_stats.get_most_probable()
        LOGGER.info(most_probable[0])
        LOGGER.info(most_probable[1])
        if most_probable[0] and most_probable[1]:
            least_probable = ball_stats.get_least_probable()
            LOGGER.info(least_probable[0])
            LOGGER.info(least_probable[1])
            if least_probable[0] and least_probable[1]:
                # FIXME Hard coded for one line
                line = EuroMillionsLine()
                num_main_balls = len(line.main_balls)
                num_lucky_stars = len(line.lucky_stars)
                # Use most probable for main balls and least probable for
                # lucky stars
                for iterator in range(0, num_main_balls):
                    line.main_balls[iterator] = most_probable[0][iterator][0]
                for iterator in range(0, num_lucky_stars):
                    line.lucky_stars[iterator] = least_probable[1][iterator][0]
                line.sort()
                ticket.lines.append(line)
            else:
                LOGGER.error("TGME3: least probable is empty")
        else:
            LOGGER.error("TGME3: most probable is empty")
        LOGGER.info("TGME3: ticket printout")
        ticket.print(False)
        return ticket


class LotteryTicketGenerationMethodEuro4(LotteryTicketGenerationMethod):
    """ Ticket generation method concrete class.
        Use mixture of most and least.
     """

    def __init__(self):
        LotteryTicketGenerationMethod.__init__(self, "Euro4")

    def generate(self, draw_date, num_lines, ball_stats):
        """ """
        ticket = LotteryTicket(draw_date)
        # Debug
        LOGGER.info("TGME4: %d", num_lines)
        # Most probable
        most_probable = ball_stats.get_most_probable()
        LOGGER.info(most_probable[0])
        LOGGER.info(most_probable[1])
        if most_probable[0] and most_probable[1]:
            least_probable = ball_stats.get_least_probable()
            LOGGER.info(least_probable[0])
            LOGGER.info(least_probable[1])
            if least_probable[0] and least_probable[1]:
                # FIXME Hard coded for one line
                line = EuroMillionsLine()
                num_main_balls = len(line.main_balls)
                num_lucky_stars = len(line.lucky_stars)
                # Use least probable for main balls and most probable for
                # lucky stars
                for iterator in range(0, num_main_balls):
                    line.main_balls[iterator] = least_probable[0][iterator][0]
                for iterator in range(0, num_lucky_stars):
                    line.lucky_stars[iterator] = most_probable[1][iterator][0]
                line.sort()
                ticket.lines.append(line)
            else:
                LOGGER.error("TGME4: least probable is empty")
        else:
            LOGGER.error("TGME4: most probable is empty")
        LOGGER.info("TGME4: ticket printout")
        ticket.print(False)
        return ticket


class LotteryParserEuromillionsNL(LotteryParser):
    """ Parses the CSV data from the National Lottery. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserEuromillionsNL, self).__init__()
        self.name = 'EuroMillions National Lottery'

    def check_header(self, row):
        """ Returns True if the header matches """
        LOGGER.info(self.name + " " + str(row[6]))
        return str(row[6]) == 'Lucky Star 1'

    @staticmethod
    def parse_row(row, draw):
        """ Return a draw object filled with one draw of information. """
        draw.draw_date = convert_str_to_date(str(row[0]))
        line = EuroMillionsLine()
        line.main_balls[0] = int(row[1])
        line.main_balls[1] = int(row[2])
        line.main_balls[2] = int(row[3])
        line.main_balls[3] = int(row[4])
        line.main_balls[4] = int(row[5])
        line.lucky_stars[0] = int(row[6])
        line.lucky_stars[1] = int(row[7])
        LOGGER.debug("LPEMNL:pr: %d", line.main_balls[0])
        draw.line = line
        return draw


class LotteryParserEuromillionsMW(LotteryParser):
    """ Parses the CSV data from
        http://lottery.merseyworld.com/Euro/Winning_index.html.
    """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryParserEuromillionsMW, self).__init__()
        self.name = 'EuroMillions MerseyWorld'

    def check_header(self, row):
        """ Returns True if the header matches """
        LOGGER.info(self.name + " " + str(row[10]))
        return str(row[10]) == 'L1'

    @staticmethod
    def parse_row(row, draw):
        ''' Read row data and copy into EuroMillionsCSV class.
        0  - No.,Day,DD,MMM,YYYY,
        5  - N1,N2,N3,N4,N5,
        10 - L1,L2,Jackpot,Wins
        Day of week is ignored as this can be obtained from the date.
        '''
        day_num = int(row[2])
        month_num = list(calendar.month_abbr).index(row[3])
        year_num = int(row[4])
        draw.draw_date = datetime.date(year_num, month_num, day_num)
        line = EuroMillionsLine()
        line.main_balls[0] = int(row[5])
        line.main_balls[1] = int(row[6])
        line.main_balls[2] = int(row[7])
        line.main_balls[3] = int(row[8])
        line.main_balls[4] = int(row[9])
        line.lucky_stars[0] = int(row[10])
        line.lucky_stars[1] = int(row[11])
        LOGGER.debug("LPEMMW:pr: %d", line.main_balls[0])
        draw.line = line
        draw.jackpot = int(row[12])
        draw.jackpot_wins = int(row[13])
        return draw


class LotteryStatsGenerationMethodEuro1(LotteryStatsGenerationMethod):
    """ Stats generation method. """

    def __init__(self):
        LotteryStatsGenerationMethod.__init__(self, "Euro1")
        self._main_balls_most_probable = []
        self._main_balls_least_probable = []
        self._lucky_stars_most_probable = []
        self._lucky_stars_least_probable = []

    def analyse(self, lottery_results, date_range):
        """ Sets internal stores of information from the given results in the
            given date range.
        """
        # A date range is (most_recent, short_range, long_range)
        date_to = date_range[0]
        date_from = date_range[2]  # FIXME What about short_range???
        lottery = lottery_results.get_lottery()
        balls_in_range = lottery.get_balls_in_date_range(date_from, date_to)
        sets_of_balls = lottery.get_sets_of_balls()
        iterator = 0
        LOGGER.debug("LSGME:a %d", len(balls_in_range))
        LOGGER.debug("LSGME:a1 %s", str(balls_in_range))  # AJB 2 empty arrays!
        for ball_set in sets_of_balls:
            LOGGER.debug("Set of balls: %s", ball_set.get_name())
            num_balls = ball_set.get_num_balls()
            str_log = "LSGME1:a: NUM BALLS " + str(num_balls) + " iterator " \
                + str(iterator)
            LOGGER.info(str_log)
            frequency_of_balls = frequency(num_balls, balls_in_range[iterator])
            LOGGER.debug(frequency_of_balls)
            num_likley = 3
            if num_balls > 20:
                num_likley = 6
            most_likely = most_common_balls(frequency_of_balls, num_likley)
            # print("Most likely", most_likely)
            least_likely = least_common_balls(frequency_of_balls, num_likley)
            # print("Least likely", least_likely)
            if ball_set.get_name() == "main":
                self._main_balls_most_probable = most_likely
                self._main_balls_least_probable = least_likely
            else:
                self._lucky_stars_most_probable = most_likely
                self._lucky_stars_least_probable = least_likely
            iterator += 1

    def get_most_probable(self):
        """ Returns a tuple of (main ball_stats, lucky_star_stats).
            NOTE: Must return list of at least 6 and at least 3 for ticket
            generation methods to work.
        """
        LOGGER.debug("LSGME1:gmp: called")
        return (self._main_balls_most_probable,
                self._lucky_stars_most_probable)

    def get_least_probable(self):
        """ Returns a tuple of (main ball_stats, lucky_star_stats).
            NOTE: Must return list of at least 6 and at least 3 for ticket
            generation methods to work.
        """
        LOGGER.debug("LSGME1:glp: called")
        return (self._main_balls_least_probable,
                self._lucky_stars_least_probable)


class LotteryStatsGenerationMethodEuro2(LotteryStatsGenerationMethod):
    """ TODO """

    def __init__(self):
        LotteryStatsGenerationMethod.__init__(self, "Euro2")
        self._main_balls_most_probable = []
        self._main_balls_least_probable = []
        self._lucky_stars_most_probable = []
        self._lucky_stars_least_probable = []

    def analyse(self, lottery_results, date_range):
        """ """
        # LOGGER.debug("analyse2:", date_range)
        # A date range is (most_recent, short_range, long_range)
        date_to = date_range[0]
        date_from = date_range[2]  # FIXME What about short_range???
        balls = lottery_results.get_lottery().get_balls_in_date_range(
            date_from, date_to)
        sets_of_balls = lottery_results.get_lottery().get_sets_of_balls()
        iterator = 0
        LOGGER.info(balls)
        for ball_set in sets_of_balls:
            # LOGGER.debug("Set of balls:", ball_set.get_name())
            num_balls = ball_set.get_num_balls()
            str_log = "LSGME2:a:NUM BALLS " + str(num_balls) + " iterator " + \
                str(iterator)
            LOGGER.info(str_log)
            frequency_of_balls = frequency(num_balls, balls[iterator])
            LOGGER.debug(frequency_of_balls)
            num_likley = 3
            if num_balls > 20:
                num_likley = 6
            most_likely = most_common_balls(frequency_of_balls, num_likley)
            least_likely = least_common_balls(frequency_of_balls, num_likley)
            if ball_set.get_name() == "main":
                self._main_balls_most_probable = most_likely
                self._main_balls_least_probable = least_likely
            else:
                self._lucky_stars_most_probable = most_likely
                self._lucky_stars_least_probable = least_likely
            iterator += 1

    def get_most_probable(self):
        """ Returns a tuple of (main ball_stats, lucky_star_stats).
            NOTE: Must return list of at least 6 and at least 3 for ticket
            generation methods to work.
        """
        LOGGER.debug("LSGME2:gmp: called")
        return (self._main_balls_most_probable,
                self._lucky_stars_most_probable)

    def get_least_probable(self):
        """ Returns a tuple of (main ball_stats, lucky_star_stats).
            NOTE: Must return list of at least 6 and at least 3 for ticket
            generation methods to work.
        """
        LOGGER.debug("LSGME2:gmp: called")
        return (self._main_balls_least_probable,
                self._lucky_stars_least_probable)


class LotteryEuroMillions(Lottery):
    """ The Euro Millions lottery. """

    def __init__(self):
        """ Initialises the class. """
        super(LotteryEuroMillions, self).__init__()
        self._name = "EuroMillions"
        self._sets_of_balls = 2
        self._main_balls = SetOfBalls("main", 50)
        self._lucky_stars = SetOfBalls("lucky stars", 12)
        # Parsers
        self._available_parsers.append(LotteryParserEuromillionsNL())
        self._available_parsers.append(LotteryParserEuromillionsMW())
        # Ticket generation methods
        self._ticket_generation_methods.append(
            LotteryTicketGenerationMethodEuro1())
        self._ticket_generation_methods.append(
            LotteryTicketGenerationMethodEuro2())
        self._ticket_generation_methods.append(
            LotteryTicketGenerationMethodEuro3())
        self._ticket_generation_methods.append(
            LotteryTicketGenerationMethodEuro4())
        # Stats
        self._stats_generation_methods.append(
            LotteryStatsGenerationMethodEuro1())
        self._stats_generation_methods.append(
            LotteryStatsGenerationMethodEuro2())
        # Debug
        LOGGER.info("Initialised parsers:")
        for parser in self._available_parsers:
            LOGGER.info(parser.name)

    def get_new_draw(self):
        """ Return a new draw. """
        return EuroMillionsDraw()

    def get_sets_of_balls(self):
        """ Returns all sets of balls for this lottery. """
        LOGGER.debug("LEM:gsob")
        return [self._main_balls, self._lucky_stars]

    def get_balls_in_date_range(self, oldest_date, newest_date):
        """ Return a tuple containing the sets of balls in the given date
            range.  The result is used for frequency counting so only the
            number of each ball is returned.
        """
        LOGGER.debug("LEM:gbidr, len %d, from %s to %s", len(self.draws),
                     str(oldest_date), str(newest_date))
        main_balls = []
        lucky_stars = []
        for lottery_draw in self.draws:
            if lottery_draw.draw_date >= oldest_date \
                    and lottery_draw.draw_date <= newest_date:
                LOGGER.debug("LEM:gbidr, draw: %d",
                             lottery_draw.line.main_balls[0])
                # Append all main balls to the given list
                main_balls.append(lottery_draw.line.main_balls[0])
                main_balls.append(lottery_draw.line.main_balls[1])
                main_balls.append(lottery_draw.line.main_balls[2])
                main_balls.append(lottery_draw.line.main_balls[3])
                main_balls.append(lottery_draw.line.main_balls[4])
                # Append all lucky star balls to the given list
                lucky_stars.append(lottery_draw.line.lucky_stars[0])
                lucky_stars.append(lottery_draw.line.lucky_stars[1])
        return (main_balls, lucky_stars)
