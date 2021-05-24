#!/usr/bin/python

import curses
import time
import datetime
import os
import random
import math

# More lag = less CPU usage
# Less lag = less delay on input
LAG = 10
# LAG = 0 --> CPU% = 100
# LAG = 10 --> CPU% = 2
# LAG = 100 --> CPU% = "0.0" (htop)

def z(number):
    if number < 0:
        return "({})".format(number)
    else:
        return number

def get_question(skill):
    # List of lines in the file that are for this skill
    skill_lines = []

    # Sample question file line: "2.2 M -10 -2 -10 -2"
    with open("auto_questions") as auto_questions:
        lines = auto_questions.readlines()

        # Find the correct lines for the skill
        for line in lines:
            if line[:3] == skill:
                skill_lines.append(line[4:])

    # Pick a random question type (multi-variable for readability)
    question_id = random.randint(0, len(skill_lines) - 1)
    question_line = skill_lines[question_id]
    question_line = question_line.split()

    x = random.randint(int(question_line[1]), int(question_line[2]))
    y = random.randint(int(question_line[3]), int(question_line[4]))

    # Addition
    if question_line[0] == "A":
        if random.randint(1, 2) == 1:
            question = "{} + {}".format(z(x), z(y))
        else:
            question = "{} + {}".format(z(y), z(x))

        answer = x + y

    # Subtraction
    elif question_line[0] == "S":
        # "AN" is not written
        if len(question_line) == 5:
            if random.randint(1, 2) == 1:
                question = "{} - {}".format(z(x + y), z(y))
                answer = x
            else:
                question = "{} - {}".format(z(x + y), z(x))
                answer = y

        # AN _is_ written (allow negatives)
        else:
            if random.randint(1, 2) == 1:
                question = "{} - {}".format(z(x), z(y))
                answer = x - y
            else:
                question = "{} - {}".format(z(y), z(x))
                answer = y - x


    # Multiplication
    elif question_line[0] == "M":
        if random.randint(1, 2) == 1:
            question = "{} × {}".format(z(x), z(y))
        else:
            question = "{} × {}".format(z(y), z(x))

        answer = x * y

    # Division
    elif question_line[0] == "D":
        if random.randint(1, 2) == 1:
            # Make sure no division by zero
            while y == 0:
                y = random.randint(int(question_line[3]), int(question_line[4]))

            question = "{} ÷ {}".format(z(x * y), z(y))
            answer = x
        else:
            # Make sure no division by zero
            while x == 0:
                x = random.randint(int(question_line[1]), int(question_line[2]))

            question = "{} ÷ {}".format(z(x * y), z(x))
            answer = y

    # Exponents
    elif question_line[0] == "E":
        question = "{}^{}".format(x, y)
        answer = x ** y

    # Roots
    elif question_line[0] == "R":
        if y == 2:
            question = "sqrt {}".format(x**y)
        elif y == 3:
            question = "cube root of {}".format(x**y)
        else:
            question = "{}th root of {}".format(y, x**y)

        answer = x

    return {
            "question": question,
            "answer": answer
            }

def configure(skill):
    with open("auto_config") as auto_config:
        lines = auto_config.readlines()

        # Find the correct line for the skill
        # Sample skill config line: "2.3 25 0.75 13"
        for line in lines:
            if line[:3] == skill:
                config = line[3:].split()
                return {
                        "total_time": int(float(config[0])),
                        "decrement": float(config[1]),
                        "threshold": int(float(config[2]))
                        }

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

