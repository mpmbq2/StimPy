import numpy as np
import pandas as pd
import neo
import bokeh

def main(path):
    '''Guided registration of stimulation artifact and PSC duration in Bokeh for automated analysis'''
    
    # Step 1: load metadata from DataSet object in <path>
    # Step 2: Find the 'baseline' file for each recorded pair
    # For Channel 1
        # Step 3: Prompt user to set latency cursors are start and end of artefact
            # raw_input('Please set latency cursors to encomapse the stimulation artefact. Type "c" to continue.')
        # Step 4: Prompt user to set peak cursors over the psc, and fit cursors from the peak to the baseline
        # Step 5: Store the [start] and [end] points of the artifact in an 'artifact' dict
        # Step 6: Store the [fit] values of the decay
        # Step 7: Repeat steps 3-6 for the stimulation in Channel 2 (remember to save the values into the other neuron)
    # For Channel 2
        # Step 8: Prompt user to set latency cursors are start and end of artefact
            # raw_input('Please set latency cursors to encomapse the stimulation artefact. Type "c" to continue.')
        # Step 9: Prompt user to set peak cursors over the psc, and fit cursors from the peak to the baseline
        # Step 10: Store the [start] and [end] points of the artefact in an 'artefact' dict
        # Step 11: Store the [fit] values of the decay
        # Step 12: Repeat steps 8-11 for the stimulation in Channel 1 (remember to save the values into the other neuron)
