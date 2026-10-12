import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt

from signal_operations import (
    read_signal,
    add_signals,
    subtract_signals,
    multiply_signal,
    shift_signal,
    fold_signal,
    generate_signal,
)


# ---------------------------------------------------------
# DSP DATA AND COLORS
# ---------------------------------------------------------
signals = []

BG = "#F4F7FB"
CARD = "#FFFFFF"
SIDEBAR = "#172033"
SIDEBAR_ACTIVE = "#293750"
TEXT = "#172033"
MUTED = "#718096"
ACCENT = "#4F7DF3"
BORDER = "#E2E8F0"
SUCCESS = "#16876D"


# ---------------------------------------------------------
# ROOT WINDOW / THEME
# ---------------------------------------------------------
root = tk.Tk()
root.title("DSP Tasks")
root.geometry("1180x780")
root.minsize(980, 680)
root.configure(bg=BG)

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Modern.TEntry",
    padding=(10, 9),
    fieldbackground="#FFFFFF",
    foreground=TEXT,
    bordercolor=BORDER,
    lightcolor=BORDER,
    darkcolor=BORDER,
)

style.map(
    "Modern.TEntry",
    bordercolor=[("focus", ACCENT)],
    lightcolor=[("focus", ACCENT)],
    darkcolor=[("focus", ACCENT)],
)

style.configure(
    "Modern.TCombobox",
    padding=(8, 7),
    fieldbackground="#FFFFFF",
    background="#FFFFFF",
    foreground=TEXT,
    arrowcolor=MUTED,
)

style.map(
    "Modern.TCombobox",
    fieldbackground=[("readonly", "#FFFFFF")]
)


# ---------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------
sidebar = tk.Frame(root, bg=SIDEBAR, width=235)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)


# ---------------------------------------------------------
# SIDEBAR BRAND
# ---------------------------------------------------------
brand = tk.Frame(sidebar, bg=SIDEBAR)
brand.pack(fill="x", padx=22, pady=(28, 34))

logo = tk.Label(
    brand,
    text="∿",
    font=("Segoe UI Symbol", 27, "bold"),
    bg=ACCENT,
    fg="white",
    width=2,
    height=1
)
logo.pack(side="left", padx=(0, 11))

brand_text = tk.Frame(brand, bg=SIDEBAR)
brand_text.pack(side="left")

tk.Label(
    brand_text,
    text="DSP LAB",
    font=("Segoe UI", 11, "bold"),
    bg=SIDEBAR,
    fg="#FFFFFF"
).pack(anchor="w")

tk.Label(
    brand_text,
    text="Signal workspace",
    font=("Segoe UI", 9),
    bg=SIDEBAR,
    fg="#AAB5C7"
).pack(anchor="w", pady=(3, 0))

tk.Label(
    sidebar,
    text="WORKSPACE",
    font=("Segoe UI", 8, "bold"),
    bg=SIDEBAR,
    fg="#8996AC"
).pack(anchor="w", padx=24, pady=(0, 12))


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
nav_buttons = {}
current_task = tk.StringVar(value="task1")


def make_button(parent, text, command, primary=True, width=None):
    """Create a consistent button using Tkinter widgets."""

    if primary:
        bg = ACCENT
        fg = "#FFFFFF"
        active_bg = "#3E68D6"
        active_fg = "#FFFFFF"
    else:
        bg = "#FFFFFF"
        fg = TEXT
        active_bg = "#EDF2F7"
        active_fg = TEXT

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=active_fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=16,
        pady=10,
        width=width,
    )

    if not primary:
        button.configure(
            highlightthickness=1,
            highlightbackground=BORDER
        )

    return button


def set_task(task):
    current_task.set(task)

    for key, button in nav_buttons.items():
        selected = key == task

        button.configure(
            bg=SIDEBAR_ACTIVE if selected else SIDEBAR,
            fg="#FFFFFF" if selected else "#B8C3D4",
        )

    task1_page.pack_forget()
    task2_page.pack_forget()

    if task == "task1":
        task1_page.pack(fill="both", expand=True)

        page_title.configure(text="Task 1")
        page_subtitle.configure(
            text="Load, explore, and transform discrete-time signals."
        )

    else:
        task2_page.pack(fill="both", expand=True)

        page_title.configure(text="Task 2")
        page_subtitle.configure(
            text="Generate sine and cosine signals from configurable parameters."
        )


