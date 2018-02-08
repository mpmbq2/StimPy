import numpy as np
import scipy.signal


class AnalogData:
    def __init__(self, signal=None, time=None, units=None, sampling_rate=None):
        self.signal = signal
        self.time = time
        self.units = units
        self.sampling_rate = sampling_rate

    def filter(self, freq=1000, in_place=True):
        '''This method filters the self.working_data attribute to produce more reliable detection.
        ::Params::
        freq = frequency of filtering. Default is 1 kHz.
        type = type of filter to use (Options: Bessel, Butterworth, Gaussian). Default is Bessel.
        channel = the channel to be filtered. {'one', 'two' or 'both'}
        in_place = Whether to operate on the file data directly or a copy. Default is False

        ::Returns::
        Filtered file object or True if executed fully
        '''

        # Create filter
        Wn = freq/self.sampling_rate
        order = 4
        b, a = scipy.signal.bessel(order, Wn)
        for idx, trace in enumerate(self.signal):
            self.signal[idx] = scipy.signal.filtfilt(b, a, trace)
