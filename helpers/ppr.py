import numpy as np
import stf


def ppr_peak():
    # Get function values
    decay_func = stf.leastsq(0)

    # Create time from fit start to next peak
    x = np.arange(stf.get_fit_start(), stf.peak_index())

    # Create fitted curve up until peak
    trace = [(decay_func['Offset'] + decay_func['Amp_0'] * np.exp(-(ind/10.0)/decay_func['Tau_0'])) for ind, val in enumerate(x)]
    
    # Find peak value
    peak_val = stf.get_peak()-stf.get_base()
    print('The measured peak is {0} pA'.format(peak_val))

    # Find value of fit at peak
    fit_peak = trace[-1] - stf.get_base()
    print('Tau is {0} pA'.format(decay_func['Tau_0']))
    print('The fitted peak is {0} pA'.format(fit_peak))
    print('The baseline is {0} pA'.format(stf.get_base()))
    # stf.new_window(trace)

    final_peak = peak_val - fit_peak
    print('The final peak is {0} pA'.format(final_peak))

    return True
