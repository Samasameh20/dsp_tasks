
"""Task 3: Signal quantization."""

import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

from signal_operations import quantize_signal


def build_task3_page(
    parent,
    get_selected_signals,
    make_card,
    make_button,
    field,
    colors,
):
    BG = colors["BG"]
    CARD = colors["CARD"]
    TEXT = colors["TEXT"]
    MUTED = colors["MUTED"]
    BORDER = colors["BORDER"]

    # Quantization settings
    _, settings = make_card(
        parent,
        "Quantization settings",
        "Select a signal in Task 1, then choose levels or bits."
    )

    mode = tk.StringVar(value="Levels")

    tk.Label(
        settings, text="Input method",
        bg=CARD, fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).grid(row=0, column=0, sticky="w", padx=(0, 12), pady=8)

    mode_box = ttk.Combobox(
        settings,
        textvariable=mode,
        values=("Levels", "Bits"),
        state="readonly",
        width=15,
        style="Modern.TCombobox",
    )
    mode_box.grid(row=0, column=1, sticky="w", pady=8)

    value_wrap, value_entry = field(
        settings, "Number of levels", "4"
    )
    value_wrap.grid(
        row=1, column=0, columnspan=2,
        sticky="ew", pady=8
    )

    def update_label(_event=None):
        if mode.get() == "Bits":
            value_wrap.winfo_children()[0].configure(
                text="Number of bits"
            )
            value_entry.delete(0, tk.END)
            value_entry.insert(0, "2")
        else:
            value_wrap.winfo_children()[0].configure(
                text="Number of levels"
            )
            value_entry.delete(0, tk.END)
            value_entry.insert(0, "4")

    mode_box.bind("<<ComboboxSelected>>", update_label)

    result_label = tk.Label(
        settings,
        text="",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 9),
    )
    result_label.grid(
        row=2, column=0, columnspan=2,
        sticky="w", pady=(4, 8)
    )

    # Encoded signal table
    _, table_body = make_card(
        parent,
        "Encoded signal",
        "Each sample is represented by its quantization interval code."
    )

    columns = (
        "index", "original", "interval",
        "quantized", "error", "binary"
    )

    table = ttk.Treeview(
        table_body,
        columns=columns,
        show="headings",
        height=7,
    )

    headings = {
        "index": "Index n",
        "original": "Original",
        "interval": "Interval",
        "quantized": "Quantized",
        "error": "Error",
        "binary": "Binary code",
    }

    widths = {
        "index": 70,
        "original": 100,
        "interval": 90,
        "quantized": 100,
        "error": 100,
        "binary": 110,
    }

    for column in columns:
        table.heading(column, text=headings[column])
        table.column(
            column,
            width=widths[column],
            anchor="center",
        )

    table.pack(fill="x", expand=True)

    latest_result = {}

    def run_quantization():
        selected = get_selected_signals()

        if len(selected) != 1:
            messagebox.showwarning(
                "Signal selection",
                "Go to Task 1 and select exactly one signal."
            )
            return

        try:
            value = int(value_entry.get())

            if mode.get() == "Bits":
                if value < 1:
                    raise ValueError(
                        "Number of bits must be at least 1."
                    )

                levels = 2 ** value
            else:
                levels = value

            if levels < 2:
                raise ValueError(
                    "Number of levels must be at least 2."
                )

            result = quantize_signal(selected[0], levels)

            latest_result.clear()
            latest_result.update(result)

            for item in table.get_children():
                table.delete(item)

            for i, index in enumerate(result["indices"]):
                table.insert(
                    "",
                    "end",
                    values=(
                        index,
                        f'{selected[0]["samples"][i]:.4f}',
                        result["intervals"][i],
                        f'{result["quantized_samples"][i]:.4f}',
                        f'{result["errors"][i]:.4f}',
                        result["encoded_signal"][i],
                    ),
                )

            result_label.configure(
                text=(
                    f"Levels: {levels}    "
                    f"Bits per code: {len(result['encoded_signal'][0]) if result['encoded_signal'] else 0}    "
                    f"Step size: {result['step_size']:.6f}"
                )
            )

            display_results(
                selected[0],
                result,
            )

        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
        except Exception as error:
            messagebox.showerror("Quantization error", str(error))

    def display_results(signal, result):
        indices = result["indices"]

        fig, axes = plt.subplots(
            2, 1, figsize=(10, 7)
        )

        fig.suptitle(
            f"Quantization Results — {signal['name']}"
        )

        # Quantized signal
        axes[0].stem(
            indices,
            signal["samples"],
            linefmt="C0-",
            markerfmt="C0o",
            basefmt="k-",
            label="Original",
        )
        axes[0].step(
            indices,
            result["quantized_samples"],
            where="mid",
            color="C1",
            linewidth=2,
            label="Quantized",
        )
        axes[0].set_title("Original vs Quantized Signal")
        axes[0].set_xlabel("Index n")
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()

        # Quantization error
        axes[1].stem(
            indices,
            result["errors"],
            linefmt="C2-",
            markerfmt="C2o",
            basefmt="k-",
        )
        axes[1].set_title("Quantization Error")
        axes[1].set_xlabel("Index n")
        axes[1].set_ylabel("Error")
        axes[1].grid(True, alpha=0.3)

        fig.tight_layout()
        plt.show()

    make_button(
        settings,
        "Quantize selected signal",
        run_quantization,
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=8)

    return latest_result
