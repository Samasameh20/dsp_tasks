import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt

from style import COLORS, configure_styles
from tasks.task1_operations import (
    add_signal_results, display_signals, fold_signal_result,
    load_signal_from_file, multiply_signal_result, save_signal_result,
    shift_signal_result, subtract_signal_results,
)
from tasks.task2_operations import generate_signal_result

signals = []
BG, CARD = COLORS["BG"], COLORS["CARD"]
SIDEBAR, SIDEBAR_ACTIVE = COLORS["SIDEBAR"], COLORS["SIDEBAR_ACTIVE"]
TEXT, MUTED, ACCENT = COLORS["TEXT"], COLORS["MUTED"], COLORS["ACCENT"]
BORDER, SUCCESS = COLORS["BORDER"], COLORS["SUCCESS"]

root = tk.Tk()
root.title("DSP Tasks")
root.geometry("1180x780")
root.minsize(980, 680)
root.configure(bg=BG)
configure_styles(root)

sidebar = tk.Frame(root, bg=SIDEBAR, width=235)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

brand = tk.Frame(sidebar, bg=SIDEBAR)
brand.pack(fill="x", padx=22, pady=(28, 34))
tk.Label(brand, text="∿", font=("Segoe UI Symbol", 27, "bold"),
         bg=ACCENT, fg="white", width=2, height=1).pack(side="left", padx=(0, 11))
brand_text = tk.Frame(brand, bg=SIDEBAR)
brand_text.pack(side="left")
tk.Label(brand_text, text="DSP LAB", font=("Segoe UI", 11, "bold"),
         bg=SIDEBAR, fg="#FFFFFF").pack(anchor="w")
tk.Label(brand_text, text="Signal workspace", font=("Segoe UI", 9),
         bg=SIDEBAR, fg="#AAB5C7").pack(anchor="w", pady=(3, 0))
tk.Label(sidebar, text="WORKSPACE", font=("Segoe UI", 8, "bold"),
         bg=SIDEBAR, fg="#8996AC").pack(anchor="w", padx=24, pady=(0, 12))

def make_button(parent, text, command, primary=True, width=None):
    # Button colors are read from the shared style palette.
    if primary:
        bg, fg, active_bg, active_fg = ACCENT, "#FFFFFF", "#3E68D6", "#FFFFFF"
    else:
        bg, fg, active_bg, active_fg = CARD, TEXT, "#EDF2F7", TEXT
    button = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
        activebackground=active_bg, activeforeground=active_fg, relief="flat",
        bd=0, cursor="hand2", font=("Segoe UI", 10, "bold"),
        padx=16, pady=10, width=width)
    if not primary:
        button.configure(highlightthickness=1, highlightbackground=BORDER)
    return button

nav_buttons = {}
current_task = tk.StringVar(value="task1")
header = tk.Frame(main, bg=BG)
header.pack(fill="x", padx=32, pady=(26, 20))
heading_area = tk.Frame(header, bg=BG)
heading_area.pack(side="left", fill="x", expand=True)
page_title = tk.Label(heading_area, text="Task 1", font=("Segoe UI", 24, "bold"),
                      bg=BG, fg=TEXT)
page_title.pack(anchor="w")
page_subtitle = tk.Label(heading_area,
    text="Load, explore, and transform discrete-time signals.",
    font=("Segoe UI", 10), bg=BG, fg=MUTED)
page_subtitle.pack(anchor="w", pady=(5, 0))
tk.Label(header, text="●  READY", font=("Segoe UI", 9, "bold"),
         bg="#E5F6F0", fg=SUCCESS, padx=12, pady=8).pack(side="right", anchor="n", pady=4)

pages = tk.Frame(main, bg=BG)
pages.pack(fill="both", expand=True, padx=32, pady=(0, 28))
task1_page = tk.Frame(pages, bg=BG)
task2_page = tk.Frame(pages, bg=BG)

def set_task(task):
    current_task.set(task)
    for key, button in nav_buttons.items():
        button.configure(bg=SIDEBAR_ACTIVE if key == task else SIDEBAR,
                         fg="#FFFFFF" if key == task else "#B8C3D4")
    task1_page.pack_forget()
    task2_page.pack_forget()
    if task == "task1":
        task1_page.pack(fill="both", expand=True)
        page_title.configure(text="Task 1")
        page_subtitle.configure(text="Load, explore, and transform discrete-time signals.")
    else:
        task2_page.pack(fill="both", expand=True)
        page_title.configure(text="Task 2")
        page_subtitle.configure(text="Generate sine and cosine signals from configurable parameters.")

