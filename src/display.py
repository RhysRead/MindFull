#!/usr/bin/env python3

"""display.py: The main file containing the GUI code for MindFull."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2019, Rhys Read"


import tkinter as tk
import logging
import keyboard
import threading

from time import time, sleep

BACKGROUND_COLOUR = 'black'


class Display(object):
    def __init__(self):
        self.__root = tk.Tk()

        self.__root.config(background=BACKGROUND_COLOUR)

        self.__root.pack_propagate(0)
        self.__root.resizable(0, 0)
        self.__root.attributes('-fullscreen', True)

        self.__all_times = []

        self.__time_rounding_value = 1

        self.__base_time = 0
        self.__last_time = 0
        self.__displayed_time = 0
        self.__mean_time = 0
        self.__best_time = 0

        self.__best_time_pretext = 'Best: '
        self.__last_time_pretext = 'Previous: '
        self.__mean_time_pretext = 'Mean: '

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

        self.__mean_time_label = tk.Label(self.__root,
                                          text=self.__mean_time_pretext + '0.0',
                                          font='Helvetica 25 bold',
                                          fg='Black')
        self.__mean_time_label.grid(row=2, column=0, sticky=tk.W, padx=100)

        self.__last_time_label = tk.Label(self.__root,
                                          text=self.__last_time_pretext + '0.0',
                                          font='Helvetica 25 bold',
                                          fg='Black')
        self.__last_time_label.grid(row=2, column=1, sticky=tk.W, padx=100)

        self.__best_time_label = tk.Label(self.__root,
                                          text=self.__best_time_pretext + '0.0',
                                          font='Helvetica 25 bold',
                                          fg='Black')
        self.__best_time_label.grid(row=2, column=2, sticky=tk.W, padx=100)

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

        # Starting side processes
        self.__root.after(100, self.__update_timer_recurring)
        threading.Thread(target=self.__keypress_thread).start()

        # Mainloop
        self.__root.mainloop()
        logging.info('Times:\n' + '\n'.join([str(round(i, self.__time_rounding_value)) for i in self.__all_times]))
        self.__active = False

    def __update_timer_recurring(self):
        if not self.__active:
            return
        self.__displayed_time = get_seconds_since_base_time(self.__base_time)

        # Set displayed time for live timer
        self.__timer_label.config(text=round(self.__displayed_time,
                                             self.__time_rounding_value))

        # If the current time exceeds the best time, set the best time
        seconds_since_base_time = get_seconds_since_base_time(self.__base_time)
        if seconds_since_base_time > self.__best_time:
            self.__best_time_label.config(text=self.__best_time_pretext + str(round(seconds_since_base_time,
                                                                                    self.__time_rounding_value)))

        self.__root.after(100, self.__update_timer_recurring)

    def __set_new_base_time(self):
        self.__last_time = get_seconds_since_base_time(self.__base_time)

        self.__all_times.append(self.__last_time)

        # Set best time
        if self.__last_time > self.__best_time:
            self.__best_time = self.__last_time
            self.__best_time_label.config(text=self.__best_time_pretext + str(round(self.__best_time,
                                                                                    self.__time_rounding_value)))
        # Set mean time
        self.__mean_time = sum(self.__all_times) / len(self.__all_times)
        self.__mean_time_label.config(text=self.__mean_time_pretext + str(round(self.__mean_time,
                                                                                self.__time_rounding_value)))
        # Set last time
        self.__last_time_label.config(text=self.__last_time_pretext + str(round(self.__last_time,
                                                                                self.__time_rounding_value)))

        self.__base_time = time()

    def __keypress_thread(self):
        while self.__active:
            if keyboard.is_pressed(' '):
                self.__set_new_base_time()
                # sleeping to avoid one press registering as many
                sleep(0.1)


def get_seconds_since_base_time(base_time: float):
    return time() - base_time
