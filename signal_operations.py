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