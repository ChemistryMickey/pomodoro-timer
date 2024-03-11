from datetime import datetime, timedelta
import pyttsx3
import sys
from time import sleep
from tqdm.auto import tqdm

USE_VOICE = True
WARNING_MINUTES = 5
DEBUG_PRINT = False


def main():
    print(tomato_banner())
    pomodoro_parameters = get_parameters()
    if DEBUG_PRINT:
        print(pomodoro_parameters)

    input("Press enter to start.")
    cur_round = 1  # eh, humans are 1-indexed
    while True:
        work_round(cur_round, pomodoro_parameters)
        break_round(cur_round, pomodoro_parameters)

        cur_round += 1


def break_round(cur_round: int, pomodoro_parameters: dict[str, int]) -> None:
    # Get the amount of break time
    if cur_round % pomodoro_parameters["rounds before long break"] == 0:
        speak(f"Time for a {pomodoro_parameters['long break']} minute long-break")
        break_mins = pomodoro_parameters["long break"]
        break_warning_mins = WARNING_MINUTES
    else:
        speak(f"Time for a {pomodoro_parameters['short break']} minute break")
        break_mins = pomodoro_parameters["short break"]
        break_warning_mins = None  # NO WARNING

    # Actually take the break
    for minute in tqdm(range(break_mins), desc=f"{break_mins} break in progress..."):
        minute_end = datetime.now() + timedelta(minutes=1)

        if (
            break_warning_mins is not None
            and minute == (break_mins - break_warning_mins)
            and pomodoro_parameters["warn"]
        ):
            speak(f"{break_warning_mins} minute warning.")

        wait_seconds = (minute_end - datetime.now()).total_seconds()
        sleep(wait_seconds)

    speak_and_print(f"Round {cur_round} break complete")

    if not pomodoro_parameters["skip input break"]:
        speak_and_print(f"Press enter to begin next work round.")
        input()


def work_round(cur_round: int, pomodoro_parameters: dict[str, int]) -> None:
    speak(
        f"Starting round {cur_round}. Work for {pomodoro_parameters['work']} minutes!"
    )
    for minute in tqdm(
        range(pomodoro_parameters["work"]),
        desc=f"Round {cur_round} work in progress...",
    ):
        minute_end = datetime.now() + timedelta(minutes=1)

        if (
            minute == (pomodoro_parameters["work"] - WARNING_MINUTES)
            and pomodoro_parameters["warn"]
        ):
            speak(f"{WARNING_MINUTES} minute warning.")

        wait_seconds = (minute_end - datetime.now()).total_seconds()
        sleep(wait_seconds)

    speak_and_print(f"Work for round {cur_round} completed")

    if not pomodoro_parameters["skip input break"]:
        speak_and_print(f"Press enter to begin break.")
        input()


def get_parameters():
    default_parameters = {
        "work": 30,
        "short break": 5,
        "long break": 20,
        "rounds before long break": 3,
        "warn": True,
        "skip input break": False,
    }
    if len(sys.argv) >= 2:
        # process command line arguments
        for i, arg in enumerate(sys.argv[1:]):
            try:
                if arg.isnumeric():
                    continue

                if "-w" in arg or "--work" in arg:
                    default_parameters["work"] = int(sys.argv[i + 2])
                    if default_parameters["work"] < 1:
                        raise Exception(f"Work time must be >= 1")
                elif "-s" in arg or "--short_break" in arg:
                    default_parameters["short break"] = int(sys.argv[i + 2])
                    if default_parameters["short break"] < 1:
                        raise Exception(f"Short break time must be >= 1")
                elif "-l" in arg or "--long_break" in arg:
                    default_parameters["long break"] = int(sys.argv[i + 2])
                    if default_parameters["long break"] < 1:
                        raise Exception(f"Long break time must be >= 1")
                elif "-p" in arg or "--period" in arg:
                    default_parameters["rounds before long break"] = int(
                        sys.argv[i + 2]
                    )
                    if default_parameters["rounds before long break"] <= 0:
                        raise Exception(f"Rounds before break must be >= 1")
                elif "-nw" in arg or "--no_warning" in arg:
                    default_parameters["warn"] = False
                elif "-sib" in arg or "--skip_input_break" in arg:
                    default_parameters["skip input break"] = True
                else:
                    raise Exception("Invalid Argument")
            except:
                print_help_text()

    return default_parameters


