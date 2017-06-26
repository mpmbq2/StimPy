import numpy as np
import scipy.signal as signal
import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mini_utils as mu


def template_match(function, data, template):

    original_shape = data.shape
    data = data.flatten()
    # Define holder, make windows
    detector = []
    windows = mu.rolling_window(trace, len(template))

    # Make detection trace
    for window in windows:
        detector.append(function.detect(window, template))

    # Add length to time tracker
    detector = np.reshape(detector, original_shape)

    return detector
