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
        -'zero' replaces the artifact with zeros (Not supported yet)
        
        -'linear' replaces the artifact with a line connecting the two points at 
        either end
        
        -'quad' performs a quadratic interpolation to infer the data
    
    :: Output ::
    
    A new window with the blanked data
    
    trace: The corrected trace
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
    # The next line with interp1d fails by essentially consuming all RAM in a fraction of a second
    # interp = interpolate.interp1d(indices[not_nan], trace[not_nan], kind=method)
    # Replace interp1d with interpolate.InterpolatedUnivariateSpline
    if method == 'cubic':
        k = 3
    elif method == 'quad':
        k = 2
    elif method == 'linear':
        k = 1
    interp = interpolate.InterpolatedUnivariateSpline(indices[not_nan], trace[not_nan], k=3)
    # TODO: Add ability to use zero instead of linear
    # Replace trace with interpolated trace
    trace = interp(indices)
    # Make new window and return trace
    stf.new_window(trace)

    return trace


def multi_baseline(interp=True):
    """
    This function requires baseline cursors to be set at the first baseline 
    point, and latency cursors to be set at the second baseline point. It will 
    return a new window with the region between the cursors, proportionally
    baselined. 
    i.e. it interpolates a straight line between the two baseline points, which is then subtracted from the trace
    """
    # Get data
    data = stf.get_trace()
    trace = data.copy
    # Define baselines
    baseline_start = (int(stf.get_base_start()), int(stf.base_fit_end()))
    baseline_end = (int(stf.get_fit_start()), int(stf.get_fit_end()))
    # Set middle region to NaN
    trace[baseline_start[1]:baseline_end[0]] = [np.nan for _ in trace[baseline_start[1]:baseline_end[0]]]
    # Find all non-NaN values
    not_nan = np.isfinite(trace)
    # Create indices for full trace
    indices = np.arange(len(trace))
    # Create interpolation function
    if interp:
        interp = interpolate.interp1d(indices[not_nan], trace[not_nan], kind='linear')
        # Interpolate the line and fit the data with a line
        interp_trace = interp(indices)
        line = np.polyfit(indices, interp_trace, 1)
    else:
        line = np.polyfit(indices, trace[not_nan], 1)
    # Subtract the line
    data = data - line
    # Make new window and return trace
    stf.new_window(data)

    return trace

