import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

from signal_operations import (
    read_signal,
    add_signals,
    subtract_signals,
    multiply_signal,
    shift_signal,
    fold_signal
)


# =========================================================
# SIGNALS
# =========================================================

signals = []


# =========================================================
# DISPLAY SIGNAL
# =========================================================

def display_signal(indices, samples, title):

    plt.figure(figsize=(8, 5))

    plt.stem(indices, samples)

    plt.xlabel("n")
    plt.ylabel("Amplitude")

    plt.title(title)

    plt.grid(True)

    plt.axhline(0, color="black", linewidth=0.8)

    plt.show()


# =========================================================
# LOAD SIGNAL
# =========================================================

def load_signal():

    file_name = filedialog.askopenfilename(
        title="Select Signal File",
        filetypes=[
            ("Text Files", "*.txt")
        ]
    )

    if file_name == "":
        return

    try:

        indices, samples = read_signal(file_name)

        signal = {
            "name": file_name.split("/")[-1],
            "indices": indices,
            "samples": samples
        }

        signals.append(signal)

        signal_list.insert(
            tk.END,
            signal["name"]
        )

        messagebox.showinfo(
            "Success",
            "Signal loaded successfully!"
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            "Could not read the signal:\n"
            + str(error)
        )


# =========================================================
# DISPLAY SELECTED SIGNAL
# =========================================================

def show_selected_signal():

    selected = signal_list.curselection()

    if len(selected) != 1:

        messagebox.showwarning(
            "Warning",
            "Please select one signal."
        )

        return

    signal = signals[selected[0]]

    display_signal(
        signal["indices"],
        signal["samples"],
        signal["name"]
    )


# =========================================================
# ADD SIGNALS
# =========================================================

def add_selected_signals():

    selected = signal_list.curselection()

    if len(selected) < 2:

        messagebox.showwarning(
            "Warning",
            "Please select at least two signals."
        )

        return

    signal1 = signals[selected[0]]
    signal2 = signals[selected[1]]

    indices, samples = add_signals(
        signal1,
        signal2
    )

    display_signal(
        indices,
        samples,
        "Addition Result"
    )


# =========================================================
# SUBTRACT SIGNALS
# =========================================================

def subtract_selected_signals():

    selected = signal_list.curselection()

    if len(selected) != 2:

        messagebox.showwarning(
            "Warning",
            "Please select exactly two signals."
        )

        return

    signal1 = signals[selected[0]]
    signal2 = signals[selected[1]]

    indices, samples = subtract_signals(
        signal1,
        signal2
    )

    display_signal(
        indices,
        samples,
        "Subtraction Result"
    )


# =========================================================
# MULTIPLY SIGNAL
# =========================================================

def multiply_selected_signal():

    selected = signal_list.curselection()

    if len(selected) != 1:

        messagebox.showwarning(
            "Warning",
            "Please select one signal."
        )

        return

    try:

        constant = float(
            constant_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter a valid number."
        )

        return

    signal = signals[selected[0]]

    indices, samples = multiply_signal(
        signal,
        constant
    )

    display_signal(
        indices,
        samples,
        "Multiplication Result"
    )


# =========================================================
# SHIFT SIGNAL
# =========================================================

def shift_selected_signal():

    selected = signal_list.curselection()

    if len(selected) != 1:

        messagebox.showwarning(
            "Warning",
            "Please select one signal."
        )

        return

    try:

        k = int(
            shift_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter an integer."
        )

        return

    signal = signals[selected[0]]

    indices, samples = shift_signal(
        signal,
        k
    )

    display_signal(
        indices,
        samples,
        "Shifted Signal"
    )


# =========================================================
# FOLD SIGNAL
# =========================================================

def fold_selected_signal():

    selected = signal_list.curselection()

    if len(selected) != 1:

        messagebox.showwarning(
            "Warning",
            "Please select one signal."
        )

        return

    signal = signals[selected[0]]

    indices, samples = fold_signal(
        signal
    )

    display_signal(
        indices,
        samples,
        "Folded Signal x[-n]"
    )


# =========================================================
# GUI
# =========================================================

root = tk.Tk()

root.title(
    "Digital Signal Processing - Task 1"
)

root.geometry(
    "600x700"
)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    root,
    text="Digital Signal Processing",
    font=("Arial", 20, "bold")
)

title.pack(pady=15)


subtitle = tk.Label(
    root,
    text="Signal Processing Task 1",
    font=("Arial", 12)
)

subtitle.pack(pady=5)


# =========================================================
# LOAD
# =========================================================

load_button = tk.Button(
    root,
    text="Load Signal",
    width=30,
    command=load_signal
)

load_button.pack(pady=8)


# =========================================================
# SIGNAL LIST
# =========================================================

list_label = tk.Label(
    root,
    text="Loaded Signals:",
    font=("Arial", 11, "bold")
)

list_label.pack(pady=5)


signal_list = tk.Listbox(
    root,
    width=50,
    height=8,
    selectmode=tk.MULTIPLE
)

signal_list.pack(pady=5)


# =========================================================
# DISPLAY
# =========================================================

display_button = tk.Button(
    root,
    text="Display Selected Signal",
    width=30,
    command=show_selected_signal
)

display_button.pack(pady=6)


# =========================================================
# ADDITION
# =========================================================

add_button = tk.Button(
    root,
    text="Add Selected Signals",
    width=30,
    command=add_selected_signals
)

add_button.pack(pady=6)


# =========================================================
# SUBTRACTION
# =========================================================

subtract_button = tk.Button(
    root,
    text="Subtract Two Signals",
    width=30,
    command=subtract_selected_signals
)

subtract_button.pack(pady=6)


# =========================================================
# MULTIPLICATION
# =========================================================

constant_label = tk.Label(
    root,
    text="Multiplication Constant:"
)

constant_label.pack(pady=3)


constant_entry = tk.Entry(
    root,
    width=20
)

constant_entry.pack(pady=3)


multiply_button = tk.Button(
    root,
    text="Multiply Signal",
    width=30,
    command=multiply_selected_signal
)

multiply_button.pack(pady=6)


# =========================================================
# SHIFT
# =========================================================

shift_label = tk.Label(
    root,
    text="Shift k (+ = advance, - = delay):"
)

shift_label.pack(pady=3)


shift_entry = tk.Entry(
    root,
    width=20
)

shift_entry.pack(pady=3)


shift_button = tk.Button(
    root,
    text="Shift Signal",
    width=30,
    command=shift_selected_signal
)

shift_button.pack(pady=6)


# =========================================================
# FOLDING
# =========================================================

fold_button = tk.Button(
    root,
    text="Fold / Reverse Signal",
    width=30,
    command=fold_selected_signal
)

fold_button.pack(pady=6)


# =========================================================
# START PROGRAM
# =========================================================

root.mainloop()