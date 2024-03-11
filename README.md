# Pomodoro timer (Python and Rust Implementations)
A nifty little CLI pomodoro timer to sharpen my rust against my python.

## Rust:
### Dependencies:
See [Cargo.toml].

### Help Text:
```
A nifty little CLI pomodoro timer with binary sounds and a progress bar

Usage: custom-pomodoro-timer [OPTIONS]

Options:
  -w, --work <WORK>
          Duration of the work round [min] [default: 30]
  -s, --short-break <SHORT_BREAK>
          Duration of the short break round [min] [default: 5]
  -l, --long-break <LONG_BREAK>
          Duration of the long break round [min] [default: 20]
  -r, --rounds-before-long-break <ROUNDS_BEFORE_LONG_BREAK>
          Number of rounds before the pattern repeats (e.g. [short, short, long, short, short, long, ...]) [default: 3]
  -w, --warn
          Produce a series of warning beeps 5 minutes before the work or long break is over
  -i, --skip-input-break
          Skip user input before continuing to the next round (continue without user input)
  -d, --disable-all-sound
          Don't beep at all. You're missing out though. Learn binary. It'll be fun!
  -h, --help
          Print help
```
### Output:
```
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

Starting round 1. Work for 30 minutes!
Work in Progress... ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ [11m/1800s] 
```

## Python:
### Dependencies:
- pyttsx3 (Text-to-Speech to indicate a work/break period has begun/ended)
- tqdm (Progress Bar)

### Help Text:
```
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
```

### Output:
```
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

Press enter to start.
Round 1 work in progress...:   0%|                          | 0/30 [00:00<?, ?it/s]
```