#!/usr/bin/env python3

"""display.py: The main file containing the GUI code for MindFull."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2019, Rhys Read"


import tkinter as tk
import logging

from time import time, sleep


class Display(object):
    def __init__(self):
        self.__root = tk.Tk()

        self.__root.pack_propagate(0)
        self.__root.resizable(0, 0)
        self.__root.attributes('-fullscreen', True)

        self.__base_time = 0
        self.__last_time = 0
        self.__displayed_time = 0

        self.__active = False

        self.__make_gui()

    def __make_gui(self):
        self.__root.title('MindFull V0.1')

        self.__title_label = tk.Label(self.__root,
                                      text='MindFull.',
                                      font='Helvetica 20 bold',
                                      fg='Black')
        self.__title_label.grid(row=0, column=1, sticky=tk.W, padx=100)

        self.__timer_label = tk.Label(self.__root,
                                      text=0.1,
                                      font='Helvetica 25 bold',
                                      fg='Grey')
        self.__timer_label.grid(row=1, column=1, sticky=tk.W, padx=100)

        self.__last_time_label = tk.Label(self.__root,
                                          text=0.0,
                                          font='Helvetica 25 bold',
                                          fg='Black')
        self.__last_time_label.grid(row=2, column=1, sticky=tk.W, padx=100)

        self.__lost_focus_button = tk.Button(self.__root,
                                             text='Lost Focus',
                                             font='Helvetica 17 bold',
                                             command=self.__set_new_base_time,
                                             width='10',
                                             height='5',
                                             fg='Black',
                                             bg='Light Blue')
        self.__lost_focus_button.grid(row=1, column=0, sticky=tk.E, padx=100)

        self.__exit_button = tk.Button(self.__root,
                                       text='EXIT',
                                       font='Helvetica 17 bold',
                                       command=self.__root.quit,
                                       width='10',
                                       height='5',
                                       fg='Black',
                                       bg='Red')
        self.__exit_button.grid(row=1, column=2, sticky=tk.E, padx=100)

    def start(self):
        self.__active = True
        self.__base_time = time()
        self.__root.after(100, self.__update_timer_recurring)
        self.__root.mainloop()

    def __update_timer_recurring(self):
        if not self.__active:
            return
        self.__displayed_time = get_seconds_since_base_time(self.__base_time)
        self.__timer_label.config(text=round(self.__displayed_time, 1))
        self.__root.after(100, self.__update_timer_recurring)

    def __set_new_base_time(self):
        self.__last_time = get_seconds_since_base_time(self.__base_time)
        self.__last_time_label.config(text=round(self.__last_time, 1))
        self.__base_time = time()


def get_seconds_since_base_time(base_time: float):
    return time() - base_time
