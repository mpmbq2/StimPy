import numpy as np
import pandas as pd
import stf
import stfio


"""Pseudocode describing the PSC analysis process to be used:
    1) PSC object created by user, pointing to MetaData object
    2) Psc.proceed() method called to open first file in list
    3) User prompted to select traces to use for channel 1 cell 1
    4) User prompted to set baseline, peak, and fit cursors for channel 1 cell 1
        4.1) User enters 'measure' to save locations
    5) User prompted to select traces to use for channel 1 cell 2
    6) User prompted to set baseline, peak, and fit cursors for channel 1 cell 2
        6.1) User enters 'measure' to save locations
    7) User prompted to select traces to use for channel 2 cell 1
    8) User prompted to set baseline, peak, and fit cursors for channel 2 cell 1
        8.1) User enters 'measure' to save locations
    9) User prompted to select traces to use for channel 2 cell 2
    10) User prompted to set baseline, peak, and fit cursors for channel 2 cell 2
        10.1) User enters 'measure' to save locations
    11) Baseline is measured at all 4 conditions, stored as 'holding_current'
    12) Peaks are measured by subtracting 'holding_current' from stf.get_peak for all traces (in for loop)
    13) Fits are obtained using stf.leastsq(0), and 'Tau_0' is saved
    
    But for now, just have user set baseline, peaks, and fit. Measure all selected, average together, and print to Table
    
    It would also be useful to write the I/O function to read in files using a pd.DataFrame. Maybe create a thin wrapper
        object with a state variable that is the index of the next file to be read. calling object.next() would advance 
        the state variable and open the file. Either use neo.AxonIO or stfio depending on which works.
"""
