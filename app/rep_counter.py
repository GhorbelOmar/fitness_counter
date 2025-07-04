import numpy as np
from typing import List, Tuple
from app.models import RepCountRequest


def keep_only_outliers(series: list[float]) -> list[float]:
    if len(series) < 3:
        return []
    arr = np.array(series)
    q1, q3 = np.percentile(arr, [30, 60])
    avg = np.mean(arr)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    output = []
    for v in series:
        if v < lower_bound or v > upper_bound:
            output.append(v)
        else:
            output.append(0)
    return output


def find_local_extrema(signal: List[float]) -> Tuple[List[int], List[int]]:
    positive_maxima = []
    negative_minima = []

    for i in range(1, len(signal) - 1):
        if signal[i] > signal[i - 1] and signal[i] > signal[i + 1] and signal[i] > 0:
            positive_maxima.append(i)
        elif signal[i] < signal[i - 1] and signal[i] < signal[i + 1] and signal[i] < 0:
            negative_minima.append(i)

    return positive_maxima, negative_minima

def count_cycles(series: list[float]) -> int:
    positive_maximas, negative_minimas = find_local_extrema(series)
    print(f"Positive Maximas: {positive_maximas}, Negative Minimas: {negative_minimas}")
    count = 1
    for m1,m2 in zip(positive_maximas, positive_maximas[1:]):
        if any(m1 < n < m2 for n in negative_minimas):
            count += 1
    return count


def find_useful_axis(xyz: list[list[float]]) -> list[float]:
    """
    for each series, min max scale the values and calculate the std deviation.
    return only a list of the series that have the highest std deviation.
    """
    scaled = []
    for series in xyz:
        if len(series) < 3:
            continue
        arr = np.array(series)
        min_val = np.min(arr)
        max_val = np.max(arr)
        if max_val == min_val:
            scaled_series = np.zeros_like(arr)
        else:
            scaled_series = (arr - min_val) / (max_val - min_val)
        scaled.append(scaled_series)

    std_devs = [np.std(s) for s in scaled]
    if not std_devs:
        return []
    max_std_dev_index = np.argmax(std_devs)
    print(f"Max std dev index: {max_std_dev_index}, std dev: {std_devs[max_std_dev_index]}")
    return xyz[max_std_dev_index]


def count_reps(accel_data: RepCountRequest) -> int:
    """
    Count the number of repetitions in the accelerometer data.
    """
    xyz = [accel_data.data[i].x for i in range(len(accel_data.data))], \
          [accel_data.data[i].y for i in range(len(accel_data.data))], \
          [accel_data.data[i].z for i in range(len(accel_data.data))]
    axis_in_use = find_useful_axis(xyz)

    if not axis_in_use:
        return 0

    # move all points in the series down by the average value of the series
    avg = np.mean(axis_in_use)
    axis_in_use = [point - 1.2 * avg for point in axis_in_use]

    count = count_cycles(axis_in_use)
    return count