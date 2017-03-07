import pandas as pd
import os
from classes import NeuronPair
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

    def new(self, parent_directory):

        # Find all the metadata
        for root, _, files in os.walk(parent_directory):
            for f in files:
                if f == 'meta.csv':
                    df = pd.read_csv(os.path.join(root, f))
                    sub_df = self._parse_meta(df)
                    pair = NeuronPair()



                    #
                    # # create cell objects from meta
                    # pairs = df['pair'].unique()
                    # for p in pairs:
                    #
                    #
                    #
                    #
                    #     data_files = df.file[df.pair == p]
                    #
                    # # Last thing to do with meta.csv file is to append to master meta DataFrame
                    # self.meta.append(df)

    def _parse_meta(self, df_in):
        df_out = df_in[(df_in.pair == p for p in df_in['pair'].unique())]
        yield df_out

    def load_database(self, db_path):
        pass

    def append_data(self, path):
        pass

    def annotate_files(self):
        pass

    def plot(self, kind=None, filters=None):
        pass