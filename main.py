#!/usr/bin/python

import curses
import time
import datetime

# Print some text
def text(text, y, stdscr):
    # Find the middle of the screen
    mx = stdscr.getmaxyx()[1]//2
    my = stdscr.getmaxyx()[0]//2

    # Subtract len(text)//2 to adjust for the length of the text
    stdscr.addstr(my + y, mx - len(text)//2, text)
    stdscr.refresh()

# The main selection menu
def main_menu(stdscr, sel_row):
    options = [{
                "text": "Welcome to MathTreadmill",
                "y": -5
            },
            {
                "text": "Auto Mode",
                "y": 1
            },
            {
                "text": "Custom Mode",
                "y": 2
            }]

    for index, option in enumerate(options):
        if sel_row == index:
            # This reverses the background colour for the selected option
            stdscr.attron(curses.color_pair(1))
            text(option["text"], option["y"], stdscr)
            stdscr.attroff(curses.color_pair(1))

        else:
            text(option["text"], option["y"], stdscr)


def main(stdscr):
    # Set up colours
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.nodelay(True)

    # Starting screen
    state = "main_menu"
    sel_row = 1
    main_menu(stdscr, sel_row)

    # Main loop
    while 1:
        # Get the pressed key
        key = stdscr.getch()

        # Quit with "q"
        if key == 113:
            break

        # Main menu
        elif state == "main_menu":
            # Pressing 'up' or 'k' selects the "Auto Mode" option
            if key in [curses.KEY_UP, 107]:
                sel_row = 1
                main_menu(stdscr, sel_row)

            # Pressing 'down' or 'j' selects the "Custom Mode" option
            elif key in [curses.KEY_DOWN, 106]:
                sel_row = 2
                main_menu(stdscr, sel_row)

            # Pressing enter goes into the option
            elif key in [curses.KEY_ENTER, 10, 13]:
                stdscr.clear()

                if sel_row == 1:
                    state = "auto"

                    question = "16 - 14"
                    current_value = ""

                    sec_total = 60
                    sec_rem = 60

                    question_start = datetime.datetime.now()

                    bars = round(sec_total / sec_rem * 20)

                else:
                    state = "custom"
                    text("What would you like..?", 0, stdscr)

        # Auto Mode
        elif state == "auto":
            sec_rem = sec_total - (datetime.datetime.now() - question_start).seconds
            bars = round(sec_rem / sec_total * 20)

            if sec_rem < 10:
                sec_rem = " {}".format(sec_rem)

            text("{} = ?".format(question), -1, stdscr)
            text("> {}_".format(current_value), 0, stdscr)

            text("|{bar}{space}|".format(bar="█"*bars, space=" "*(20-bars)), 3, stdscr)
            text("{sec}s left".format(sec=sec_rem), 4, stdscr)

curses.wrapper(main)