def custom_menu(stdscr, sel_row):
    option_text = ["Select a level."]

    # Add the level titles to the options list
    with open("custom/levels") as custom_levels:
        lines = custom_levels.readlines()

        for line in lines:
            if lines.index(line) == 0:
                continue

            option_text.append(line.split()[0])

    # Calculate the y positions
    y_positions = [2]
    for number in range(2, len(option_text)):
        if number % 2 == 1:
            y_positions.append(y_positions[-1] + 1)
        else:
            y_positions.insert(0, y_positions[0] - 1)

    # Add the y position for the "select a level" text
    if y_positions[0] < -3:
        y_positions.insert(0, y_positions[0] - 2)
    else:
        y_positions.insert(0, -5)

    # Compile it into one list of dictionaries
    options = []
    for i in range(len(option_text)):
        options.append({
            "text": option_text[i],
            "y": y_positions[i]
            })

    # Draw everything onto the screen
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
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    skills = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2", "4.3", "4.4", "5.1", "5.2", "5.3", "5.4", "SSS"]

    # Decide whether or not to create the file
    create = True

    if os.path.exists("auto_progress"):
        create = False

        # If you have a progress file, get the saved skill from it
        with open("auto_progress") as auto_progress:
            try:
                skill = skills.index(auto_progress.readlines()[0])

            except:
                # They have a file but something is wrong with it
                create = True

    # Create the skills file if it doesn't exist
    if create:
        skill = 0

        with open("auto_progress", "w") as auto_progress:
            auto_progress.write("1.1")

    # Starting screen
    state = "main_menu"
    sel_row = 1
    main_menu(stdscr, sel_row)

    # Main loop
    while 1:
        # Reduce CPU usage (see top of file more info)
        stdscr.timeout(LAG)

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

                    question_object = get_question(skills[skill])
                    question = question_object["question"]
                    answer = question_object["answer"]

                    config_object = configure(skills[skill])
                    sec_total = config_object["total_time"]
                    sec_rem = sec_total
                    decrement = config_object["decrement"]
                    threshold = config_object["threshold"]

                    wrong = 0

                    current_value = ""

                    question_start = datetime.datetime.now()

                    bars = round(sec_total / sec_rem * 20)

                else:
                    state = "custom_menu"
                    sel_row = 1
                    custom_menu(stdscr, sel_row)

        # Auto Mode
        elif state == "auto":
            # Calculate bar numbers
            sec_rem = sec_total - (datetime.datetime.now() - question_start).seconds
            sec_rem -= wrong # Split the bar in half every time you get it wrong
            bars = round(sec_rem / sec_total * 20)

            # Running out of time
            if sec_rem <= 0:
                state = "fail"

                stdscr.clear()

                text("You ran out of time.", -5, stdscr)

                # Show correct answer
                text("{} = {}".format(question, answer), -1, stdscr)

                # Instructions
                text("Press ENTER to try again.", 4, stdscr)

                # Quesion resetting is handled in the fail state
                continue

            # Avoid having decimals by default
            if sec_rem > 1:
                sec_rem = int(sec_rem)

            # Clear old number
            if sec_rem < 10:
                sec_rem = " {}".format(sec_rem)

            # Skill
            text(str(skills[skill]), -5, stdscr)

            # Question
            text("{} = ?".format(question), -1, stdscr)

            # Respose
            text("{}> {}_{}".format(" "*12, current_value, " "*12), 0, stdscr)

            # Time bar
            text("|{bar}{space}|".format(bar="█"*bars, space=" "*(20-bars)), 3, stdscr)

            # Time text
            text("{sec}s left".format(sec=sec_rem), 4, stdscr)

            # 0-9
            if key in range(48, 58):
                current_value += str(key - 48)

                # Make sure value doesn't exceed space
                if len(current_value) > 6:
                    current_value = current_value[:-1]

            # Input negative numbers
            if key == 45:
                current_value += "-"

                # Make sure value doesn't exceed space
                if len(current_value) > 6:
                    current_value = current_value[:-1]

            # Backspace
            elif key in [8, curses.KEY_BACKSPACE]:
                current_value = current_value[:-1]

            # Make sure the user submitted a number, not "--" or something
            # Enter, to submit an answer
            elif key in [curses.KEY_ENTER, 10, 13] and current_value.count("-") != len(current_value):
                if len(current_value) > 0 and int(current_value) == answer:
                    # Update to next question

                    # Clear screen to avoid extra characters
                    stdscr.clear()

                    # Use decrement
                    sec_total -= decrement

                    # Go to next skill if you finish the current one
                    if sec_total < threshold:
                        skill += 1

                        # Update the skill in the savefile
                        with open("auto_progress", "w") as auto_progress:
                            auto_progress.write(skills[skill])

                        config_object = configure(skills[skill])
                        sec_total = config_object["total_time"]
                        decrement = config_object["decrement"]
                        threshold = config_object["threshold"]

                    # Get the new question
                    question_object = get_question(skills[skill])
                    question = question_object["question"]
                    answer = question_object["answer"]

                    wrong = 0
                    current_value = ""
                    question_start = datetime.datetime.now()

                elif len(current_value) > 0:
                    # First get the remaining seconds (it's currently a string)
                    sec_rem = sec_total - (datetime.datetime.now() - question_start).seconds
                    sec_rem -= wrong
                    wrong += math.floor(sec_rem / 2)

                    # Clear typed answer
                    current_value = ""

        # Custom mode
        elif state == "custom_menu":
            # state = "custom_menu"
            # sel_row = 1
            # custom_menu(stdscr, sel_row)
            # Pressing 'up' or 'k' selects the "Auto Mode" option
            if key in [curses.KEY_UP, 107]:
                sel_row = 1
                custom_menu(stdscr, sel_row)

            # Pressing 'down' or 'j' selects the "Custom Mode" option
            elif key in [curses.KEY_DOWN, 106]:
                sel_row = 2
                custom_menu(stdscr, sel_row)

            # Pressing enter goes into the option
            # elif key in [curses.KEY_ENTER, 10, 13]:
            #     stdscr.clear()

            #     if sel_row == 1:
            #         state = "auto"

            #         question_object = get_question(skills[skill])
            #         question = question_object["question"]
            #         answer = question_object["answer"]

            #         config_object = configure(skills[skill])
            #         sec_total = config_object["total_time"]
            #         sec_rem = sec_total
            #         decrement = config_object["decrement"]
            #         threshold = config_object["threshold"]

            #         wrong = 0

        # Game Over screen
        elif state == "fail" and key in [curses.KEY_ENTER, 10, 13]:
            # Reset
            sec_total = config_object["total_time"]
            wrong = 0
            current_value = ""
            question_start = datetime.datetime.now()

            # Get the new question
            question_object = get_question(skills[skill])
            question = question_object["question"]
            answer = question_object["answer"]

            # Run everything again
            state = "auto"

            # Remove noise from Game Over screen
            stdscr.clear()

curses.wrapper(main)
