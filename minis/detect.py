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


def template_match(function, data, temp):

    # Flatten data array
    original_shape = data.shape
    data = data.flatten()
    # Define holder, make windows
    detector = []
    windows = mu.rolling_window(data, len(temp))
    print("Data shape: {0}".format(data.shape))
    # Make detector trace
    with Pool(processes=6) as pool:
        detection_func = partial(function.detect, template=temp)
        detector = pool.map(detection_func, windows)
    #for window in windows:
    #    detector.append(function.detect(window, template))

    detector = np.pad(np.array(detector), (0,164), 'edge')
    print("Detector shape: {0}".format(detector.shape))
    # TODO: Clean up comments. Lots of functions have been comented out.
    # reshape data
    # Don't need to reshape, because will just collapse again later
    #detector = np.reshape(detector, original_shape)
    #print("Detector reshaped: {0}".format(detector.shape))

    return detector

@progress(char='#', pause=1.0)
def find_events(detector, threshold=4):

    # Set values that don't cross threshold to 0
    detector[detector < threshold] = np.nan
    # Find peaks
    # with Pool(processes=4) as pool:
    #     function = partial(peakutils.peak.indexes, thres=0.001, min_dist=10)
    #     peak_indices = pool.map(function, detector)
    peak_indices = peakutils.peak.indexes(detector, thres=0.001, min_dist=10)

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
    return events
