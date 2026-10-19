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
        raise ValueError("Number of levels must be an integer >= 2.")

    indices = signal["indices"]
    samples = signal["samples"]

    if not samples:
        raise ValueError("Cannot quantize an empty signal.")

    minimum = min(samples)
    maximum = max(samples)

    if minimum == maximum:
        bits = math.ceil(math.log2(levels))

        return {
            "indices": indices.copy(),
            "quantized_samples": samples.copy(),
            "errors": [0.0] * len(samples),
            "encoded_signal": [
                format(0, f"0{bits}b")
                for _ in samples
            ],
            "intervals": [0] * len(samples),
            "step_size": 0.0,
        }

    step_size = (maximum - minimum) / levels
    bits = math.ceil(math.log2(levels))

    quantized_samples = []
    errors = []
    encoded_signal = []
    interval_indices = []

    for sample in samples:
        interval = int((sample - minimum) / step_size)

        # Include the maximum sample in the last interval.
        interval = min(interval, levels - 1)

        lower_bound = minimum + interval * step_size
        quantized_value = lower_bound + step_size / 2

        error = quantized_value - sample
        binary_code = format(interval, f"0{bits}b")

        interval_indices.append(interval)
        quantized_samples.append(quantized_value)
        errors.append(error)
        encoded_signal.append(binary_code)

    return {
        "indices": indices.copy(),
        "quantized_samples": quantized_samples,
        "errors": errors,
        "encoded_signal": encoded_signal,
        "intervals": interval_indices,
        "step_size": step_size,
    }