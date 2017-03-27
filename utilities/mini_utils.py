import numpy as np
import scipy.signal as signal


def mini_cut():
    traces = []
    for i in stf.get_selected_indices():
        traces.append(get_trace(trace=i)[40000:])
    trace = np.array(traces)
    stf.new_window_matrix(trace)
    
    return True
    
def mini_filter():
    pass

def mini_detect():
    
    # Initialize variables
    total_minis = []
    total_iei = []
    mini_traces = []
    event_count = 0
    cumulative_time = 0
    
    # Loop through selected traces
    for i in stf.get_selected_indices():
        # Initialize within-loop variables
        mini_idx = []
        iei = []
        stf.set_trace(i)
        
        # Get trace and compute derivative in pA/ms
        trace = stf.get_trace(i)
        deriv = np.diff(trace)/stf.get_sampling_interval()
        
        # Add length to time tracker
        cumulative_time = cumulative_time + len(trace)
        
        # While-loop for iterating over the whole trace looking for events
        idx = 0
        while idx < len(deriv):
            # Check to see if threshold is crossed
            if deriv[idx] <= -50.0:
                # If corssed, extract information
                # Only look for inter-event interval if another event has 
                # already been found
                if len(mini_idx) > 1:
                    iei.append((idx - mini_idx[-1])/10000.0)
                mini_idx.append(idx)
                mini_traces.append(trace[idx-150:idx+400])
                stf.set_marker(idx, trace[idx])
                event_count += 1
                # Advance by 150 samples
                idx += 150
            else:
                idx += 1
        # Append the information from this sweep to the master list
        total_minis.append(mini_idx)
        total_iei.extend(iei)
    
    # Plot the minis for manual inspection
    stf.new_window_matrix(mini_traces)
    
    # Calculate necessary info and return dictionary
    ave_iei = np.mean(total_iei)
    event_freq = event_count / (cumulative_time / 10000.0) # Events per second
    parms_dict = {
                    "Mini Times": total_minis, 
                    "Average Inter-event interval": ave_iei,
                    "Event Frequency": event_freq
                 }
    
    return parms_dict

def mini_cluster():
    """
    Takes selected indices from the displayed minis and returns minis in 
    separate windows clustered by Peak, Half-width, and 90-10% decay time
    """
    # Initialize variables for sorting
    cluster_vars = []
    
    # Main loop to find values for variables
    for idx in stf.get_selected_indices():
        trace_vars = []
        # Get trace
        trace = stf.get_trace(idx)
        # Find baseline
        base = np.mean(trace[stf.get_base_start():stf.get_base_end()])
        # Subtract baseline
        trace = trace - base
        # Find peak
        peak = np.min(trace[stf.get_peak_start():stf.get_peak_end()])
        trace_vars.append(peak)
        peak_idx = np.argmin(trace[stf.get_peak_start():stf.get_peak_end()])
        
        # Find forward point for half-width
        f_roll = peak_idx
        while trace[f_roll] < (0.5*peak):
            f_roll += 1
        
        # Find backward point for half-width
        b_roll = peak_idx
        while trace[b_roll] < (0.5*peak):
            b_roll -= 1
        
        half_width = (f_roll - b_roll) * 0.1 # Half width in ms
        trace_vars.append(half_width)
        
        # Find ninty-ten times
        ninty_idx = peak_idx
        while trace[ninty_idx] < (0.9*peak):
            ninty_idx += 1
        ten_idx = peak_idx
        while trace[ten_idx] < (0.1*peak):
            ten_idx += 1
        decay_time = (ten_idx - ninty_idx) * 0.1 # Decay time in ms
        trace_vars.append(decay_time)
        cluster_vars.append(trace_vars)
        
        
    
