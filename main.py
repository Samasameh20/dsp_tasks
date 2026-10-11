
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt

from signal_operations import (
    read_signal,
    add_signals,
    subtract_signals,
    multiply_signal,
    shift_signal,
    fold_signal,
    generate_signal
)


# =========================================================
# SIGNAL STORAGE
# =========================================================

signals = []


# =========================================================
# DISPLAY SIGNALS
# =========================================================

def display_signals(selected_signals):

    if not selected_signals:
        messagebox.showwarning(
            "Warning",
            "Please select at least one signal."
        )
        return

    mode = display_mode.get()

    fig, ax = plt.subplots(figsize=(9, 5))

    for signal in selected_signals:

        indices = signal["indices"]
        samples = signal["samples"]
        name = signal["name"]

        if mode == "Continuous":

            ax.plot(
                indices,
                samples,
                marker="o",
                label=name
            )

        else:

            markerline, stemlines, baseline = ax.stem(
                indices,
                samples,
                label=name
            )

    ax.set_xlabel("Index n")
    ax.set_ylabel("Amplitude")
    ax.set_title("Signal Display")
    ax.grid(True)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.legend()

    plt.tight_layout()
    plt.show()


# =========================================================
# SAVE RESULT IN SIGNAL LIST
# =========================================================

def save_result(indices, samples, name):

    result = {
        "name": name,
        "indices": indices,
        "samples": samples
    }

    signals.append(result)

    signal_list.insert(tk.END, name)

    return result


# =========================================================
# LOAD SIGNAL FROM FILE
# =========================================================

def load_signal():

    file_name = filedialog.askopenfilename(
        title="Select Signal File",
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_name:
        return

    try:

        indices, samples = read_signal(file_name)

        if not indices:
            messagebox.showerror(
                "Error",
                "No valid signal samples were found."
            )
            return

        name = os.path.basename(file_name)

        save_result(indices, samples, name)

        messagebox.showinfo(
            "Success",
            "Signal loaded successfully!"
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            "Could not read the signal:\n" + str(error)
        )


# =========================================================
# GET SELECTED SIGNALS
# =========================================================

def get_selected_signals():

    selected = signal_list.curselection()

    return [
        signals[position]
        for position in selected
    ]


# =========================================================
# DISPLAY SELECTED SIGNAL(S)
# =========================================================

def show_selected_signals():

    selected = get_selected_signals()

    if len(selected) > 2:
        messagebox.showwarning(
            "Warning",
            "Select one or two signals to display."
        )
        return

    display_signals(selected)


# =========================================================
# ADD SIGNALS
# =========================================================

def add_selected_signals():

    selected = get_selected_signals()

    if len(selected) < 2:
        messagebox.showwarning(
            "Warning",
            "Select at least two signals."
        )
        return

    indices, samples = add_signals(*selected)

    result = save_result(
        indices,
        samples,
        "Addition Result"
    )

    display_signals([result])


# =========================================================
# SUBTRACT SIGNALS
# =========================================================

def subtract_selected_signals():

    selected = get_selected_signals()

    if len(selected) != 2:
        messagebox.showwarning(
            "Warning",
            "Select exactly two signals."
        )
        return

    indices, samples = subtract_signals(
        selected[0],
        selected[1]
    )

    result = save_result(
        indices,
        samples,
        "Subtraction Result"
    )

    display_signals([result])


# =========================================================
# MULTIPLY SIGNAL
# =========================================================

def multiply_selected_signal():

    selected = get_selected_signals()

    if len(selected) != 1:
        messagebox.showwarning(
            "Warning",
            "Select exactly one signal."
        )
        return

    try:
        constant = float(constant_entry.get())

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid multiplication constant."
        )
        return

    indices, samples = multiply_signal(
        selected[0],
        constant
    )

    result = save_result(
        indices,
        samples,
        "Multiplication Result"
    )

    display_signals([result])


# =========================================================
# SHIFT SIGNAL
# =========================================================

def shift_selected_signal():

    selected = get_selected_signals()

    if len(selected) != 1:
        messagebox.showwarning(
            "Warning",
            "Select exactly one signal."
        )
        return

    try:
        k = int(shift_entry.get())

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter an integer for k."
        )
        return

    indices, samples = shift_signal(
        selected[0],
        k
    )

    result = save_result(
        indices,
        samples,
        "Shift Result"
    )

    display_signals([result])


# =========================================================
# FOLD SIGNAL
# =========================================================

def fold_selected_signal():

    selected = get_selected_signals()

    if len(selected) != 1:
        messagebox.showwarning(
            "Warning",
            "Select exactly one signal."
        )
        return

    indices, samples = fold_signal(selected[0])

    result = save_result(
        indices,
        samples,
        "Folded Signal"
    )

    display_signals([result])


# =========================================================
# GENERATE SINE OR COSINE
# =========================================================

