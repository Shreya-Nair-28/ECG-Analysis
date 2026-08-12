import os

import wfdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt
from wfdb import rdann


# --------------------------------
# FUNCTION 1: Load ECG
# --------------------------------

def load_ecg(record_number):

    try:
        record = wfdb.rdrecord(
            record_number,
            pn_dir="mitdb"
        )

        return record

    except Exception:
        return None


# --------------------------------
# FUNCTION 2: Get ECG Signal
# --------------------------------

def get_ecg_signal(record, duration):

    # Convert requested seconds into number of samples
    num_samples = int(duration * record.fs)

    # Column 0 = first ECG channel
    ecg = record.p_signal[:num_samples, 0]

    # Convert sample numbers into seconds
    time = np.arange(num_samples) / record.fs

    return ecg, time


# --------------------------------
# FUNCTION 3: Filter ECG
# --------------------------------

def filter_ecg(ecg, fs):

    low_cutoff = 0.5
    high_cutoff = 40

    # Design a 4th-order Butterworth band-pass filter
    b, a = butter(
        4,
        [low_cutoff, high_cutoff],
        btype="bandpass",
        fs=fs
    )

    # Apply the filter
    filtered_ecg = filtfilt(
        b,
        a,
        ecg
    )

    return filtered_ecg


# --------------------------------
# FUNCTION 4: Get Expert Beats
# --------------------------------

def get_expert_beats(record_number, duration, fs):

    # Load MIT-BIH expert annotations
    annotation = rdann(
        record_number,
        "atr",
        pn_dir="mitdb"
    )

    # Convert duration into samples
    max_sample = int(duration * fs)

    expert_beats = []

    # Go through every annotation
    for sample, symbol in zip(
        annotation.sample,
        annotation.symbol
    ):

        # Stop when we reach the end of our
        # selected analysis window
        if sample >= max_sample:
            break

        # Keep normal beat annotations
        if symbol == "N":
            expert_beats.append(sample)

    return np.array(expert_beats)


# --------------------------------
# FUNCTION 5: Detect R-Peaks
# --------------------------------

def detect_peaks(ecg, threshold):

    peaks, properties = find_peaks(
        ecg,
        height=threshold,
        distance=180
    )

    return peaks


# --------------------------------
# FUNCTION 6: Calculate Heart Rate
# --------------------------------

def calculate_heart_rate(peaks, time):

    # Convert peak sample positions into seconds
    peak_times = time[peaks]

    # Calculate time between consecutive R-peaks
    rr_intervals = np.diff(peak_times)

    # Convert R-R intervals into BPM
    heart_rates = 60 / rr_intervals

    # Calculate average heart rate
    average_heart_rate = np.mean(heart_rates)

    return (
        peak_times,
        rr_intervals,
        heart_rates,
        average_heart_rate
    )


# =================================
# MAIN PROGRAM
# =================================

record_number = input(
    "Enter the record number (e.g., 100, 101, 201, 222): "
)


# --------------------------------
# Load ECG
# --------------------------------

record = load_ecg(record_number)


# Check whether loading worked
if record is None:

    print(
        f"Could not load Record {record_number}."
    )

    print(
        "The record may not exist, "
        "or there may be an internet connection problem."
    )

    exit()


# --------------------------------
# Choose Analysis Duration
# --------------------------------

duration = float(
    input(
        "Enter analysis duration in seconds (max 60): "
    )
)


# Check duration
if duration <= 0 or duration > 60:

    print(
        "Please enter a duration between 0 and 60 seconds."
    )

    exit()


# --------------------------------
# Get Expert Beats
# --------------------------------

expert_beats = get_expert_beats(
    record_number,
    duration,
    record.fs
)


print("\n--- EXPERT BEATS ---")

print(
    "Number of expert beats:",
    len(expert_beats)
)

print(
    "Expert beat samples:",
    expert_beats
)


# --------------------------------
# Get ECG
# --------------------------------

ecg, time = get_ecg_signal(
    record,
    duration
)


# --------------------------------
# Filter ECG
# --------------------------------

filtered_ecg = filter_ecg(
    ecg,
    record.fs
)


# --------------------------------
# Detect Peaks
# --------------------------------

# Detect peaks in RAW ECG
raw_peaks = detect_peaks(
    ecg,
    0.5
)


# Detect peaks in FILTERED ECG
filtered_peaks = detect_peaks(
    filtered_ecg,
    0.5
)


# --------------------------------
# Calculate RAW Heart Rate
# --------------------------------

(
    peak_times,
    rr_intervals,
    heart_rates,
    average_heart_rate
) = calculate_heart_rate(
    raw_peaks,
    time
)


