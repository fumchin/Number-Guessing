#!/usr/bin/python3
import tkinter as tk
import threading

class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event
        self.time_string = tk.StringVar()
        self.duration_sec = 0
        self.duration_min = 0
        self.duration_sec_string = "00"
        self.duration_min_string = "00"
        self.run_or_not = True

    def run(self):
        while not self.stopped.wait(1):
            self.time_string.set("time: " + self.duration_min_string + ":" + self.duration_sec_string)
            if self.run_or_not:
                self.duration_sec += 1
                if self.duration_sec >= 60:
                    self.duration_sec -= 60
                    self.duration_min += 1
                self.output_string_format()

    def output_string_format(self):
        if self.duration_min >= 10:
            self.duration_min_string = str(self.duration_min)
        else:
            self.duration_min_string = "0" + str(self.duration_min)

        if self.duration_sec >= 10:
            self.duration_sec_string = str(self.duration_sec)
        else:
            self.duration_sec_string = "0" + str(self.duration_sec)

    def set_time_string(self, time_string):
        self.time_string = time_string

    def reset_time(self):
        self.duration_sec = 0
        self.duration_min = 0

    def pause(self):
        self.run_or_not = False

    def restart(self):
        self.run_or_not = True
        self.duration_sec = 0
        self.duration_min = 0

    # return string
    def get_time(self):
        return self.duration_min_string + ":" + self.duration_sec_string