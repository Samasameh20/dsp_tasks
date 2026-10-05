import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from signal_operations import (
    read_signal,
    add_signals,
    subtract_signals,
    multiply_signal,
    shift_signal,
    fold_signal
)


# =========================================================
# Read Signal File
# =========================================================

def ReadSignalFile(file_name):

    expected_indices = []
    expected_samples = []

    with open(file_name, 'r') as f:

        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()

        while line:

            L = line.strip()

            if len(L.split(' ')) == 2:

                L = line.split(' ')

                V1 = int(L[0])
                V2 = float(L[1])

                expected_indices.append(V1)
                expected_samples.append(V2)

                line = f.readline()

            else:
                break

    return expected_indices, expected_samples


# =========================================================
# Addition Test
# =========================================================

def AddSignalSamplesAreEqual(
        userFirstSignal,
        userSecondSignal,
        Your_indices,
        Your_samples):

    if (
        userFirstSignal == 'Signal1.txt'
        and userSecondSignal == 'Signal2.txt'
    ):

        file_name = "add.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Addition Test case failed, "
            "your signal have different length "
            "from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Addition Test case failed, "
                "your signal have different "
                "indicies from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:

            continue

        else:

            print(
                "Addition Test case failed, "
                "your signal have different "
                "values from the expected one"
            )

            return

    print("Addition Test case passed successfully")


# =========================================================
# Subtraction Test
# =========================================================

def SubSignalSamplesAreEqual(
        userFirstSignal,
        userSecondSignal,
        Your_indices,
        Your_samples):

    if (
        userFirstSignal == 'Signal1.txt'
        and userSecondSignal == 'Signal2.txt'
    ):

        file_name = "subtract.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Subtraction Test case failed, "
            "your signal have different length "
            "from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Subtraction Test case failed, "
                "your signal have different "
                "indicies from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:

            continue

        else:

            print(
                "Subtraction Test case failed, "
                "your signal have different "
                "values from the expected one"
            )

            return

    print("Subtraction Test case passed successfully")


# =========================================================
# Multiplication Test
# =========================================================

def MultiplySignalByConst(
        User_Const,
        Your_indices,
        Your_samples):

    if User_Const == 5:

        file_name = "mul5.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Multiply by "
            + str(User_Const)
            + " Test case failed, "
            "your signal have different length "
            "from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Multiply by "
                + str(User_Const)
                + " Test case failed, "
                "your signal have different "
                "indicies from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:

            continue

        else:

            print(
                "Multiply by "
                + str(User_Const)
                + " Test case failed, "
                "your signal have different "
                "values from the expected one"
            )

            return

    print(
        "Multiply by "
        + str(User_Const)
        + " Test case passed successfully"
    )


# =========================================================
# Shift Test
# =========================================================

def ShiftSignalByConst(
        Shift_value,
        Your_indices,
        Your_samples):

    if Shift_value == 3:

        file_name = "advance3.txt"

    elif Shift_value == -3:

        file_name = "delay3.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Shift by "
            + str(Shift_value)
            + " Test case failed, "
            "your signal have different length "
            "from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Shift by "
                + str(Shift_value)
                + " Test case failed, "
                "your signal have different "
                "indicies from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:

            continue

        else:

            print(
                "Shift by "
                + str(Shift_value)
                + " Test case failed, "
                "your signal have different "
                "values from the expected one"
            )

            return

    print(
        "Shift by "
        + str(Shift_value)
        + " Test case passed successfully"
    )


# =========================================================
# Folding Test
# =========================================================

def Folding(
        Your_indices,
        Your_samples):

    file_name = "folding.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Folding Test case failed, "
            "your signal have different length "
            "from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Folding Test case failed, "
                "your signal have different "
                "indicies from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:

            continue

        else:

            print(
                "Folding Test case failed, "
                "your signal have different "
                "values from the expected one"
            )

            return

    print("Folding Test case passed successfully")


# =========================================================
# LOAD SIGNALS
# =========================================================

indices1, samples1 = read_signal("Signal1.txt")

signal1 = {
    "indices": indices1,
    "samples": samples1
}


indices2, samples2 = read_signal("Signal2.txt")

signal2 = {
    "indices": indices2,
    "samples": samples2
}


# =========================================================
# RUN TESTS
# =========================================================

print("\n========== SIGNAL PROCESSING TESTS ==========\n")


# -------------------------
# Addition
# -------------------------

indices, samples = add_signals(
    signal1,
    signal2
)

AddSignalSamplesAreEqual(
    "Signal1.txt",
    "Signal2.txt",
    indices,
    samples
)


# -------------------------
# Subtraction
# -------------------------

indices, samples = subtract_signals(
    signal1,
    signal2
)

SubSignalSamplesAreEqual(
    "Signal1.txt",
    "Signal2.txt",
    indices,
    samples
)


# -------------------------
# Multiplication
# -------------------------

indices, samples = multiply_signal(
    signal1,
    5
)

MultiplySignalByConst(
    5,
    indices,
    samples
)


# -------------------------
# Shift +3
# -------------------------

indices, samples = shift_signal(
    signal1,
    3
)

ShiftSignalByConst(
    3,
    indices,
    samples
)


# -------------------------
# Folding
# -------------------------

indices, samples = fold_signal(
    signal1
)

Folding(
    indices,
    samples
)


print("\n=============================================")