for key, label in (("task1", "〰   Task 1"), ("task2", "∿   Task 2")):
    btn = tk.Button(sidebar, text=label, anchor="w",
        command=lambda k=key: set_task(k),
        bg=SIDEBAR_ACTIVE if key == "task1" else SIDEBAR,
        fg="#FFFFFF" if key == "task1" else "#B8C3D4",
        activebackground=SIDEBAR_ACTIVE, activeforeground="#FFFFFF",
        relief="flat", bd=0, cursor="hand2",
        font=("Segoe UI", 10, "bold"), padx=20, pady=14)
    btn.pack(fill="x", padx=12, pady=3)
    nav_buttons[key] = btn

footer = tk.Frame(sidebar, bg=SIDEBAR)
footer.pack(side="bottom", fill="x", padx=22, pady=22)
tk.Frame(footer, bg="#354158", height=1).pack(fill="x", pady=(0, 14))
tk.Label(footer, text="DIGITAL SIGNAL PROCESSING", bg=SIDEBAR,
         fg="#8996AC", font=("Segoe UI", 8, "bold")).pack(anchor="w")
tk.Label(footer, text="Coursework workspace", bg=SIDEBAR,
         fg="#B8C3D4", font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))

def make_card(parent, title, subtitle=None):
    card = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="x", pady=(0, 16))
    top = tk.Frame(card, bg=CARD)
    top.pack(fill="x", padx=20, pady=(17, 12))
    tk.Label(top, text=title, font=("Segoe UI", 12, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w")
    if subtitle:
        tk.Label(top, text=subtitle, font=("Segoe UI", 9),
                 bg=CARD, fg=MUTED).pack(anchor="w", pady=(4, 0))
    body = tk.Frame(card, bg=CARD)
    body.pack(fill="x", padx=20, pady=(0, 18))
    return card, body

def field(parent, label, default="", width=18):
    wrapper = tk.Frame(parent, bg=CARD)
    tk.Label(wrapper, text=label, font=("Segoe UI", 9, "bold"),
             bg=CARD, fg=MUTED).pack(anchor="w", pady=(0, 6))
    entry = ttk.Entry(wrapper, style="Modern.TEntry", width=width)
    if default != "":
        entry.insert(0, str(default))
    entry.pack(fill="x")
    return wrapper, entry

# Task 1 scrollable page
task1_canvas = tk.Canvas(task1_page, bg=BG, highlightthickness=0, bd=0)
task1_scrollbar = ttk.Scrollbar(task1_page, orient="vertical", command=task1_canvas.yview)
task1_canvas.configure(yscrollcommand=task1_scrollbar.set)
task1_scrollbar.pack(side="right", fill="y")
task1_canvas.pack(side="left", fill="both", expand=True)
task1_content = tk.Frame(task1_canvas, bg=BG)
task1_window = task1_canvas.create_window((0, 0), window=task1_content, anchor="nw")

def update_task1_scroll_region(_event=None):
    task1_canvas.configure(scrollregion=task1_canvas.bbox("all"))
def resize_task1_content(event):
    task1_canvas.itemconfigure(task1_window, width=event.width)
def scroll_task1(event):
    if current_task.get() != "task1":
        return
    if getattr(event, "delta", 0):
        task1_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif getattr(event, "num", None) == 4:
        task1_canvas.yview_scroll(-1, "units")
    elif getattr(event, "num", None) == 5:
        task1_canvas.yview_scroll(1, "units")
task1_content.bind("<Configure>", update_task1_scroll_region)
task1_canvas.bind("<Configure>", resize_task1_content)
task1_canvas.bind_all("<MouseWheel>", scroll_task1)
task1_canvas.bind_all("<Button-4>", scroll_task1)
task1_canvas.bind_all("<Button-5>", scroll_task1)

_, rep1 = make_card(task1_content, "Signal representation",
                    "Choose how Task 1 signals and operation results are plotted.")
row = tk.Frame(rep1, bg=CARD)
row.pack(fill="x")
tk.Label(row, text="Plot style", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=MUTED).pack(side="left", padx=(0, 12))
task1_display_mode = tk.StringVar(value="Discrete")
ttk.Combobox(row, textvariable=task1_display_mode, values=("Discrete", "Continuous"),
             state="readonly", width=18, style="Modern.TCombobox").pack(side="left")

_, load_body = make_card(task1_content, "Signal library",
                         "Import signals, select one or more, then display or process them.")
load_row = tk.Frame(load_body, bg=CARD)
load_row.pack(fill="x")
signal_count = tk.Label(load_row, text="0 signals", font=("Segoe UI", 9, "bold"),
                        bg=CARD, fg=MUTED)
signal_count.pack(side="right", padx=5)
signal_list = tk.Listbox(load_body, selectmode=tk.MULTIPLE, exportselection=False,
    height=5, font=("Segoe UI", 10), bg="#F8FAFD", fg=TEXT,
    selectbackground="#DCE7FF", selectforeground=TEXT, relief="flat", bd=0,
    highlightthickness=1, highlightbackground=BORDER)
signal_list.pack(fill="x", pady=(14, 12))

def save_result(indices, samples, name):
    return save_signal_result(signals, signal_list, signal_count, indices, samples, name)

def load_signal():
    file_name = filedialog.askopenfilename(title="Select Signal File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not file_name:
        return
    try:
        result = load_signal_from_file(file_name)
        if not result["indices"]:
            messagebox.showerror("Error", "No valid signal samples were found.")
            return
        save_result(result["indices"], result["samples"], os.path.basename(file_name))
        messagebox.showinfo("Success", "Signal loaded successfully!")
    except Exception as error:
        messagebox.showerror("Error", "Could not read the signal:\n" + str(error))

def get_selected_signals():
    return [signals[position] for position in signal_list.curselection()]

def display_selected_signal():
    selected = get_selected_signals()
    if not selected:
        messagebox.showwarning("No Signal Selected",
                               "Please select at least one signal from the Signal Library.")
        return
    try:
        display_signals(selected, mode=task1_display_mode.get())
    except Exception as error:
        messagebox.showerror("Display Error", str(error))

def add_selected_signals():
    selected = get_selected_signals()
    if len(selected) < 2:
        messagebox.showwarning("Warning", "Select at least two signals.")
        return
    try:
        indices, samples = add_signal_results(selected)
        result = save_result(indices, samples, "Addition Result")
        display_signals([result], mode=task1_display_mode.get())
    except Exception as error:
        messagebox.showerror("Operation Error", str(error))

def subtract_selected_signals():
    selected = get_selected_signals()
    if len(selected) != 2:
        messagebox.showwarning("Warning", "Select exactly two signals.")
        return
    try:
        indices, samples = subtract_signal_results(selected[0], selected[1])
        result = save_result(indices, samples, "Subtraction Result")
        display_signals([result], mode=task1_display_mode.get())
    except Exception as error:
        messagebox.showerror("Operation Error", str(error))

def multiply_selected_signal():
    selected = get_selected_signals()
    if len(selected) != 1:
        messagebox.showwarning("Warning", "Select exactly one signal.")
        return
    try:
        indices, samples = multiply_signal_result(selected[0], float(constant_entry.get()))
        result = save_result(indices, samples, "Multiplication Result")
        display_signals([result], mode=task1_display_mode.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid multiplication constant.")
    except Exception as error:
        messagebox.showerror("Operation Error", str(error))

def shift_selected_signal():
    selected = get_selected_signals()
    if len(selected) != 1:
        messagebox.showwarning("Warning", "Select exactly one signal.")
        return
    try:
        indices, samples = shift_signal_result(selected[0], int(shift_entry.get()))
        result = save_result(indices, samples, "Shift Result")
        display_signals([result], mode=task1_display_mode.get())
    except ValueError:
        messagebox.showerror("Error", "Enter an integer for k.")
    except Exception as error:
        messagebox.showerror("Operation Error", str(error))

def fold_selected_signal():
    selected = get_selected_signals()
    if len(selected) != 1:
        messagebox.showwarning("Warning", "Select exactly one signal.")
        return
    try:
        indices, samples = fold_signal_result(selected[0])
        result = save_result(indices, samples, "Folded Signal")
        display_signals([result], mode=task1_display_mode.get())
    except Exception as error:
        messagebox.showerror("Operation Error", str(error))

make_button(load_row, "＋  Load signal from file", load_signal).pack(side="left")
make_button(load_body, "▤  Display Signal", display_selected_signal).pack(anchor="w")

_, ops_body = make_card(task1_content, "Signal operations",
                        "Select the required signal(s) in the library above.")
ops_grid = tk.Frame(ops_body, bg=CARD)
ops_grid.pack(fill="x")
for col in range(3):
    ops_grid.grid_columnconfigure(col, weight=1, uniform="ops")
make_button(ops_grid, "Add selected signals", add_selected_signals, False).grid(
    row=0, column=0, sticky="ew", padx=(0, 8), pady=5)
make_button(ops_grid, "Subtract two signals", subtract_selected_signals, False).grid(
    row=0, column=1, sticky="ew", padx=4, pady=5)
make_button(ops_grid, "Fold / reverse", fold_selected_signal, False).grid(
    row=0, column=2, sticky="ew", padx=(8, 0), pady=5)
constant_wrap, constant_entry = field(ops_grid, "Multiplication constant", "2")
constant_wrap.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(12, 5))
shift_wrap, shift_entry = field(ops_grid, "Shift k (+ advance, − delay)", "1")
shift_wrap.grid(row=1, column=1, sticky="ew", padx=4, pady=(12, 5))
action_wrap = tk.Frame(ops_grid, bg=CARD)
action_wrap.grid(row=1, column=2, sticky="ew", padx=(8, 0), pady=(12, 5))
tk.Label(action_wrap, text="Apply operation", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=MUTED).pack(anchor="w", pady=(0, 6))
action_buttons = tk.Frame(action_wrap, bg=CARD)
action_buttons.pack(fill="x")
make_button(action_buttons, "Multiply", multiply_selected_signal).pack(
    side="left", fill="x", expand=True, padx=(0, 4))
make_button(action_buttons, "Shift", shift_selected_signal).pack(
    side="left", fill="x", expand=True, padx=(4, 0))

# Task 2 page
_, rep2 = make_card(task2_page, "Signal representation",
                    "Choose how generated signals are plotted.")
row2 = tk.Frame(rep2, bg=CARD)
row2.pack(fill="x")
tk.Label(row2, text="Plot style", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=MUTED).pack(side="left", padx=(0, 12))
display_mode = tk.StringVar(value="Discrete")
ttk.Combobox(row2, textvariable=display_mode, values=("Discrete", "Continuous"),
             state="readonly", width=18, style="Modern.TCombobox").pack(side="left")

_, gen_body = make_card(task2_page, "Signal generator",
                        "Set the signal parameters, then generate a sine or cosine waveform.")
fields_grid = tk.Frame(gen_body, bg=CARD)
fields_grid.pack(fill="x")
for col in range(3):
    fields_grid.grid_columnconfigure(col, weight=1, uniform="params")
amp_wrap, amplitude_entry = field(fields_grid, "Amplitude A", "1")
phase_wrap, phase_entry = field(fields_grid, "Phase shift θ (degrees)", "0")
freq_wrap, frequency_entry = field(fields_grid, "Analog frequency f (Hz)", "5")
fs_wrap, sampling_frequency_entry = field(fields_grid, "Sampling frequency fs (Hz)", "50")
duration_wrap, duration_entry = field(fields_grid, "Duration (seconds)", "1")
amp_wrap.grid(row=0, column=0, sticky="ew", padx=(0, 12), pady=(0, 15))
phase_wrap.grid(row=0, column=1, sticky="ew", padx=6, pady=(0, 15))
freq_wrap.grid(row=0, column=2, sticky="ew", padx=(12, 0), pady=(0, 15))
fs_wrap.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 15))
duration_wrap.grid(row=1, column=1, sticky="ew", padx=6, pady=(0, 15))

def generate_selected_signal(signal_type):
    try:
        result = generate_signal_result(signal_type, amplitude_entry.get(),
            phase_entry.get(), frequency_entry.get(), sampling_frequency_entry.get(),
            duration_entry.get(), display_mode.get())
        save_result(result["indices"], result["samples"], result["name"])
        result["figure"].tight_layout()
        plt.show()
    except ValueError as error:
        messagebox.showerror("Invalid Input", str(error))
    except Exception as error:
        messagebox.showerror("Generation Error", str(error))

button_row = tk.Frame(gen_body, bg=CARD)
button_row.pack(fill="x", pady=(5, 0))
make_button(button_row, "Generate sine wave",
            lambda: generate_selected_signal("sine")).pack(side="left", padx=(0, 10))
make_button(button_row, "Generate cosine wave",
            lambda: generate_selected_signal("cosine"), primary=False).pack(side="left")

set_task("task1")
root.mainloop()
