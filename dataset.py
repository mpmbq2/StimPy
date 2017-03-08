import pandas as pd
import os
from classes import Base, NeuronPair, SingleNeuron
from sqlalchemy.ext.declarative import declarative_base
from stio import read_abf


class DataSet:
    '''A class that will contain a dataset, which is the data obtained from a single culture'''

    def __init__(self, type=None):
        self.meta = pd.DataFrame()
        if type is None:
            self.type = input('Please input an experiment type (single, pair): ')
        else:
            self.type = type
        self.cells = list()
        self.pairs = list()
        self.abf_files = list()

    def new_db(self, parent_directory):


        # Find all the metadata
        for root, _, files in os.walk(parent_directory):
            for f in files:
                if f == 'meta.csv':
                    df = pd.read_csv(os.path.join(root, f))
                    for sub_df in self._parse_meta(df):
                        self._create_pairs(sub_df, Base)



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

    def _create_pairs(self, dataframe, path=None):

        for idx, abf_files in enumerate(dataframe.files):
            data = read_abf(os.path.join(path, abf_files))

            neuron1 = SingleNeuron(Base,
                                   genotype=data.genotype[idx],
                                   signal=data['channel1'],
                                   units=data['channel1_units'],
                                   time=data['time'])
            neuron2 = SingleNeuron(Base,
                                   genotype=data.genotype[idx],
                                   signal=data['channel2'],
                                   units=data['channel2_units'],
                                   time = data['time'])
            pair = NeuronPair(Base,
                              file_list=dataframe['files'],
                              genotype=dataframe.genotype)

    def load_database(self, db_path):
        pass

    def append_data(self, path):
        pass

    def annotate_files(self):
        pass

    def plot(self, kind=None, filters=None):
        pass