import os
import numpy as np
import pandas as pd
import pickle
from .AbfFile import AbfFile
import stf


class DataSet:

    def __init__(self, path=None):

        self.path = path

        # Initialize metadata
        if not os.path.exists(os.path.join(path, '.stimpy')):
            os.makedirs(os.path.join(path, '.stimpy'))
            self.metadata = pd.read_csv(os.path.join(path, 'meta.csv'))
            self.metadata.to_pickle(os.path.join(path, '.stimpy', 'metadata.pkl'))
        else:
            self.metadata = pd.read_pickle(os.path.join(path, '.stimpy', 'metadata.pkl'))

        # Initialize PSC data
        if os.path.isfile(os.path.join(self.path, '.stimpy', 'psc_data.pkl')):
            self.psc_data = pd.read_csv(os.path.join(self.path, '.stimpy', 'psc_data.csv'))
        else:
            self.psc_data = None

    def psc_analysis(self):

        self.psc_data = self.metadata[self.metadata.recording_type == 'psc']
        self.psc_data['ch1_self_psc'] = [False for _ in self.psc_data]
        self.psc_data['ch1_other_psc'] = [False for _ in self.psc_data]
        self.psc_data['ch2_self_psc'] = [False for _ in self.psc_data]
        self.psc_data['ch2_other_psc'] = [False for _ in self.psc_data]
        self.psc_data['ch1_self_tau'] = [False for _ in self.psc_data]
        self.psc_data['ch1_other_tau'] = [False for _ in self.psc_data]
        self.psc_data['ch2_self_tau'] = [False for _ in self.psc_data]
        self.psc_data['ch2_other_tau'] = [False for _ in self.psc_data]

        for idx, abffiles in enumerate(self.psc_data):
            # Initialize Channel 1
            data = AbfFile(abffiles, self.path)
            stf.new_window_matrix(data.channel1.signal)

            # Cell 1 to Self
            advance_var = input("Cell 1: Select the traces to use, set the Peak, Baseline, and fit cursors for self.\n"
                                "If no connection exists, type 'no connection'\n"
                                "Type 'y' to advance to the next trace:\t")

            while advance_var is not 'y' or advance_var is not 'no connection':
                advance_var = input("You must type 'y' or 'no connection' to advance:\t")

            if advance_var == 'no connection':
                self.psc_data['ch1_self_psc'][idx] = None
                self.psc_data['ch1_self_tau'][idx] = None
            else:
                peaks = np.array(
                    [np.min(trace[stf.get_peak_start():stf.get_peak_end()]) for trace in data.channel1.signal]
                )
                bases = np.array(
                    [np.mean(trace[stf.get_base_start():stf.get_base_end()]) for trace in data.channel1.signal]
                )
                peak = np.mean(peaks - bases)
                fit = stf.leastsq(0)
                self.psc_data['ch1_self_psc'][idx] = peak
                self.psc_data['ch1_self_tau'][idx] = fit['Tau_0']

            # Cell 2 to Cell 1
            advance_var = input("Great, now do the same for Cell 2 onto Cell 1.\n"
                                "Type 'y' to advance to the next trace:\t")

            while advance_var is not 'y' or advance_var is not 'no connection':
                advance_var = input("You must type 'y' or 'no connection' to advance:\t")

            if advance_var == 'no connection':
                self.psc_data['ch2_other_psc'][idx] = None
                self.psc_data['ch2_other_tau'][idx] = None
            else:
                peaks = np.array(
                    [np.min(trace[stf.get_peak_start():stf.get_peak_end()]) for trace in data.channel1.signal]
                )
                bases = np.array(
                    [np.mean(trace[stf.get_base_start():stf.get_base_end()]) for trace in data.channel1.signal]
                )
                peak = np.mean(peaks - bases)
                fit = stf.leastsq(0)
                self.psc_data['ch2_other_psc'][idx] = peak
                self.psc_data['ch2_other_tau'][idx] = fit['Tau_0']

            # Initialize Channel 2
            data = AbfFile(abffiles, self.path)
            stf.new_window_matrix(data.channel1.signal)

            # Cell 2 to Self
            advance_var = input("Cell 2: Select the traces to use, set the Peak, Baseline, and fit cursors for self.\n"
                                "If no connection exists, type 'no connection'\n"
                                "Type 'y' to advance to the next trace:\t")

            while advance_var is not 'y' or advance_var is not 'no connection':
                advance_var = input("You must type 'y' or 'no connection' to advance:\t")

            if advance_var == 'no connection':
                self.psc_data['ch2_self_psc'][idx] = None
                self.psc_data['ch2_self_tau'][idx] = None
            else:
                peaks = np.array([np.min(trace[stf.get_peak_start():stf.get_peak_end()]) for trace in data.channel1.signal])
                bases = np.array(
                    [np.mean(trace[stf.get_base_start():stf.get_base_end()]) for trace in data.channel1.signal])
                peak = np.mean(peaks - bases)
                fit = stf.leastsq(0)
                self.psc_data['ch2_self_psc'][idx] = peak
                self.psc_data['ch2_self_tau'][idx] = fit['Tau_0']

            # Cell 2 to Cell 1
            advance_var = input("Great, now do the same for Cell 2 onto Cell 1.\n"
                                "Type 'y' to advance to the next trace:\t")

            while advance_var is not 'y' or advance_var is not 'no connection':
                advance_var = input("You must type 'y' or 'no connection' to advance:\t")

            if advance_var == 'no connection':
                self.psc_data['ch1_other_psc'][idx] = None
                self.psc_data['ch1_other_tau'][idx] = None
            else:
                peaks = np.array([np.min(trace[stf.get_peak_start():stf.get_peak_end()]) for trace in data.channel1.signal])
                bases = np.array(
                    [np.mean(trace[stf.get_base_start():stf.get_base_end()]) for trace in data.channel1.signal])
                peak = np.mean(peaks - bases)
                fit = stf.leastsq(0)
                self.psc_data['ch1_other_psc'][idx] = peak
                self.psc_data['ch1_other_tau'][idx] = fit['Tau_0']

        self.psc_data.to_csv(os.path.join(self.path, '.stimpy', 'psc_data.csv'))
