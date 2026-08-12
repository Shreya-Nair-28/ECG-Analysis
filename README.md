# ECG Signal Processing and Heart-Rate Analysis Using Python

## Overview

This project uses Python to analyze real electrocardiogram (ECG) recordings from the MIT-BIH Arrhythmia Database on PhysioNet.

The project focuses on processing ECG signals, detecting R-peaks, calculating heart rate, and investigating how band-pass filtering affects the analysis.

## Research Question

How does band-pass filtering affect automated ECG R-peak detection and heart-rate estimation across different MIT-BIH ECG recordings?

## Objectives

- Load real ECG recordings using WFDB.
- Visualize ECG signals using Matplotlib.
- Apply a band-pass filter to reduce unwanted signal components.
- Detect R-peaks using SciPy.
- Calculate R-R intervals and average heart rate.
- Compare results from raw and filtered ECG signals.
- Compare detected beat counts with expert annotations.
- Organize results using Pandas and save them as a CSV dataset.

## Dataset

The project uses the MIT-BIH Arrhythmia Database available through PhysioNet.

The analysis uses selected 30-second sections of several recordings.

## Tools and Libraries

- Python
- NumPy
- Matplotlib
- Pandas
- SciPy
- WFDB

## Method

The analysis follows this workflow:

ECG recording  
↓  
Select analysis window  
↓  
Band-pass filtering  
↓  
R-peak detection  
↓  
R-R interval calculation  
↓  
Heart-rate calculation  
↓  
Raw vs filtered comparison  
↓  
Results stored in CSV

## Results

Five ECG recordings were analyzed using the same baseline settings.

For Records 100, 101, 201, and 223, the raw and filtered average heart-rate estimates were very similar, with percentage differences below 0.01%.

Record 222 showed a larger difference of approximately 1.81% and also had fewer detected peaks than the expert beat annotations.

These results suggest that the filtering step had little effect on average heart-rate estimation for most of the tested recordings, while the performance of the fixed peak-detection parameters varied between recordings.

## Limitations

The project uses a simple peak detector with fixed amplitude and minimum-distance parameters. ECG amplitude and morphology can vary between recordings, so the detector does not perform equally well on every signal.

Only selected 30-second sections were analyzed rather than complete recordings.

The project uses expert annotations as a reference for beat counts but does not perform a full beat-by-beat accuracy evaluation.

## Conclusion

This project demonstrates a Python-based workflow for loading, preprocessing, visualizing, and analyzing real ECG signals.

For most of the tested recordings, filtering preserved the estimated average heart rate with very little change. The different behavior observed in Record 222 demonstrates a limitation of using fixed peak-detection parameters across different ECG recordings.

## Project Structure

ECG-Analysis/
├── ecg_analysis.py
├── results_analysis.py
├── ecg_results.csv
├── README.md
├── requirements.txt
└── plots/
    ├── heart_rate_comparison.png
    └── filtering_difference.png