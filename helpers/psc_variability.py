def find_average():

    peaks = []
    for i in  stf.get_selected_indices():
        trace = stf.get_trace(trace=i)
        base = trace[int(stf.get_base_start()):int(stf.get_base_end())]
        base = np.median(base)
        
        p = trace[stf.get_peak_start():stf.get_peak_end()] - base
        peaks.append(np.min(p))
        
    peak_mean = np.mean(peaks)
    peak_error = np.std(peaks)
    
    stf.show_table({'Peak': peak_mean, 'Error': peak_error})
    
    return peak_mean, peak_error
    
    
def correct_autapse():
    
    traces = []
    fit_time = stf.get_fit_end() - stf.get_fit_start()
    x = np.arange(fit_time)
    
    trace_time = stf.get_peak_end() - stf.get_fit_start()
    y = np.arange(trace_time)
    
    for i in stf.get_selected_indices():
    
        trace = stf.get_trace(trace=i)
        base = np.median(trace[get_base_start():get_base_end()])
    
        trace = trace[stf.get_fit_start():stf.get_peak_end()] - base
        fit = np.polyfit(x, trace[:fit_time], 1)
        
        line = fit[0] * y + fit[1]
        line[line > 0] = 0
        
        traces.append(trace - line)
        
    traces = np.array(traces)
    
    new_window_matrix(traces)
    
    return traces
        
    
    
     
        
