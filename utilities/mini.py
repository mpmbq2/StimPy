import theano as th
import numpy as np

def _epsc_template(points=None):
    '''

    :param samplerate: float
        Sampling rate of the experiment. Default is 10 kHz.
    :param points: scalar
        Desired size of the event. Default is 100 points
    :return: ndarray
        1-D numpy array of length (points) containing the epsc waveform
    '''
    if points is None:
        points = 100
    time = np.linspace(1, points, num=points)
    temp = np.array([(1 - np.exp(-(t - time[0]) / 0.5)) * np.exp(-(t - time[0]) / 6) for t in time])
    return -temp


def _ipsc_template(points=None):
    '''

        :param samplerate: float
            Sampling rate of the experiment. Default is 10 kHz.
        :param points: scalar
            Desired size of the event. Default is 100 points
        :return: ndarray
            1-D numpy array of length (points) containing the epsc waveform
        '''

    if points == None
        points = 100
    time = np.linspace(1, points, num=points)
    temp = np.array([(1 - np.exp(-(t - time[0]) / 0.5)) * np.exp(-(t - time[0]) / 30) for t in time])
    return -temp


def detection(trace, template=None):
    '''

    :param trace: ndarray
        Voltage clamp signal to be analyzed
    :param template: string
        Specify if the deterction is for EPSCs or IPSCs
        Default is 'epsc'
    :return: ndarray
        Indices of detected events
    '''

    if template == None:
        template = 'epsc'

    if template == 'epsc':
        temp = _epsc_template(points=None)

    if template == 'ipsc':
        temp = _ipsc_template(points=None)

    def rolling_window(a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    windows = rolling_window(trace, len(temp))
    detection_threshold = np.empty(trace.shape)

    for idx, data in enumerate(windows):
        scale = (np.sum((temp * data)) - np.sum(temp) * (np.sum(data)/len(temp)))/(np.sum((temp**2)) - np.sum(temp) * (np.sum(temp)/len(temp)))
        offset = (np.sum(data) - scale * np.sum(temp))/len(temp)
        fitted = temp * scale + offset
        sse = np.sum((data - fitted)**2)
        error = (sse/(len(temp)-1))**1/2
        detection_threshold[idx] = scale/error


def extraction(trace, event_indicies):
