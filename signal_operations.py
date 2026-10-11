
import math


# =========================================================
# READ SIGNAL FROM FILE
# =========================================================

def read_signal(file_name):

    indices = []
    samples = []

    with open(file_name, "r") as file:

        # Skip the first three header lines
        file.readline()
        file.readline()
        file.readline()

        for line in file:

            parts = line.strip().split()

            if len(parts) != 2:
                continue

            try:
                index = int(parts[0])
                value = float(parts[1])
            except ValueError:
                continue

            indices.append(index)
            samples.append(value)

    return indices, samples


# =========================================================
# ADD SIGNALS
# =========================================================

def add_signals(*input_signals):

    result = {}

    for signal in input_signals:

        for index, value in zip(
            signal["indices"],
            signal["samples"]
        ):

            if index in result:
                result[index] += value
            else:
                result[index] = value

    indices = sorted(result.keys())
    samples = [result[index] for index in indices]

    return indices, samples


# =========================================================
# SUBTRACT TWO SIGNALS
# =========================================================

def subtract_signals(signal1, signal2):

    result = {}

    for index, value in zip(
        signal1["indices"],
        signal1["samples"]
    ):
        result[index] = value

    for index, value in zip(
        signal2["indices"],
        signal2["samples"]
    ):
        if index in result:
            result[index] -= value
        else:
            result[index] = -value

    indices = sorted(result.keys())
    samples = [result[index] for index in indices]

    return indices, samples


# =========================================================
# MULTIPLY SIGNAL BY A CONSTANT
# =========================================================

def multiply_signal(signal, constant):

    indices = signal["indices"].copy()

    samples = [
        value * constant
        for value in signal["samples"]
    ]

    return indices, samples


# =========================================================
# SHIFT SIGNAL
# =========================================================

def shift_signal(signal, k):

    # Positive k advances the signal.
    # Negative k delays the signal.
    indices = [
        index - k
        for index in signal["indices"]
    ]

    samples = signal["samples"].copy()

    return indices, samples


# =========================================================
# FOLD SIGNAL
# =========================================================

def fold_signal(signal):

    new_indices = []
    new_samples = []

    for i in range(
        len(signal["indices"]) - 1,
        -1,
        -1
    ):

        new_indices.append(
            -signal["indices"][i]
        )

        new_samples.append(
            signal["samples"][i]
        )

    return new_indices, new_samples


# =========================================================
# GENERATE SINE OR COSINE SIGNAL
# =========================================================

def generate_signal(
    signal_type,
    amplitude,
    phase_degrees,
    frequency,
    sampling_frequency,
    duration
):

    if amplitude < 0:
        raise ValueError("Amplitude must be non-negative.")

    if frequency <= 0:
        raise ValueError("Frequency must be greater than zero.")

    if sampling_frequency <= 0:
        raise ValueError("Sampling frequency must be greater than zero.")

    if sampling_frequency <= 2 * frequency:
        raise ValueError(
            "Sampling frequency must be greater than "
            "twice the signal frequency."
        )

    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    # Convert phase from degrees to radians
    phase = math.radians(phase_degrees)

    # Number of samples to generate
    number_of_samples = int(
        duration * sampling_frequency
    )

    indices = list(range(number_of_samples))
    samples = []

    for n in indices:

        # Time of the current sample
        t = n / sampling_frequency

        # Calculate the signal value
        angle = (
            2 * math.pi * frequency * t
            + phase
        )

        if signal_type.lower() == "sine":
            value = amplitude * math.sin(angle)

        elif signal_type.lower() == "cosine":
            value = amplitude * math.cos(angle)

        else:
            raise ValueError(
                "Signal type must be sine or cosine."
            )

        samples.append(value)

    return indices, samples