for key, label in (
    ("task1", "〰   Task 1"),
    ("task2", "∿   Task 2")
):
    btn = tk.Button(
        sidebar,
        text=label,
        anchor="w",
        command=lambda k=key: set_task(k),
        bg=SIDEBAR_ACTIVE if key == "task1" else SIDEBAR,
        fg="#FFFFFF" if key == "task1" else "#B8C3D4",
        activebackground=SIDEBAR_ACTIVE,
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=14,
    )

    btn.pack(fill="x", padx=12, pady=3)
    nav_buttons[key] = btn


# ---------------------------------------------------------
# SIDEBAR FOOTER
# ---------------------------------------------------------
sidebar_footer = tk.Frame(sidebar, bg=SIDEBAR)
sidebar_footer.pack(side="bottom", fill="x", padx=22, pady=22)

tk.Frame(
    sidebar_footer,
    bg="#354158",
    height=1
).pack(fill="x", pady=(0, 14))

tk.Label(
    sidebar_footer,
    text="DIGITAL SIGNAL PROCESSING",
    bg=SIDEBAR,
    fg="#8996AC",
    font=("Segoe UI", 8, "bold")
).pack(anchor="w")

tk.Label(
    sidebar_footer,
    text="Coursework workspace",
    bg=SIDEBAR,
    fg="#B8C3D4",
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(5, 0))


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
header = tk.Frame(main, bg=BG)
header.pack(fill="x", padx=32, pady=(26, 20))

heading_area = tk.Frame(header, bg=BG)
heading_area.pack(side="left", fill="x", expand=True)

page_title = tk.Label(
    heading_area,
    text="Task 1",
    font=("Segoe UI", 24, "bold"),
    bg=BG,
    fg=TEXT
)
page_title.pack(anchor="w")

page_subtitle = tk.Label(
    heading_area,
    text="Load, explore, and transform discrete-time signals.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
)
page_subtitle.pack(anchor="w", pady=(5, 0))

tk.Label(
    header,
    text="●  READY",
    font=("Segoe UI", 9, "bold"),
    bg="#E5F6F0",
    fg=SUCCESS,
    padx=12,
    pady=8
).pack(side="right", anchor="n", pady=4)


# ---------------------------------------------------------
# CONTENT PAGES
# ---------------------------------------------------------
pages = tk.Frame(main, bg=BG)
pages.pack(fill="both", expand=True, padx=32, pady=(0, 28))

task1_page = tk.Frame(pages, bg=BG)
task2_page = tk.Frame(pages, bg=BG)


# ---------------------------------------------------------
# TASK 1 SCROLLABLE PAGE
# ---------------------------------------------------------
task1_canvas = tk.Canvas(
    task1_page,
    bg=BG,
    highlightthickness=0,
    bd=0
)

task1_scrollbar = ttk.Scrollbar(
    task1_page,
    orient="vertical",
    command=task1_canvas.yview
)

task1_canvas.configure(
    yscrollcommand=task1_scrollbar.set
)

task1_scrollbar.pack(side="right", fill="y")
task1_canvas.pack(side="left", fill="both", expand=True)

task1_content = tk.Frame(task1_canvas, bg=BG)

task1_window = task1_canvas.create_window(
    (0, 0),
    window=task1_content,
    anchor="nw"
)


def update_task1_scroll_region(_event=None):
    task1_canvas.configure(
        scrollregion=task1_canvas.bbox("all")
    )


def resize_task1_content(event):
    task1_canvas.itemconfigure(
        task1_window,
        width=event.width
    )


task1_content.bind(
    "<Configure>",
    update_task1_scroll_region
)

task1_canvas.bind(
    "<Configure>",
    resize_task1_content
)


def scroll_task1(event):
    if current_task.get() != "task1":
        return

    if getattr(event, "delta", 0):
        task1_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    elif getattr(event, "num", None) == 4:
        task1_canvas.yview_scroll(-1, "units")

    elif getattr(event, "num", None) == 5:
        task1_canvas.yview_scroll(1, "units")


task1_canvas.bind_all("<MouseWheel>", scroll_task1)
task1_canvas.bind_all("<Button-4>", scroll_task1)
task1_canvas.bind_all("<Button-5>", scroll_task1)


