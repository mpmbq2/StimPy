import pandas as pd
import os


class DataSet:
    '''A class that will contain a dataset, which is the data obtained from a single culture'''

    def __init__(self, type=None):
        self.meta = pd.DataFrame()
        if type is None:
            self.type = input('Please input an experiment type (single, pair): ')
        else:
            self.type = type
        self.cells = list()
        self.pair_locations = list()

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
                        # TODO: Read in the baseline .abf file with neo (and check for possible header info)
                        # TODO: Convert to ndarray
                        # TODO: Separate the channels
                        # TODO: Save the channels as .npy files

                    # Last thing to do with meta.csv file is to append to master meta DataFrame
                    self.meta.append(df)

    def load_database(self, db_path):
        pass

    def append_data(self, path):
        pass

    def annotate_files(self):
        pass

    def plot(self, kind=None, filters=None):
        pass