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
    # with Pool(processes=6) as pool:
    #     detection_func = partial(function.detect, template=temp)
    #     detector = pool.map(detection_func, windows)
    for window in windows:
        detector.append(function.detect(window, template=temp))

    detector = np.pad(np.array(detector), (0,164), 'edge')
    print("Detector shape: {0}".format(detector.shape))
    print(np.max(detector))
    # TODO: Clean up comments. Lots of functions have been comented out.
    return detector

def find_events(detector, threshold=4):

    # Find peaks
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

def parameters(events):
    '''
    Given an array of synaptic events, returns parameters of those events.
    Optionally, it excludes events based on predefined terms.

    Flow:
        Events are baselined using first 100 points and peakutils.baseline
            with deg=1 or deg=2.
        Baselined events are checked for max derivative in [50:150].
            If they fall below cutoff, append False to deriv_acceptance list.
        Filtered events are checked for peak amplitude in [50:150]. If less than
            10 pA, drop (append False to list).
        Events filtered on risetime
        Events filtered on decay time
    Returns:
        Dictionary containing only filtered events and a DataFrame describing
            them.
    '''
    pass
