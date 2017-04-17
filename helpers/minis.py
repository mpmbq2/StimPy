from __future__ import print_function
import numpy as np
import scipy.signal as signal
import stf
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import math
import .mini_utils as mu


class MiniRec:
    """
    MiniRec is an object used to analyzing miniature EPSCs and IPSCs. It takes no arguments to start. On initialization,
    It takes the selected traces and stores them as MiniRec.traces. The workflow from there is as follows:
    
    MiniRec.cut(point) cuts the trace at the given point and returns it in a new window
    
    MiniRec.filter() filters the data to make mini extraction more accurate
    
    MiniRec.detect(method) detects mini events using the method specified (either derivative or template-match). This
    method concludes by returning the detected minis in a new window. It also creates a dataframe (mini_df) to store
    The information concerning each detected mini (i.e. event number, trace, and index). This allows to easier analysis
    in the future.
    
    MiniRec.select() is called AFTER the user has gone through the minis to select which should be kept for further 
    analysis. The select method iterates over detected minis in mini_df and appends True or False to the row depending
    on whether the user chose to include that mini or not.
    
    MiniRec.plot_decay() computes all of the relevant parameters on the selected minis (half-width, decay time, peak)
    and plots them for manual inspection. It also plots vertical and horizontal lines at the default cutoffs for
    clustering IPSCs from EPSCs (decay of 5 ms) and minis from spontaneous (-50 pA) Using a peak cutoff is not 
    recommended as the way to display peak data will be with cumulative probability plots, so mini vs spontaneous
    activity is not terribly relevant.
    
    MiniRec.classify() 
    """
    def __init__(self):
    
        self.selected_traces = stf.get_selected_indices()
        self.traces = np.array([stf.get_trace(x) for x in self.selected_traces])
        self.fs = stf.get_sampling_interval()
        self.cut_traces = []
        self.mini_traces = None
        self.mini_df = None
        self.interevent_interval = []
        self.event_count = 0
        self.cumulative_time = 0
        self.cluster_df = pd.DataFrame()
    
    def cut(self, point):
    
        self.cut_traces = []
        for i in stf.get_selected_indices():
            self.cut_traces.append(self.traces[i][point:])
        stf.new_window_matrix(np.array(self.cut_traces))
    
    def filter(self, ftype='butter', freq=1000.0):
        """
        """
        rad_samp = freq * (2 * math.pi) / 10000.0
        if ftype == 'butter':
            b, a = signal.butter(5, rad_samp)
        elif ftype == 'bessel':
            b, a = signal.bessel(5, rad_samp)
        else:
        	print("Filter {0} not implemented".format(ftype))
            pass
        
        self.traces = signal.filtfilt(b, a, self.traces)
        stf.new_window_matrix(self.traces)

    def detect(self, method='template match', template_type='epsc', threshold=4):
        
        # Predefine universal variables
        self.selected_traces = stf.get_selected_indices()
        mini_traces = []
        mini_indices = []
        
        if method == 'template match':
            # Create detection function and template
            # TODO: Allow for selection of both epsc and ipsc templates
            detection_function = mu.TensorDetect()
            if template_type == 'epsc':
                temp = mu._epsc_template(points=150)
            elif template_type == 'ipsc':
                temp = mu._ipsc_template(points=300)
            # Define holder, make windows, predefine detection function
            for i in self.selected_traces:
                # Set trace in the stf window
                stf.set_trace(i)
                
                # Get trace, define holder, and make windows
                trace = self.cut_traces[i]
                detection_threshold = []
                windows = mu.rolling_window(trace, len(temp))
                
                # Make detection trace
                for idx, data in enumerate(windows):
                    detection_threshold.append(detection_function.detect(data, temp))
                
                # Add length to time tracker
                self.cumulative_time = self.cumulative_time + len(trace)
                
                # While-loop for iterating over the whole trace looking for events
                idx = 150
                while idx < (len(detection_threshold)-401):
                    # Check to see if threshold is crossed
                    if detection_threshold[idx] >= threshold:
                        # If crossed, extract information
                        mini_indices.append({'event_number': self.event_count, 
                                                    'trace': i, 
                                                    'index': idx})
                        mini_traces.append(trace[idx-150:idx+400])
                        stf.set_marker(idx, trace[idx])
                        self.event_count += 1
                        # Advance by 150 samples
                        idx += 150
                    else:
                        idx += 1
            
            self.mini_traces = np.asarray(mini_traces)
            # Plot the minis for manual inspection
            stf.new_window_matrix(self.mini_traces)
            
            # Calculate necessary info and return dictionary
            self.mini_df = pd.DataFrame(mini_indices)
            
            
        elif method == 'derivative':
            # Loop through selected traces
            for i in self.selected_traces:
                # Initialize within-loop variables
                stf.set_trace(i)
                
                # Get trace and compute derivative in pA/ms
                trace = self.cut_traces[i]
                deriv = np.diff(trace) / stf.get_sampling_interval()
                
                # Add length to time tracker
                self.cumulative_time = self.cumulative_time + len(trace)
                
                # While-loop for iterating over the whole trace looking for events
                idx = 150
                while idx < (len(deriv)-401):
                    # Check to see if threshold is crossed
                    if deriv[idx] <= threshold:
                        # If crossed, extract information
                        mini_indices.append({'event_number': self.event_count, 
                                                    'trace': i, 
                                                    'index': idx})
                        mini_traces.append(trace[idx-150:idx+400])
                        stf.set_marker(idx, trace[idx])
                        self.event_count += 1
                        # Advance by 150 samples
                        idx += 150
                    else:
                        idx += 1
            
            self.mini_traces = np.asarray(mini_traces)
            # Plot the minis for manual inspection
            stf.new_window_matrix(self.mini_traces)
            
            # Calculate necessary info and return dictionary
            self.mini_df = pd.DataFrame(mini_indices)
    
    def select(self):
        select_mini = []
        selected_indices = stf.get_selected_indices()
        
        for idx, values in enumerate(self.mini_df['event_number']):
            if values in selected_indices:
                select_mini.append(True)
            else:
                select_mini.append(False)
        
        self.mini_df['select_mini'] = pd.Series(select_mini)

    def plot_decay(self):
        """
        Takes selected indices from the displayed minis and returns minis in 
        separate windows clustered by Peak, Half-width, and 90-10% decay time
        """
        # Initialize variables for sorting
        cluster_vars = []
        
        # Main loop to find values for variables
        for idx, value in enumerate(self.mini_df['select_mini']):
            if value:
                flag = False
                trace = self.mini_traces[idx]
                # Find baseline
                base = np.mean(trace[stf.get_base_start():stf.get_base_end()])
                # Subtract baseline
                trace = trace - base
                # Find peak
                peak = np.min(trace[stf.get_peak_start():stf.get_peak_end()])
                peak_idx = (np.argmin(trace[stf.get_peak_start():stf.get_peak_end()]) + stf.get_peak_start())
                
                # Find forward point for half-width
                f_roll = peak_idx
                while trace[f_roll] < (0.5*peak):
                    if f_roll == 549:
                        print('Exceeded trace length looking for forward 50% value on index {0}'.format(idx))
                        flag = True
                        break
                    else:
                        f_roll += 1
                
                # Find backward point for half-width
                b_roll = peak_idx
                while trace[b_roll] < (0.5*peak):
                    if b_roll == 549:
                        print('Exceeded trace length looking for backward 50% value on index {0}'.format(idx))
                        flag = True
                        break
                    else:
                        b_roll -= 1
                
                #print('Peak Value: {0}\t Peak index: {1}'.format(peak, peak_idx))
                #print('Forward half: {0}\t Forward Index: {1}'.format(trace[f_roll], f_roll))
                #print('Backward half: {0}\t Backward Index: {1}'.format(trace[b_roll], b_roll))
                half_width = (f_roll - b_roll) * self.fs # Half width in ms
                
                # Find ninty-ten times
                ninty_idx = peak_idx
                while trace[ninty_idx] < (0.9*peak):
                    if ninty_idx == 549:
                        print('Exceeded trace length looking for 90% value on index {0}'.format(idx))
                        flag = True
                        break
                    else:
                        ninty_idx += 1
                ten_idx = ninty_idx
                while trace[ten_idx] < (0.2*peak):
                    if ten_idx == 549:
                        print('Exceeded trace length looking for 20% value on index {0}'.format(idx))
                        flag = True
                        break
                    else:
                        ten_idx += 1
                decay_time = (ten_idx - ninty_idx) * self.fs # Decay time in ms
                cluster_vars.append({'Peak': peak, 
                                    'Half Width': half_width, 
                                    'Decay Time': decay_time,
                                    'Flag': flag})
            else:
                cluster_vars.append({'Peak': None, 
                                    'Half Width': None, 
                                    'Decay Time': None,
                                    'Flag': False})
        #self.cluster_df = pd.DataFrame(cluster_vars)       In next line, not needed. Save in case
        self.mini_df = pd.merge(self.mini_df, pd.DataFrame(cluster_vars))
        #plt.hist(self.cluster_df['Peak'])      Not useful anymore
        #plt.show()                             Not needed
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(self.mini_df['Peak'], self.mini_df['Decay Time'])
        ax.set_xlabel("Peak")
        ax.set_ylabel("Decay Time (ms)")
        plt.axhline(5)
        plt.axvline(-50)
        plt.show()
    
    def classify(self, category=['peak', 'decay'], cutoff={'Peak': -50, 'Decay': 5}):
        # TODO: Fix mutable arguments. Set to None by default, then have function alter values if None
        # Create holding lists
        transmitter = []
        mini_spont = []
        # If classifying by peak is desired
        if 'peak' in category:
            # For each selected mini...
            for idx, value in enumerate(self.mini_df['select_mini']):
                if value:
                    # If the mini is greater than the cutoff, then it's spontaneous
                    if self.mini_df['Peak'] < cutoff['Peak']:
                        mini_spont.append('spontaneous')
                    # Otherwise, it's a mini
                    else:
                        mini_spont.append('mini')
                else:
                    mini_spont.append(None)
            self.mini_df['event_category'] = pd.Series(mini_spont)
        if 'decay' in category:
            for idx, value in enumerate(self.mini_df['select_mini']):
                if value:
                    if self.mini_df['Decay Time'] < cutoff['Decay']:
                        transmitter.append('glu')
                    else:
                        transmitter.append('gaba')
                else:
                    transmitter.append(None)
            self.mini_df['event_transmitter'] = pd.Series(transmitter)
    
                

    def cluster(self):
        """
        Takes selected indices from the displayed minis and returns minis in 
        separate windows clustered by Peak, Half-width, and 90-10% decay time
        """
        # Initialize variables for sorting
        clustering_vars = []
        
        # Main loop to find values for variables
        for idx, value in self.mini_df['select_mini']:
            if value:
                trace_vars = []
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
                while trace[f_roll] > (0.5*peak):
                    f_roll += 1
                
                # Find backward point for half-width
                b_roll = peak_idx
                while trace[b_roll] > (0.5*peak):
                    b_roll -= 1
                
                half_width = (f_roll - b_roll) * self.fs # Half width in ms
                trace_vars.append(half_width)
                
                # Find ninty-ten times
                ninty_idx = peak_idx
                while trace[ninty_idx] > (0.9*peak):
                    ninty_idx += 1
                ten_idx = peak_idx
                while trace[ten_idx] > (0.1*peak):
                    ten_idx += 1
                decay_time = (ten_idx - ninty_idx) * self.fs # Decay time in ms
                trace_vars.append(decay_time)
                clustering_vars.append(trace_vars)
        
        # Cluster with K-Means
        print("Fitting...")
        kmeans = KMeans(n_clusters=2, copy_x=True).fit(clustering_vars)
        list_0 = []
        list_1 = []
        for idx, values in enumerate(clustering_vars):
            if kmeans.labels_[idx] == 0:
                list_0.append(values)
            elif kmeans.labels_[idx] == 1:
                list_1.append(values)
            else:
                print("Cluster label is not 0 or 1 for trace {0}".format(idx))
        
        return list_0, list_1
    
        
        
    
