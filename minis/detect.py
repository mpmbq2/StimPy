import numpy as np
import scipy.signal as signal
import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mini_utils as mu
import peakutils
from prygress import progress
from multiprocessing import Pool
from functools import partial
import time


def template_match(function, data, temp):

    start = time.time()
    # Flatten data array
    original_shape = data.shape
    data = data.flatten()
    # Define holder, make windows
    detector = []
    windows = mu.rolling_window(data, len(temp))
    print("Data shape: {0}".format(data.shape))
    # Make detector trace
    # with Pool(processes=6) as pool:
    #     detection_func = partial(function.detect, template=temp)
    #     detector = pool.map(detection_func, windows)
    for window in windows:
        detector.append(function.detect(window, template=temp))

    detector = np.pad(np.array(detector), (0,164), 'edge')
    print("Detector shape: {0}".format(detector.shape))
    print(np.max(detector))
    # TODO: Clean up comments. Lots of functions have been comented out.
    # reshape data
    # Don't need to reshape, because will just collapse again later
    #detector = np.reshape(detector, original_shape)
    #print("Detector reshaped: {0}".format(detector.shape))

    end = time.time()
    print("Elapsed time: {0}".format(end-start))
    return detector

def find_events(detector, threshold=4):

    # Find peaks
    # with Pool(processes=4) as pool:
    #     function = partial(peakutils.peak.indexes, thres=0.001, min_dist=10)
    #     peak_indices = pool.map(function, detector)
    temp_indices = peakutils.peak.indexes(detector, thres=0.0, min_dist=0)
    ct_indices = list()
    for idx in temp_indices:
        if detector[idx] >= threshold:
            ct_indices.append(True)
        else:
            ct_indices.append(False)
    peak_indices = temp_indices[ct_indices]

    return peak_indices

def extract_events(data, indices):

    # Flatten data so indices match the data
    data = data.flatten()
    events = list()
    for idx in indices:
        if (idx-100) < 0:
            continue
        elif (idx+300) > len(data):
            break
        else:
            events.append(data[idx-100:idx+300])
    return np.array(events)
