import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt




def read_signal(file_name):


    indices = []
    samples = []

    with open(file_name, "r") as file:

        # Skip the first 3 lines
        file.readline()
        file.readline()
        file.readline()

        # Read samples
        line = file.readline()

        while line:

            parts = line.strip().split()

            if len(parts) == 2:

                index = int(parts[0])
                value = float(parts[1])

                indices.append(index)
                samples.append(value)

            line = file.readline()

    return indices, samples




def display_signal(indices, samples, title):

    plt.figure(figsize=(8, 5))

    plt.stem(indices, samples)

    plt.xlabel("n")
    plt.ylabel("Amplitude")

    plt.title(title)

    plt.grid(True)

    plt.axhline(0, color="black", linewidth=0.8)

    plt.show()



signals = []



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



def add_signals():

    selected = signal_list.curselection()

    if len(selected) < 2:

        messagebox.showwarning(
            "Warning",
            "Please select at least two signals."
        )

        return

    result = {}


    for position in selected:

        signal = signals[position]


        for index, value in zip(
                signal["indices"],
                signal["samples"]):

            if index in result:

                result[index] += value

            else:

                result[index] = value


    indices = sorted(result.keys())

    # Get values in the same order
    samples = []

    for index in indices:

        samples.append(
            result[index]
        )

    display_signal(
        indices,
        samples,
        "Addition Result"
    )



def multiply_signal():

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

    indices = signal["indices"].copy()

    samples = []

    for value in signal["samples"]:

        samples.append(
            value * constant
        )

    display_signal(
        indices,
        samples,
        "Multiplication Result"
    )



def subtract_signals():

    selected = signal_list.curselection()

    if len(selected) != 2:

        messagebox.showwarning(
            "Warning",
            "Please select exactly two signals."
        )

        return

    signal1 = signals[selected[0]]
    signal2 = signals[selected[1]]

    result = {}

    # First signal
    for index, value in zip(
            signal1["indices"],
            signal1["samples"]):

        result[index] = value

    # Subtract second signal
    for index, value in zip(
            signal2["indices"],
            signal2["samples"]):

        if index in result:

            result[index] -= value

        else:

            result[index] = -value

    indices = sorted(result.keys())

    samples = []

    for index in indices:

        samples.append(
            result[index]
        )

    display_signal(
        indices,
        samples,
        "Subtraction Result"
    )


def shift_signal():

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

    indices = []

    # -----------------------------------------------------
    # x[n + k]
    #
    # k = +3  -> advance 3 -> move LEFT
    #
    # k = -3  -> delay 3   -> move RIGHT
    # -----------------------------------------------------

    for index in signal["indices"]:

        indices.append(
            index - k
        )

    samples = signal["samples"].copy()

    display_signal(
        indices,
        samples,
        "Shifted Signal"
    )



def fold_signal():

    selected = signal_list.curselection()

    if len(selected) != 1:

        messagebox.showwarning(
            "Warning",
            "Please select one signal."
        )

        return

    signal = signals[selected[0]]

    new_indices = []
    new_samples = []

    # x[-n]
    for i in range(
            len(signal["indices"]) - 1,
            -1,
            -1):

        new_indices.append(
            -signal["indices"][i]
        )

        new_samples.append(
            signal["samples"][i]
        )

    display_signal(
        new_indices,
        new_samples,
        "Folded Signal x[-n]"
    )

#=======================Gui===========================


root = tk.Tk()

root.title(
    "Digital Signal Processing - Task 1"
)

root.geometry(
    "600x700"
)



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



load_button = tk.Button(
    root,
    text="Load Signal",
    width=30,
    command=load_signal
)

load_button.pack(pady=8)



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



display_button = tk.Button(
    root,
    text="Display Selected Signal",
    width=30,
    command=show_selected_signal
)

display_button.pack(pady=6)



add_button = tk.Button(
    root,
    text="Add Selected Signals",
    width=30,
    command=add_signals
)

add_button.pack(pady=6)



subtract_button = tk.Button(
    root,
    text="Subtract Two Signals",
    width=30,
    command=subtract_signals
)

subtract_button.pack(pady=6)



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
    command=multiply_signal
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
    command=shift_signal
)

shift_button.pack(pady=6)


# =========================================================
# FOLDING
# =========================================================

fold_button = tk.Button(
    root,
    text="Fold / Reverse Signal",
    width=30,
    command=fold_signal
)

fold_button.pack(pady=6)


# =========================================================
# START PROGRAM
# =========================================================

root.mainloop()