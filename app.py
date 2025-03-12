import time
import chime

# Global variables for tracking time (in minutes)
STUDY = 0.0    # in minutes
BREAK = 0.0    # in minutes (can go negative)
ALARM_PLAYED = False  # flag to prevent repeated alarm calls

# Flags to control thread execution and avoid multiple sessions
FLAG_STOP_STUDY = False
FLAG_STOP_BREAK = False
IS_STUDYING = False    # Prevents multiple study threads
IS_BREAKING = False    # Prevents multiple break threads

def play_alarm():
    """Plays the alarm when break time runs out."""
    chime.theme("zelda")
    chime.success()

def format_time(minutes):
    """
    Converts time from decimal minutes to "Xm Ys" format.
    Handles negative values for break debt.
    Example: -1.5 minutes → "-1m 30s"
    """
    mins = int(abs(minutes))
    secs = int((abs(minutes) - mins) * 60)
    if minutes < 0:
        return f"-{mins}m {secs}s"
    return f"{mins}m {secs}s"

def start_study(session_duration: int = 0):
    """
    Runs a study session. For every 3 minutes of study time,
    adds 1 minute of break credit.
    If session_duration is provided (in minutes), stops after that duration.
    Prevents starting if a study session is already active.
    """
    global STUDY, BREAK, FLAG_STOP_STUDY, ALARM_PLAYED, IS_STUDYING
    if IS_STUDYING:
        return
    IS_STUDYING = True
    FLAG_STOP_STUDY = False

    # Initialize last_credit to the current STUDY time to avoid
    # re-awarding break credit for already accumulated study time.
    last_credit = STUDY  
    interval = 0.125   # Interval in seconds

    while not FLAG_STOP_STUDY:
        time.sleep(interval)
        STUDY += interval / 60.0  # Convert seconds to minutes

        # For every 3 minutes of study, add 1 minute of break credit
        if STUDY - last_credit >= 3:
            BREAK += 1
            last_credit += 3

        # Reset alarm flag if break time is non-negative
        if BREAK >= 0:
            ALARM_PLAYED = False

        # Stop session if a duration limit is set
        if session_duration > 0 and STUDY >= session_duration:
            break

    FLAG_STOP_STUDY = True  # Mark session as ended
    IS_STUDYING = False

def start_break():
    """
    Runs a break session. Consumes break credit in real time.
    Allows break credit to go into negative values (break debt) and
    plays the alarm only once when break becomes negative.
    Prevents starting if a break session is already active.
    """
    global BREAK, FLAG_STOP_BREAK, ALARM_PLAYED, IS_BREAKING
    if IS_BREAKING:
        return
    IS_BREAKING = True
    FLAG_STOP_BREAK = False

    interval = 0.125  # Interval in seconds

    while not FLAG_STOP_BREAK:
        time.sleep(interval)
        BREAK -= interval / 60.0  # Convert seconds to minutes

        # Play alarm only once when break goes negative (break debt)
        if BREAK < 0 and not ALARM_PLAYED:
            play_alarm()
            ALARM_PLAYED = True

    FLAG_STOP_BREAK = True  # Mark session as ended
    IS_BREAKING = False

def chill():
    """
    Stops both study and break sessions without resetting the accumulated time.
    """
    global FLAG_STOP_STUDY, FLAG_STOP_BREAK
    FLAG_STOP_STUDY = True
    FLAG_STOP_BREAK = True
