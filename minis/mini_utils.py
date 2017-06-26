from theano import function, tensor
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
    temp = np.array([(1 - np.exp(-(t - time[0]) / 0.5)) * np.exp(-(t - time[0]) / 8) for t in time])
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

    if points == None:
        points = 300
    time = np.linspace(1, points, num=points)
    temp = np.array([(1 - np.exp(-(t - time[0]) / 0.5)) * np.exp(-(t - time[0]) / 50) for t in time])
    return -temp


def rolling_window(a, window):

    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)

    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


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

    if template is None:
        temp = 'epsc'

    if template == 'epsc':
        temp = _epsc_template(points=100)

    if template == 'ipsc':
        temp = _ipsc_template(points=300)

    detection_threshold = []
    windows = rolling_window(trace, len(temp))
    detection_function = TensorDetect()
    print("Window shape: {0}".format(windows.shape))
    print("Template shape: {0}".format(temp.shape))

    for idx, data in enumerate(windows):
        #print(idx)
        #print(data.shape)
        detection_threshold.append(detection_function.detect(data, temp))

    return detection_threshold


class TensorDetect:

    def __init__(self):
        data = tensor.dvector('data')
        template = tensor.dvector('template')

        scale = ((template * data.T) - template.sum() * (data.sum() / template.shape[0])) / (
            (template ** 2.0).sum() - template.sum() * (template.sum() / template.shape[0]))
        self.scale_fn = function([data, template], scale)

        offset = (data.sum() - scale * template.sum()) / template.shape[0]
        self.offset_fn = function([data, template], offset)

        fit = template * scale + offset
        self.fit_fn = function([scale, template, offset], fit)

        error = (((data - fit)**2.0).sum()) / ((template.shape[0] - 1)**1/2)
        self.error_fn = function([data, fit, template], error)

        detection_threshold = scale / error
        self.detection_fn = function([scale, error], detection_threshold)

    def detect(self, data, template):

        scale = self.scale_fn(data, template)
        offset = self.offset_fn(data, template)
        fit = self.fit_fn(scale, template, offset)
        error = self.error_fn(data, fit, template)

        return self.detection_fn(scale, error)
