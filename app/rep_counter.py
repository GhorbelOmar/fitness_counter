import numpy as np
from app.models import RepCountRequest
from typing import Tuple
from scipy.signal import find_peaks

def count_cycles(data: list[float], height_threshold_ratio=0.8, distance_threshold=250) -> Tuple[int, np.ndarray]:
    """
    Counts the number of cycles in a time-series dataset by finding prominent peaks.

    Args:
        data (list or np.ndarray): A list of floats representing the signal data.
        height_threshold_ratio (float): The ratio of the maximum peak height to use as a
                                        threshold. For example, 0.8 means the threshold
                                        will be 80% of the highest peak in the data.
        distance_threshold (int): The minimum horizontal distance (in number of data points)
                                  between consecutive peaks. This should be adjusted based
                                  on the approximate length of a cycle in your data.

    Returns:
        int: The number of detected cycles.
        np.ndarray: The indices of the detected peaks.
    """
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    if data.size == 0:
        return 0, np.array([]) # Return early for empty data

    # Dynamically calculate the height threshold
    max_height = np.max(data)
    dynamic_height_threshold = max_height * height_threshold_ratio

    # find_peaks returns the indices of the peaks in the data array
    peaks, _ = find_peaks(data, height=dynamic_height_threshold, distance=distance_threshold)

    # The number of peaks corresponds to the number of cycles
    num_cycles = len(peaks)

    return num_cycles, peaks




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
    count, peaks = count_cycles(axis_in_use, height_threshold_ratio=0.8, distance_threshold=250)
    return count