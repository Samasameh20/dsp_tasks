"""Task 2 signal generation and plotting."""
import matplotlib.pyplot as plt
from signal_operations import generate_signal

def generate_signal_result(signal_type, amplitude, phase, frequency,
                           sampling_frequency, duration, display_style="Discrete"):
    try:
        amplitude, phase = float(amplitude), float(phase)
        frequency = float(frequency)
        sampling_frequency, duration = float(sampling_frequency), float(duration)
    except (TypeError, ValueError):
        raise ValueError("All signal parameters must be valid numbers.")
    indices, samples, time_values = generate_signal(
        signal_type, amplitude, phase, frequency, sampling_frequency, duration
    )
    name = f"{signal_type.capitalize()} A={amplitude} f={frequency}"
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FBFCFE")
    if display_style == "Continuous":
        ax.plot(time_values, samples, marker="o", linewidth=2, label=name)
    else:
        ax.stem(time_values, samples, label=name)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.set_title(name + " - Signal Display")
    ax.grid(True, alpha=0.25)
    ax.axhline(0, color="#64748B", linewidth=0.8)
    ax.legend()
    return {"indices": indices, "samples": samples, "time": time_values,
            "name": name, "figure": fig}
