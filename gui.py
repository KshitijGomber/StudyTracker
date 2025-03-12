from tkinter import *
import app
import threading

root = Tk()
root.title("Study Tracker")

# Set window size to maintain a 16:9 ratio
width = 500
height = int(width * 9 / 16)
root.geometry(f"{width}x{height}")
root.configure(bg="#302c34")

# Create frames for labels and buttons
label_frame = Frame(root, bg="#302c34")
button_frame = Frame(root, bg="#302c34")

label_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)  # Ensure labels expand properly
button_frame.pack(fill=X, padx=10, pady=10)  # Keep buttons visible

# Create and position labels
study_text_label = Label(label_frame, text="Study Time:", bg="#302c34", fg="white", font=("Helvetica", 14))
study_text_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

study_label = Label(label_frame, text="0m 0s", bg="#302c34", fg="white", font=("Helvetica", 14))
study_label.grid(row=0, column=1, padx=5, pady=5, sticky=E)

break_text_label = Label(label_frame, text="Break Time:", bg="#302c34", fg="white", font=("Helvetica", 14))
break_text_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

break_label = Label(label_frame, text="0m 0s", bg="#302c34", fg="white", font=("Helvetica", 14))
break_label.grid(row=1, column=1, padx=5, pady=5, sticky=E)

# Ensure labels expand equally
label_frame.grid_columnconfigure(0, weight=1)
label_frame.grid_columnconfigure(1, weight=1)

# def update_label():
#     """ Updates the labels with formatted time (e.g., 1m 30s) """
#     study_label.config(text=app.format_time(app.STUDY))
#     break_label.config(text=app.format_time(app.BREAK))
#     root.after(1000, update_label)  # Update every second

def update_label():
    """ Updates the labels with formatted time (e.g., '1m 30s' or '-2m 30s') """
    study_label.config(text=app.format_time(app.STUDY))

    # Change break time color based on debt
    if app.BREAK < 0:
        break_label.config(text=app.format_time(app.BREAK), fg="red")  # Red if in debt
    else:
        break_label.config(text=app.format_time(app.BREAK), fg="white")  # Normal color

    root.after(1000, update_label)  # Update every second

def start_study_session():
    """ Starts a study session and stops any ongoing break session """
    app.FLAG_STOP_BREAK = True
    app.FLAG_STOP_STUDY = False
    study_thread = threading.Thread(target=app.start_study, args=(7,))
    study_thread.daemon = True
    study_thread.start()

def start_break_session():
    """ Starts a break session and stops any ongoing study session """
    app.FLAG_STOP_STUDY = True
    app.FLAG_STOP_BREAK = False
    break_thread = threading.Thread(target=app.start_break)
    break_thread.daemon = True
    break_thread.start()

def chill():
    """ Stops both study and break sessions without resetting time """
    app.FLAG_STOP_STUDY = True
    app.FLAG_STOP_BREAK = True

# Create buttons with proper size
button1 = Button(button_frame, text="Study Mode", command=start_study_session,
                 bg="#61bc9a", fg="black", bd=0, font=("Helvetica", 12), height=2)
button2 = Button(button_frame, text="Break Mode", command=start_break_session,
                 bg="#ff6480", fg="black", bd=0, font=("Helvetica", 12), height=2)
button3 = Button(button_frame, text="Chill Mode", command=chill,
                 bg="#f6bc4f", fg="black", bd=0, font=("Helvetica", 12), height=2)

# Use Grid for better button layout
button1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
button2.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
button3.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# Ensure all buttons expand equally
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

update_label()  # Start the update loop
root.mainloop()