# ---------------------------------------------------------
# REUSABLE CARD AND FIELD FUNCTIONS
# ---------------------------------------------------------
def make_card(parent, title, subtitle=None):
    card = tk.Frame(
        parent,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    card.pack(fill="x", pady=(0, 16))

    top = tk.Frame(card, bg=CARD)
    top.pack(fill="x", padx=20, pady=(17, 12))

    tk.Label(
        top,
        text=title,
        font=("Segoe UI", 12, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(anchor="w")

    if subtitle:
        tk.Label(
            top,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(4, 0))

    body = tk.Frame(card, bg=CARD)
    body.pack(fill="x", padx=20, pady=(0, 18))

    return card, body


def field(parent, label, default="", width=18):
    wrapper = tk.Frame(parent, bg=CARD)

    tk.Label(
        wrapper,
        text=label,
        font=("Segoe UI", 9, "bold"),
        bg=CARD,
        fg=MUTED
    ).pack(anchor="w", pady=(0, 6))

    entry = ttk.Entry(
        wrapper,
        style="Modern.TEntry",
        width=width
    )

    if default != "":
        entry.insert(0, str(default))

    entry.pack(fill="x")

    return wrapper, entry


# ---------------------------------------------------------
# SIGNAL DISPLAY
# ---------------------------------------------------------
def display_signals(selected_signals, mode="Discrete"):
    if not selected_signals:
        messagebox.showwarning(
            "Warning",
            "Please select at least one signal."
        )
        return

    fig, ax = plt.subplots(figsize=(9, 5))

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FBFCFE")

    for signal in selected_signals:
        indices = signal["indices"]
        samples = signal["samples"]
        name = signal["name"]

        if mode == "Continuous":
            ax.plot(
                indices,
                samples,
                marker="o",
                linewidth=2,
                label=name
            )
        else:
            ax.stem(
                indices,
                samples,
                label=name
            )

    ax.set_xlabel("Index n")
    ax.set_ylabel("Amplitude")
    ax.set_title("Signal Display")
    ax.grid(True, alpha=0.25)
    ax.axhline(0, color="#64748B", linewidth=0.8)
    ax.legend()

    fig.tight_layout()
    plt.show()


# ---------------------------------------------------------
# SAVE SIGNAL RESULT
# ---------------------------------------------------------
def save_result(indices, samples, name):
    result = {
        "name": name,
        "indices": indices,
        "samples": samples
    }

    signals.append(result)
    signal_list.insert(tk.END, name)

    signal_count.configure(
        text=f"{len(signals)} signal{'s' if len(signals) != 1 else ''}"
    )

    return result


# ---------------------------------------------------------
# LOAD SIGNAL FROM FILE
# ---------------------------------------------------------
def load_signal():
    file_name = filedialog.askopenfilename(
        title="Select Signal File",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
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


# ---------------------------------------------------------
# SELECT SIGNALS
# ---------------------------------------------------------
def get_selected_signals():
    selected = signal_list.curselection()

    return [
        signals[position]
        for position in selected
    ]


# ---------------------------------------------------------
# DISPLAY ONE SELECTED SIGNAL
# ---------------------------------------------------------
def display_selected_signal():
    selected = get_selected_signals()

    if len(selected) == 0:
        messagebox.showwarning(
            "No Signal Selected",
            "Please select a signal from the Signal Library first."
        )
        return

    if len(selected) > 1:
        messagebox.showwarning(
            "Multiple Signals Selected",
            "Please select exactly one signal to display."
        )
        return

    display_signals(
        selected,
        mode=task1_display_mode.get()
    )


# ---------------------------------------------------------
# ADD SIGNALS
# ---------------------------------------------------------
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

    display_signals(
        [result],
        mode=task1_display_mode.get()
    )


# ---------------------------------------------------------
# SUBTRACT SIGNALS
# ---------------------------------------------------------
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

    display_signals(
        [result],
        mode=task1_display_mode.get()
    )


# ---------------------------------------------------------
# MULTIPLY SIGNAL
# ---------------------------------------------------------
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

    display_signals(
        [result],
        mode=task1_display_mode.get()
    )


# ---------------------------------------------------------
# SHIFT SIGNAL
# ---------------------------------------------------------
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

    display_signals(
        [result],
        mode=task1_display_mode.get()
    )


# ---------------------------------------------------------
# FOLD SIGNAL
# ---------------------------------------------------------
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

    display_signals(
        [result],
        mode=task1_display_mode.get()
    )


# ---------------------------------------------------------
# GENERATE SINE / COSINE SIGNAL - TASK 2
# ---------------------------------------------------------
def generate_selected_signal(signal_type):
    try:
        amplitude = float(amplitude_entry.get())
        phase = float(phase_entry.get())
        frequency = float(frequency_entry.get())
        sampling_frequency = float(
            sampling_frequency_entry.get()
        )
        duration = float(duration_entry.get())

        indices, samples, time = generate_signal(
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

        save_result(indices, samples, name)

        fig, ax = plt.subplots(figsize=(9, 5))

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FBFCFE")

        if display_mode.get() == "Continuous":
            ax.plot(
                time,
                samples,
                marker="o",
                linewidth=2,
                label=name
            )
        else:
            ax.stem(
                time,
                samples,
                label=name
            )

        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Amplitude")
        ax.set_title(name + " - Signal Display")
        ax.grid(True, alpha=0.25)
        ax.axhline(0, color="#64748B", linewidth=0.8)
        ax.legend()

        fig.tight_layout()
        plt.show()

    except ValueError as error:
        messagebox.showerror(
            "Invalid Input",
            str(error)
        )


# =========================================================
# TASK 1 PAGE
# =========================================================

# ---------------------------------------------------------
# TASK 1: SIGNAL REPRESENTATION
# ---------------------------------------------------------
_, task1_representation_body = make_card(
    task1_content,
    "Signal representation",
    "Choose how Task 1 signals and operation results are plotted."
)

task1_representation_row = tk.Frame(
    task1_representation_body,
    bg=CARD
)

task1_representation_row.pack(fill="x")

tk.Label(
    task1_representation_row,
    text="Plot style",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=MUTED
).pack(side="left", padx=(0, 12))

task1_display_mode = tk.StringVar(value="Discrete")

task1_mode_menu = ttk.Combobox(
    task1_representation_row,
    textvariable=task1_display_mode,
    values=("Discrete", "Continuous"),
    state="readonly",
    width=18,
    style="Modern.TCombobox"
)

task1_mode_menu.pack(side="left")


# ---------------------------------------------------------
# TASK 1: SIGNAL LIBRARY
# ---------------------------------------------------------
_, load_body = make_card(
    task1_content,
    "Signal library",
    "Import a signal, select exactly one signal, then display it."
)

# Load and count row
load_row = tk.Frame(load_body, bg=CARD)
load_row.pack(fill="x")

make_button(
    load_row,
    "＋  Load signal from file",
    load_signal,
    primary=True
).pack(side="left")

signal_count = tk.Label(
    load_row,
    text="0 signals",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=MUTED
)

signal_count.pack(side="right", padx=5)


# Signal list
list_frame = tk.Frame(
    load_body,
    bg="#F8FAFD",
    highlightthickness=1,
    highlightbackground=BORDER
)

list_frame.pack(fill="x", pady=(14, 12))

signal_scroll = ttk.Scrollbar(
    list_frame,
    orient="vertical"
)

signal_list = tk.Listbox(
    list_frame,
    selectmode=tk.MULTIPLE,
    exportselection=False,
    height=5,
    font=("Segoe UI", 10),
    bg="#F8FAFD",
    fg=TEXT,
    selectbackground="#DCE7FF",
    selectforeground=TEXT,
    relief="flat",
    bd=0,
    highlightthickness=0,
    yscrollcommand=signal_scroll.set
)

signal_scroll.configure(
    command=signal_list.yview
)

signal_scroll.pack(side="right", fill="y")

signal_list.pack(
    side="left",
    fill="both",
    expand=True,
    padx=8,
    pady=8
)


# Display button in Signal Library
make_button(
    load_body,
    "▤  Display Signal",
    display_selected_signal,
    primary=True
).pack(anchor="w")


# ---------------------------------------------------------
# TASK 1: SIGNAL OPERATIONS
# ---------------------------------------------------------
_, operations_body = make_card(
    task1_content,
    "Signal operations",
    "Select the required signal(s) in the library above."
)

ops_grid = tk.Frame(operations_body, bg=CARD)
ops_grid.pack(fill="x")

for col in range(3):
    ops_grid.grid_columnconfigure(
        col,
        weight=1,
        uniform="ops"
    )


make_button(
    ops_grid,
    "Add selected signals",
    add_selected_signals,
    primary=False
).grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(0, 8),
    pady=5
)

make_button(
    ops_grid,
    "Subtract two signals",
    subtract_selected_signals,
    primary=False
).grid(
    row=0,
    column=1,
    sticky="ew",
    padx=4,
    pady=5
)

make_button(
    ops_grid,
    "Fold / reverse",
    fold_selected_signal,
    primary=False
).grid(
    row=0,
    column=2,
    sticky="ew",
    padx=(8, 0),
    pady=5
)


constant_wrap, constant_entry = field(
    ops_grid,
    "Multiplication constant",
    "2"
)

constant_wrap.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(0, 8),
    pady=(12, 5)
)


shift_wrap, shift_entry = field(
    ops_grid,
    "Shift k (+ advance, − delay)",
    "1"
)

shift_wrap.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=4,
    pady=(12, 5)
)


action_wrap = tk.Frame(ops_grid, bg=CARD)

action_wrap.grid(
    row=1,
    column=2,
    sticky="ew",
    padx=(8, 0),
    pady=(12, 5)
)

tk.Label(
    action_wrap,
    text="Apply operation",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=MUTED
).pack(anchor="w", pady=(0, 6))

action_buttons = tk.Frame(action_wrap, bg=CARD)
action_buttons.pack(fill="x")

make_button(
    action_buttons,
    "Multiply",
    multiply_selected_signal,
    primary=True
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 4)
)

make_button(
    action_buttons,
    "Shift",
    shift_selected_signal,
    primary=True
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=(4, 0)
)


# =========================================================
# TASK 2 PAGE
# =========================================================

# ---------------------------------------------------------
# TASK 2: SIGNAL REPRESENTATION
# ---------------------------------------------------------
_, representation_body = make_card(
    task2_page,
    "Signal representation",
    "Choose how generated signals are plotted."
)

representation_row = tk.Frame(
    representation_body,
    bg=CARD
)

representation_row.pack(fill="x")

tk.Label(
    representation_row,
    text="Plot style",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=MUTED
).pack(side="left", padx=(0, 12))

display_mode = tk.StringVar(value="Discrete")

mode_menu = ttk.Combobox(
    representation_row,
    textvariable=display_mode,
    values=("Discrete", "Continuous"),
    state="readonly",
    width=18,
    style="Modern.TCombobox"
)

mode_menu.pack(side="left")


# ---------------------------------------------------------
# TASK 2: SIGNAL GENERATOR
# ---------------------------------------------------------
_, gen_body = make_card(
    task2_page,
    "Signal generator",
    "Set the signal parameters, then generate a sine or cosine waveform."
)

fields_grid = tk.Frame(gen_body, bg=CARD)
fields_grid.pack(fill="x")

for col in range(3):
    fields_grid.grid_columnconfigure(
        col,
        weight=1,
        uniform="params"
    )


amp_wrap, amplitude_entry = field(
    fields_grid,
    "Amplitude A",
    "1"
)

phase_wrap, phase_entry = field(
    fields_grid,
    "Phase shift θ (degrees)",
    "0"
)

freq_wrap, frequency_entry = field(
    fields_grid,
    "Analog frequency f (Hz)",
    "5"
)

fs_wrap, sampling_frequency_entry = field(
    fields_grid,
    "Sampling frequency fs (Hz)",
    "50"
)

duration_wrap, duration_entry = field(
    fields_grid,
    "Duration (seconds)",
    "1"
)


amp_wrap.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(0, 12),
    pady=(0, 15)
)

phase_wrap.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=6,
    pady=(0, 15)
)

freq_wrap.grid(
    row=0,
    column=2,
    sticky="ew",
    padx=(12, 0),
    pady=(0, 15)
)

fs_wrap.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(0, 12),
    pady=(0, 15)
)

duration_wrap.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=6,
    pady=(0, 15)
)


# ---------------------------------------------------------
# TASK 2: GENERATION BUTTONS
# ---------------------------------------------------------
button_row = tk.Frame(gen_body, bg=CARD)
button_row.pack(fill="x", pady=(5, 0))

make_button(
    button_row,
    "Generate sine wave",
    lambda: generate_selected_signal("sine"),
    primary=True
).pack(side="left", padx=(0, 10))

make_button(
    button_row,
    "Generate cosine wave",
    lambda: generate_selected_signal("cosine"),
    primary=False
).pack(side="left")


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------
set_task("task1")

root.mainloop()