def generate_selected_signal(signal_type):

    try:

        amplitude = float(amplitude_entry.get())
        phase = float(phase_entry.get())
        frequency = float(frequency_entry.get())
        sampling_frequency = float(
            sampling_frequency_entry.get()
        )
        duration = float(duration_entry.get())

        indices, samples = generate_signal(
            signal_type,
            amplitude,
            phase,
            frequency,
            sampling_frequency,
            duration
        )

        name = (
            signal_type.capitalize()
            + " A=" + str(amplitude)
            + " f=" + str(frequency)
        )

        result = save_result(
            indices,
            samples,
            name
        )

        display_signals([result])

    except ValueError as error:

        messagebox.showerror(
            "Invalid Input",
            str(error)
        )


# =========================================================
# GUI WINDOW
# =========================================================

root = tk.Tk()

root.title("Digital Signal Processing - Task 2")
root.geometry("700x900")


# =========================================================
# MENU
# =========================================================

menu_bar = tk.Menu(root)

generation_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

generation_menu.add_command(
    label="Sine Wave",
    command=lambda: generate_selected_signal("sine")
)

generation_menu.add_command(
    label="Cosine Wave",
    command=lambda: generate_selected_signal("cosine")
)

menu_bar.add_cascade(
    label="Signal Generation",
    menu=generation_menu
)

root.config(menu=menu_bar)


# =========================================================
# TITLE
# =========================================================

tk.Label(
    root,
    text="Digital Signal Processing",
    font=("Arial", 20, "bold")
).pack(pady=10)

tk.Label(
    root,
    text="Task 1 + Task 2",
    font=("Arial", 12)
).pack(pady=5)


# =========================================================
# LOAD SIGNAL
# =========================================================

tk.Button(
    root,
    text="Load Signal from File",
    width=30,
    command=load_signal
).pack(pady=6)


# =========================================================
# SIGNAL LIST
# =========================================================

tk.Label(
    root,
    text="Loaded and Generated Signals",
    font=("Arial", 11, "bold")
).pack(pady=5)

signal_list = tk.Listbox(
    root,
    width=65,
    height=7,
    selectmode=tk.MULTIPLE,
    exportselection=False
)

signal_list.pack(pady=5)


# =========================================================
# DISPLAY MODE
# =========================================================

tk.Label(
    root,
    text="Display Representation:"
).pack(pady=3)

display_mode = tk.StringVar(value="Discrete")

mode_menu = tk.OptionMenu(
    root,
    display_mode,
    "Discrete",
    "Continuous"
)

mode_menu.pack(pady=3)


tk.Button(
    root,
    text="Display Selected Signal(s)",
    width=30,
    command=show_selected_signals
).pack(pady=5)


# =========================================================
# TASK 1 OPERATIONS
# =========================================================

tk.Button(
    root,
    text="Add Selected Signals",
    width=30,
    command=add_selected_signals
).pack(pady=4)

tk.Button(
    root,
    text="Subtract Two Signals",
    width=30,
    command=subtract_selected_signals
).pack(pady=4)


tk.Label(
    root,
    text="Multiplication Constant:"
).pack(pady=2)

constant_entry = tk.Entry(root, width=20)
constant_entry.pack(pady=2)

tk.Button(
    root,
    text="Multiply Signal",
    width=30,
    command=multiply_selected_signal
).pack(pady=4)


tk.Label(
    root,
    text="Shift k (+ = advance, - = delay):"
).pack(pady=2)

shift_entry = tk.Entry(root, width=20)
shift_entry.pack(pady=2)

tk.Button(
    root,
    text="Shift Signal",
    width=30,
    command=shift_selected_signal
).pack(pady=4)

tk.Button(
    root,
    text="Fold / Reverse Signal",
    width=30,
    command=fold_selected_signal
).pack(pady=4)


# =========================================================
# TASK 2: SIGNAL GENERATION INPUTS
# =========================================================

tk.Label(
    root,
    text="Signal Generation Parameters",
    font=("Arial", 12, "bold")
).pack(pady=7)


tk.Label(
    root,
    text="Amplitude A:"
).pack()

amplitude_entry = tk.Entry(root, width=20)
amplitude_entry.insert(0, "1")
amplitude_entry.pack(pady=2)


tk.Label(
    root,
    text="Phase Shift θ (degrees):"
).pack()

phase_entry = tk.Entry(root, width=20)
phase_entry.insert(0, "0")
phase_entry.pack(pady=2)


tk.Label(
    root,
    text="Analog Frequency f (Hz):"
).pack()

frequency_entry = tk.Entry(root, width=20)
frequency_entry.insert(0, "5")
frequency_entry.pack(pady=2)


tk.Label(
    root,
    text="Sampling Frequency fs (Hz):"
).pack()

sampling_frequency_entry = tk.Entry(root, width=20)
sampling_frequency_entry.insert(0, "50")
sampling_frequency_entry.pack(pady=2)


tk.Label(
    root,
    text="Duration (seconds):"
).pack()

duration_entry = tk.Entry(root, width=20)
duration_entry.insert(0, "1")
duration_entry.pack(pady=2)


tk.Label(
    root,
    text="Choose Signal Generation from the top menu",
    font=("Arial", 10, "italic")
).pack(pady=8)


# =========================================================
# START GUI
# =========================================================

root.mainloop()
