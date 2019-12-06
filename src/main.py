#!/usr/bin/env python3

"""main.py: The main file used to execute MindFull."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2019, Rhys Read"


import logging

from display import Display

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__display = Display()

    def start(self):
        self.__display.start()


if __name__ == '__main__':
    main = Main()
    main.start()
