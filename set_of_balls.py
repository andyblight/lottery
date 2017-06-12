#!/usr/bin/python3.6

class SetOfBalls:
    """ Information about the set of balls. """
    _num_balls = 0
    _name = ""

    def __init__(self, name, num_balls):
        """ Initialises the class. """
        self._num_balls = num_balls
        self._name = name

    def get_num_balls(self):
        """ Return the number of balls in the set. """
        return self._num_balls

    def get_name(self):
        """ Return the number of balls in the set. """
        return self._name