def print_help_text():
    help_text = """
Create a progress bar that increments based on the "pomodoro" technique for productivity.
This alternates periods of work/break where the break is extended once per "period" work cycles
Default Parameters (no additional arguments):
    work time = 30 [minutes]
    short break = 5 [minutes]
    long break = 20 [minutes]
    break cycle period = 3 [rounds] (i.e., every third round will be a long break (short, short, long, short short, long, ...))

Arguments:
    "-w #" or "--work #":           The duration (in minutes) of the work session
    "-s #" or "--short_break #":    The duration (in minutes) of the short break session
    "-l #" or "--long_break #":     The duration (in minutes) of the long break session
    "-p #" or "--period #":         The number work/break sessions before the cycle repeats
    "-nw" or "--no_warning":        Omit the 5 minute warning on work sessions and long breaks
    "-sib" or "--skip_input_break"  Remove the need for the user to press enter to move onto the next work/break round

Constraints:
    - All times must be >= 1 minute
    - Period between long breaks must be >= 1

Examples:
    custom-pomodoro-timer
    custom-pomodoro-timer -w 30 -sib
    custom-pomodoro-timer -w 45 -sb 7 -lb 20 -p 4
    custom-pomodoro-timer --work 45 --short_break 7 --long_break 20 --period 4
"""
    print(help_text)
    sys.exit(1)


def speak(line: str):
    if USE_VOICE:
        speaker = pyttsx3.init()
        speaker.say(line)
        speaker.runAndWait()


def speak_and_print(line: str):
    print(f"[{datetime.now()}]: {line}")
    speak(line)


def tomato_banner() -> str:
    # Created using https://www.asciiart.eu/image-to-ascii
    return """
############################################################
#                                                          #
#    ____                           _                 _    #
#   |  _ \ ___  _ __ ___   ___   __| | ___  _ __ ___ | |   #
#   | |_) / _ \| '_ ` _ \ / _ \ / _` |/ _ \| '__/ _ \| |   #
#   |  __/ (_) | | | | | | (_) | (_| | (_) | | | (_) |_|   #
#   |_|   \___/|_| |_| |_|\___/ \__,_|\___/|_|  \___/(_)   #
#                                                          #
#                             +++                          #
#                             -+                           #
#                     +-++   +++ -#   +                    #
#            +    +++++++++++++++++#######                 #
#              ++++++++++--++++++++++-++++###              #
#           ++++++++++++++-+++++##++++##########   +       #
#         +++++++++++++++++++++++####---##########         #
#        ++++++++++++++++++++++++######++++########        #
#       +++++++++++++++++++++++++++#######++++######       #
#      +++++++----++++++++++++++++++#################      #
#     +++++++-----+++++++++++++++++++################      #
#     ++++++++---++++++++++++++++++++#################     #
#    ++++++++++++++++++++++++++++++++#################     #
#    +++++++++-++++++++++++++++++++++#################     #
#    +++++++++++++++++++++++++++++++#################      #
#     +++++++++++++++++++++++++++++##################      #
#     ++++++++++++++++++++++++++++###################      #
#      ++++++++++++++++++++++++++###################       #
#       ++++++++++++++++++++++++###################        #
#        +++++++++++++++++++++####################         #
#         #######+++++++########################           #
#           ##################################             #
#              ############################                #
#                  #####################                   #
#                                                          #
#                                                          #
############################################################
"""


if __name__ == "__main__":
    main()
