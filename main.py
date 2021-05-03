#!/usr/bin/python

import curses
import time

def text(text, y, stdscr):
    mx = stdscr.getmaxyx()[1]//2
    my = stdscr.getmaxyx()[0]//2
    stdscr.addstr(my + y, mx - len(text)//2, text)
    stdscr.refresh()

def main(stdscr):

    while 1:
        text("Welcome to MathTreadmill!", -5, stdscr)
        text("14 + 123 = ?", 0, stdscr)
        text("14s remaining", 0, stdscr)
        time.sleep(4)

curses.wrapper(main)
