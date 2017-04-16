import numpy as np
from scipy import interpolate, signal
import stf


def blank_artifact(method='cubic'):
    """
    This function requires the fit cursors to be set. It corrects the 
    artifact located between the cursors based on the method specified by the 
    user. 
    
    :: Params ::
    
    method = ['zero', 'linear', 'quad', 'cubic']
        -'zero' replaces the artifact with zeros
        
        -'linear' replaces the artifact with a line connecting the two points at 
        either end
        
        -'quad' performs a quadratic interpolation to infer the data
    
    :: Output ::
    
    A new window with the blanked data
    """
    # Get data
    trace = stf.get_trace()
    # Define artifact
    artifact = (int(stf.get_fit_start()), int(stf.get_fit_end()))
    # Set artifact region to NaN
    trace[artifact[0]:artifact[1]] = [np.nan for _ in trace[artifact[0]:artifact[1]]]
    # Find all non-NaN values
    not_nan = np.logical_not(np.isnan(trace))
    # Create indices for full trace
    indices = np.arange(len(trace))
    # Create interpolation function
    interp = interpolate.interp1d(indices[not_nan], trace[not_nan], kind=method)
    # Replace trace with interpolated trace
    trace = interp(indices)
    # Make new window and return trace
    stf.new_window(trace)

    return trace


def multi_baseline():
    """
    This function requires baseline cursors to be set at the first baseline 
    point, and latency cursors to be set at the second baseline point. It will 
    return a new window with the region between the cursors, proportionally
    baselined. 
    i.e. it takes the difference between the first and second baseline, and 
    then baselines every point with a weighted subtraction
    """
    pass
