from . import *
import os
import pandas as pd


class Experiment:
    '''A class that will act as a container for all the data in an experiment'''
    pass


class DataSet(Experiment):
    '''A class that will contain a dataset, which is the data obtained from a single culture'''
    def __init__(self):
        self.meta = pd.DataFrame()

    def initialize(self, parent_directory):

        # Find all the metadata
        for root, _, files in os.walk(parent_directory):
            for f in files:
                if f == 'meta.csv':
                    df = pd.read_csv(os.path.join(root, f))
                    self.meta.append(df)

        # Initialize neurons with genotype info
        # Associate files with pairs
        # Anything else?


class NeuronPair:
    '''A class that will contain information on neuron pair, such as corresponding data files'''
    pass


class Neuron:
    '''A class that will contain the information on a single neuron, such as which channel, what genotype,
    what transmitter it uses, and extracted traces'''
    pass