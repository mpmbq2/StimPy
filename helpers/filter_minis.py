
def fit_trace(trace):
    
    def template(time, norm, rise, decay, delay, end):
        delay_phase = np.zeros(delay)
        event_phase = np.arange(delay-delay, end-delay)
        end_phase = np.zeros(len(time) - end)
        time = np.concatenate((delay_phase, event_phase, end_phase), axis=0)
        out = norm * (np.exp(-time/rise) - np.exp(-time/decay))
        return out

    time = np.arange(0, len(trace))
    p0 = np.array([20, 8, 20, 100, 300])
    
    def residuals(p0, trace, time):
        return trace - template(time, p0[0], p0[1], p0[2], p0[3], p0[4])
    
    return leastsq(residuals, p0, args=(trace, time))

    
def filter_events(traces):
    
    keepers = np.ones(traces.shape[0])
    def template(time, norm, rise, decay, delay, end):
        out = norm * (np.exp(-time/rise) - np.exp(-time/decay))
        out[:delay] = 0
        out[end:] = 0
        return out
    
    for idx, trace in enumerate(traces):
        base = np.median(trace)
        trace = trace-base
        peak = np.min(trace)
        if peak > -10:
            keepers[idx] = 0
            continue
        params, _ = fit_trace(trace)
        fit = template(time, params[0], params[1], params[2], params[3], params[4])
        over_half = fit < peak/2
        halfs = [i for i, x in enumerate(np.diff(over_half)) if x]
        if len(halfs) < 2:
            keepers[idx] = 0
            continue
        halfwidth = halfs[1] - halfs[0]
        if (halfwidth > 40) | (halfwidth < 10):
            keepers[idx] = 0
            continue
    return keepers
    
        
def check_fits(traces):
    new = []
    for trace in traces:
        params, _ = fit_trace(trace)
        fit = template(time, params[0], params[1], params[2], params[3], params[4])
        new.append(fit)
    new_window_matrix(new)
        
