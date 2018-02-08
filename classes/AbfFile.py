from .AnalogData import AnalogData
import numpy as np
import pandas as pd


class AbfFile:
    """A class that will contain the information on the files in the dataset, such as file names, types, recorded
    units, sampling rate, and recording date"""

    def __init__(self, analogsignals, file_name=None, date=None):
        self.signals = analogsignals
        self.file_name = file_name
        self.recording_date = date
        self.channel_1_minis = None
        self.channel_2_minis = None

    def extract(self, threshold=-1, method='derivative'):
        '''This method extracts mPSCs
        ::Params::
        threshold = This is the detection threshold for template correlation.
        method = The method to use for extracting minis.
        channel = The channel to be used for detection

        ::Returns::
        Dictionary: Keys are 'Data', 'Minis', and 'Metadata'
        '''

        # Extract minis
        minis1 = self._detect(channel=0, threshold=threshold)
        minis2 = self._detect(channel=1, threshold=threshold)
        print(len(minis1['indices']))
        print(len(minis2['indices']))
        # Compute mini parameters and exclude
        self._exclude(channel=0, minis=minis1)
        self._exclude(channel=1, minis=minis2)
        #
        # # Turn metadata into pandas dataframe
        # extracted_meta = pd.DataFrame(extracted_meta)
        #
        # return {'Data': self.working_data, 'Minis': minis, 'Metadata': extracted_meta}

    def _detect(self, channel=0, threshold=-1):
        deriv = np.diff(self.signals[channel].signal, axis=1)
        sweep_events = []
        event_starts = []
        for idx1, sweep in enumerate(deriv):
            bool_events = sweep < threshold
            event_windows = []
            for idx2, value in enumerate(bool_events):
                if (idx2 > 50000) & (idx2 < len(sweep)-600) & (value):
                    event_windows.append(idx2)
            event_windows = np.array(event_windows)
            for idx2, value in enumerate(np.diff(event_windows)):
                if idx2 == 0:
                    start = event_windows[idx2]
                    event_starts.append(tuple([idx1, start]))
                    sweep_events.append(
                        self.signals[channel].signal[idx1, start-100:start+600]
                        )
                elif value > 1:
                    start = event_windows[idx2+1]
                    event_starts.append(tuple([idx1, start]))
                    sweep_events.append(
                        self.signals[channel].signal[idx1, start-100:start+600]
                        )

        return {'traces': np.array(sweep_events), 'indices': event_starts}

    def _exclude(self, channel=0, minis=None):
        mini_params = []
        for idx, trace in enumerate(minis['traces']):
            base = np.mean(trace[:50])
            trace = trace - base
            peak_ind = np.argmin(trace)
            peak = np.min(trace)
            half_peak = peak/2
            half_start = np.argmax(trace < half_peak) - 1
            half_end = np.argmax(trace[peak_ind:] > half_peak) + peak_ind
            half_width = (half_end - half_start) / 10
            mini_params.append({
                    'index': minis['indices'][idx],
                    'peak': peak,
                    'half_width': half_width,
                    'trace': trace,
                    'keep': True
                    })

        minis = mini_params

        for idx, values in enumerate(minis):
            if (values['peak'] > -10) | (values['half_width'] < 3) | (values['half_width'] > 50):
                values['keep'] = False

        if channel == 0:
            self.channel_1_minis = pd.DataFrame(minis)
        elif channel == 1:
            self.channel_2_minis = pd.DataFrame(minis)
        # if channel == 0:
        #     self.channel_1_minis = {
        #             'traces': np.array([x for idx, x in enumerate(minis['traces']) if minis['keep'][idx]]),
        #             'indices': [x for idx, x in enumerate(minis['indices']) if minis['keep'][idx]],
        #             'parameters': [x for idx, x in enumerate(minis['parameters']) if minis['keep'][idx]],
        #             }
        # elif channel == 1:
        #     self.channel_2_minis = {
        #             'traces': np.array([x for idx, x in enumerate(minis['traces']) if minis['keep'][idx]]),
        #             'indices': [x for idx, x in enumerate(minis['indices']) if minis['keep'][idx]],
        #             'parameters': [x for idx, x in enumerate(minis['parameters']) if minis['keep'][idx]],
        #             }
