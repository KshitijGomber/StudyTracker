# Study Tracker App

A lightweight Python application to help you balance your study and break times. For every 3 minutes of study time, you earn 1 minute of break time. If you overuse your break time, the app tracks "break debt" (negative break time) and plays an alarm when you go into debt. You can also stop sessions anytime using the "Chill Mode" without resetting your accumulated time.

## Features

- **Study & Break Management:**  
  - Accumulate 1 minute of break time for every 3 minutes of study.
  - Deduct break time during break sessions in real time.
  - If break time is exhausted, it goes into negative (break debt) and an alarm plays only once when entering debt.

- **Graphical User Interface (GUI):**  
  - Built using Tkinter for a simple, clean interface.
  - Live updates of study and break times displayed in "Xm Ys" format.
  - Visual cues (e.g., optional color changes) can indicate break debt.

- **Threaded Sessions:**  
  - Study and break sessions run concurrently using threads.
  - Guard flags prevent multiple sessions from overlapping.

- **Chill Mode:**  
  - Instantly stop both study and break sessions without resetting your progress.

## How It Works

1. **Study Session:**  
   - When you start a study session, the timer begins.
   - Every 3 minutes of study time adds 1 minute to your available break time.
   - If you’re in break debt (negative break time), studying repays the debt until your break time is non-negative.

2. **Break Session:**  
   - When you start a break session, available break time is consumed in real time.
   - If you run out of break time and it goes negative, an alarm sounds only once per debt occurrence.

3. **Chill Mode:**  
   - Stops any running study or break session without resetting your accumulated study and break time.

## Requirements

- **Python 3.x**  
- **Tkinter:** Typically included with Python installations.
- **chime:** Used for playing an alarm sound. Install via pip:
  ```bash
  pip install chime
