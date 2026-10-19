import math

def read_signal(file_name):

    indices = []
    samples = []

    with open(file_name, "r") as file:

        
        file.readline()
        file.readline()
        file.readline()

        
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


def add_signals(signal1, signal2):

    result = {}

    # First signal
    for index, value in zip(
            signal1["indices"],
            signal1["samples"]):

        if index in result:

            result[index] += value

        else:

            result[index] = value

    # Second signal
    for index, value in zip(
            signal2["indices"],
            signal2["samples"]):

        if index in result:

            result[index] += value

        else:

            result[index] = value

    indices = sorted(result.keys())

    samples = []

    for index in indices:

        samples.append(
            result[index]
        )

    return indices, samples


def multiply_signal(signal, constant):

    indices = signal["indices"].copy()

    samples = []

    for value in signal["samples"]:

        samples.append(
            value * constant
        )

    return indices, samples


def subtract_signals(signal1, signal2):

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

    return indices, samples


def shift_signal(signal, k):

    indices = []

    for index in signal["indices"]:

        indices.append(
            index - k
        )

    samples = signal["samples"].copy()

    return indices, samples


def fold_signal(signal):

    new_indices = []
    new_samples = []

  
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

    return new_indices, new_samples

def generate_signal(
    signal_type,
    amplitude,
    phase_degrees,
    frequency,
    sampling_frequency,
    duration,
):
    if amplitude < 0:
        raise ValueError("Amplitude must be non-negative.")

    if frequency < 0:
        raise ValueError("Frequency must be non-negative.")

    if sampling_frequency <= 0:
        raise ValueError("Sampling frequency must be positive.")

    if duration <= 0:
        raise ValueError("Duration must be positive.")

    if sampling_frequency <= 2 * frequency:
        raise ValueError(
            "Sampling frequency must be greater than "
            "twice the signal frequency."
        )

    phase_radians = math.radians(phase_degrees)

    number_of_samples = int(sampling_frequency * duration)

    indices = list(range(number_of_samples))
    time = [n / sampling_frequency for n in indices]

    samples = []

    for t in time:
        angle = 2 * math.pi * frequency * t + phase_radians

        if signal_type.lower() == "sine":
            value = amplitude * math.sin(angle)

        elif signal_type.lower() == "cosine":
            value = amplitude * math.cos(angle)

        else:
            raise ValueError(
                "Signal type must be 'sine' or 'cosine'."
            )

        samples.append(value)

    return indices, samples, time

def quantize_signal(signal, levels):
    if not isinstance(levels, int) or levels < 2:
        raise ValueError("Levels must be an integer greater than or equal to 2.")

    indices = signal["indices"]
    samples = signal["samples"]

    if not samples:
        raise ValueError("The selected signal has no samples.")

    minimum = min(samples)
    maximum = max(samples)

    bits = math.ceil(math.log2(levels))

    if minimum == maximum:
        return {
            "indices": indices.copy(),
            "intervals": [1] * len(samples),
            "interval_indices": [1] * len(samples),
            "encoded_signal": ["0" * bits] * len(samples),
            "quantized_samples": samples.copy(),
            "errors": [0.0] * len(samples),
            "step_size": 0.0,
        }

    step_size = (maximum - minimum) / levels

    interval_indices = []
    encoded_values = []
    quantized_values = []
    errors = []

    for sample in samples:
        # Zero-based index used for encoding.
        interval = int((sample - minimum) / step_size)
        interval = min(interval, levels - 1)
        interval = max(interval, 0)

        quantized_value = minimum + (interval + 0.5) * step_size

        # Test Case 2 expects a one-based interval number.
        interval_indices.append(interval + 1)

        # The binary code represents the zero-based interval.
        encoded_values.append(format(interval, f"0{bits}b"))

        quantized_values.append(quantized_value)

        # Expected convention: quantized - original.
        errors.append(quantized_value - sample)

    return {
        "indices": indices.copy(),
        "intervals": interval_indices,
        "interval_indices": interval_indices,
        "encoded_signal": encoded_values,
        "quantized_samples": quantized_values,
        "errors": errors,
        "step_size": step_size,
    }