# --------------------------------
# Calculate FILTERED Heart Rate
# --------------------------------

(
    filtered_peak_times,
    filtered_rr_intervals,
    filtered_heart_rates,
    filtered_average_heart_rate
) = calculate_heart_rate(
    filtered_peaks,
    time
)


# =================================
# CALCULATE HR DIFFERENCE
# =================================

hr_difference = abs(
    average_heart_rate
    - filtered_average_heart_rate
)

hr_percentage_difference = (
    hr_difference
    / average_heart_rate
) * 100


# =================================
# PRINT ECG INFORMATION
# =================================

print("\n--- ECG INFORMATION ---")

print(
    "Sampling frequency:",
    record.fs
)

print(
    "Signal names:",
    record.sig_name
)


# =================================
# RAW VS FILTERED PEAKS
# =================================

print("\n--- RAW VS FILTERED PEAKS ---")


print("\nRaw peak times:")

print(
    time[raw_peaks]
)


print("\nFiltered peak times:")

print(
    time[filtered_peaks]
)




# =================================
# SIMPLE VALIDATION
# =================================

print("\n--- SIMPLE VALIDATION ---")

print(
    "Expert beats:",
    len(expert_beats)
)

print(
    "Detected raw beats:",
    len(raw_peaks)
)

print(
    "Detected filtered beats:",
    len(filtered_peaks)
)


# =================================
# RESULTS DATAFRAME
# =================================

results = {
    "Record": [record_number],
    "Duration (s)": [duration],
    "Expert Beats": [len(expert_beats)],
    "Raw Peaks": [len(raw_peaks)],
    "Filtered Peaks": [len(filtered_peaks)],
    "Raw HR (BPM)": [average_heart_rate],
    "Filtered HR (BPM)": [filtered_average_heart_rate],
    "HR Difference (%)": [hr_percentage_difference]
}


df = pd.DataFrame(results)


# --------------------------------
# Load previous results if they exist
# --------------------------------

if os.path.exists("ecg_results.csv"):

    old_df = pd.read_csv(
        "ecg_results.csv"
    )

    df = pd.concat(
        [old_df, df],
        ignore_index=True
    )


# --------------------------------
# Save results
# --------------------------------

df.to_csv(
    "ecg_results.csv",
    index=False
)


print("\n--- RESULTS TABLE ---")

print(
    df.to_string(index=False)
)


# =================================
# RAW R-R INTERVAL ANALYSIS
# =================================

print("\n--- RAW R-R INTERVAL ANALYSIS ---")

print(
    "R-R intervals:",
    rr_intervals
)

print(
    "Shortest R-R interval:",
    np.min(rr_intervals)
)

print(
    "Longest R-R interval:",
    np.max(rr_intervals)
)

print(
    "Mean R-R interval:",
    np.mean(rr_intervals)
)


# =================================
# HEART RATE ANALYSIS
# =================================

print("\n--- HEART RATE ANALYSIS ---")

print(
    "Average heart rate:",
    average_heart_rate
)





# =================================
# GRAPH 1: RAW ECG
# =================================

plt.figure(
    figsize=(12, 4)
)

plt.plot(
    time,
    ecg,
    label="Raw ECG"
)

# Mark raw detected peaks
plt.plot(
    time[raw_peaks],
    ecg[raw_peaks],
    "x",
    markersize=10,
    label="Raw R-Peaks"
)

plt.title(
    f"Raw ECG - MIT-BIH Record {record_number}\n"
    f"Average Heart Rate: "
    f"{average_heart_rate:.1f} BPM"
)

plt.xlabel(
    "Time (seconds)"
)

plt.ylabel(
    "Amplitude (mV)"
)

plt.ylim(
    -0.5,
    1.2
)

plt.grid(True)

plt.legend()


# =================================
# GRAPH 2: FILTERED ECG
# =================================

plt.figure(
    figsize=(12, 4)
)

plt.plot(
    time,
    filtered_ecg,
    label="Filtered ECG"
)

# Mark filtered detected peaks
plt.plot(
    time[filtered_peaks],
    filtered_ecg[filtered_peaks],
    "x",
    markersize=10,
    label="Filtered R-Peaks"
)

plt.title(
    f"Filtered ECG - MIT-BIH Record {record_number}\n"
    f"Average Heart Rate: "
    f"{filtered_average_heart_rate:.1f} BPM"
)

plt.xlabel(
    "Time (seconds)"
)

plt.ylabel(
    "Amplitude (mV)"
)

plt.ylim(
    -0.5,
    1.2
)

plt.grid(True)

plt.legend()


# =================================
# SHOW GRAPHS
# =================================

plt.show()