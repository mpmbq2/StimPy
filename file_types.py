import numpy as np
from scipy import signal
from neo.io import AxonIO
from neo.core import Block
import pandas as pd
import StimPy.stio as stio
import StimPy as sp
import os



class MiniFile:
    '''This is a container object for miniPSC file analysis

    It works in the order Open -> Filter -> Extract -> View -> Save

    This object should be instantiated by the sp.file_open function

    It is a subclass of a Neo file object, so it has all the functionality of
        Neo objects, such as quantities, etc.

    The filter step takes frequency and type arguments. Type specifies the filter type

    Extract performs the mini detection algorithm, which finds events that exceed a user defined threshold
        using a user-defined function. By default this is the template match algo. Minis that fall outside of user-defined
        cutoffs are excluded.

    View opens a window that allows the user to cycle through the minis that were extracted.
        This allows the user the ability to manually accept/reject false positives.

    Finally, the Save method allows the user to store the metainformation, as well as a data file containing the mini traces,
        to a user-defined location

    '''

    def __init__(self, path):

        self.path = path.split('/')[:-1]
        self.filename = path.split('/')[-1]
        # reader = AxonIO(filename=path)
        # self.neo_data = reader.read()
        self.working_data = stio.read_neo(os.path.join(self.path, self.filename))

    def filter(self, freq=1000, type=None):
        '''This method filters the self.working_data attribute to produce more reliable detection.
        ::Params::
        freq = frequency of filtering. Default is 1 kHz.
        type = type of filter to use (Options: Bessel, Butterworth, Gaussian). Default us Bessel.

        ::Returns::
        True if executed fully
        '''

        # Create filter
        # TODO: Write actual filter function
        Wn = freq/10000
        order = 4
        b, a = signal.bessel(order, Wn)
        # Filter working data
        self.working_data['channel1'] = signal.filtfilt(b, a, self.working_data['channel1'])
        self.working_data['channel2'] = signal.filtfilt(b, a, self.working_data['channel2'])

        return True

    def extract(self, threshold=4, method='template_match', channel=1):
        '''This method extracts mPSCs from the self.working_data attribute.
        ::Params::
        threshold = This is the detection threshold for template correlation.
        method = The method to use for extracting minis.
        channel = The channel to be used for detection

        ::Returns::
        Dictionary: Keys are 'Data', 'Minis', and 'Metadata'
        '''

        # Extract minis
        # TODO: Write mini_detect function
        if method == 'template_match':
            minis, indices = sp.mini_detect(self.working_data, 'template_match')
        else:
            print('That detection method has not been implemented yet')

        # Compute metadata
        # TODO: Wite metadata extraction function that cotains code below
        extracted_meta = list()
        for idx, trace in enumerate(minis):
            props = sp.mini_properties(trace):
            props['index'] = indices[idx]
            extracted_meta.append(props)

        # Exclude the non-conformists
        # TODO: Write 'drop' functions
        # TODO: Make this function more efficient. Could use pandas map? Could use boolean indexing?
        for idx, mini in enumerate(extracted_meta):
            if mini['half-width'] > 25ms:
                drop mini
            elif mini['half-width'] < 4ms:
                drop mini
            if mini['amplitude'] < -10pA:
                drop mini
            if mini['risetime'] < 2ms:
                drop mini

        # Turn metadata into pandas dataframe
        extracted_meta = pd.DataFrame(extracted_meta)

        return {'Data': self.working_data, 'Minis': minis, 'Metadata': extracted_meta}

    def reset_file(self):
        self.working_data = stio.read_neo(self.path)
