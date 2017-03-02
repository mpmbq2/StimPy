#from . import *
import os
import pandas as pd


class Experiment:
    '''A class that will tie DataSets together into in an experiment'''
    pass


class DataSet(Experiment):
    '''A class that will contain a dataset, which is the data obtained from a single culture'''
    def __init__(self, type=None):
        self.meta = pd.DataFrame()
        if type is None:
            self.type = input('Please input an experiment type (single, pair): ')
        else:
            self.type = type
        self.pair_locations = list()
        self.cells = list()

    def initialize(self, parent_directory):

        # Find all the metadata
        for root, _, files in os.walk(parent_directory):
            for f in files:
                if f == 'meta.csv':
                    df = pd.read_csv(os.path.join(root, f))
                    # create cell objects from meta
                    pairs = df['pair'].unique()
                    for p in pairs:
                        save_dir = os.path.join(root, 'pair_{0}'.format(p))
                        os.makedirs(save_dir)
                        self.pair_locations.append(save_dir)

                        data_files = df.file[df.pair == p]
                        # Read in the baseline .abf file with neo
                        # Convert to ndarray
                        # Separate the channels
                        # Save the channels as .npy files

                    #Last thing to do with meta.csv file is to append to master meta DataFrame
                    self.meta.append(df)




        # TODO: Initialize neurons with genotype info
        # TODO: Associate files with pairs
        # Anything else?


class NeuronPair:
    '''A class that will contain information on neuron pair, such as corresponding data files'''
    pass


class Neuron:
    '''A class that will contain the information on a single neuron, such as which channel, what genotype,
    what transmitter it uses, and extracted traces'''
    pass