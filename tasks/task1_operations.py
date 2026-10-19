"""Task 1 signal file loading, plotting, and transformations."""
import matplotlib.pyplot as plt
from signal_operations import read_signal, add_signals, subtract_signals, multiply_signal, shift_signal, fold_signal

def load_signal_from_file(file_name):
    indices, samples = read_signal(file_name)
    return {"indices": indices, "samples": samples}

def save_signal_result(signals, signal_list, signal_count, indices, samples, name):
    result = {"name": name, "indices": list(indices), "samples": list(samples)}
    signals.append(result)
    signal_list.insert("end", name)
    count = len(signals)
    signal_count.configure(text=f"{count} signal{'s' if count != 1 else ''}")
    return result

def display_signals(selected_signals, mode="Discrete"):
    if not selected_signals:
        messagebox.showwarning(
            "No signal",
            "Select at least one signal first."
        )
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    colors = plt.cm.tab10.colors

    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for i, signal in enumerate(selected_signals):
        indices = signal["indices"]
        samples = signal["samples"]
        name = signal["name"]

        color = colors[i % len(colors)]

        if mode == "Continuous":
            ax.plot(
                indices,
                samples,
                color=color,
                marker="o",
                label=name
            )
        else:
            markerline, stemlines, baseline = ax.stem(
                indices,
                samples,
                label=name
            )

            markerline.set_color(color)
            stemlines.set_color(color)
            baseline.set_color("black")

    ax.set_xlabel("Index n")
    ax.set_ylabel("Amplitude")
    ax.set_title("Signal Display")
    ax.grid(True, color="lightgray")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.legend()

    fig.tight_layout()
    plt.show()
    
def add_signal_results(selected_signals):
    return add_signals(*selected_signals)

def subtract_signal_results(first_signal, second_signal):
    return subtract_signals(first_signal, second_signal)

def multiply_signal_result(signal, constant):
    return multiply_signal(signal, constant)

def shift_signal_result(signal, k):
    return shift_signal(signal, k)

def fold_signal_result(signal):
    return fold_signal(signal)
