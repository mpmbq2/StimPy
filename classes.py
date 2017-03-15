import os
import stio


# import os
# import pandas as pd

class NeuronPair:
    """
    A class that will relate neurons to each other
    """

    def __init__(self, file_list=None, genotypes=None, transmitters=None, file_path=None):
        # if not isinstance(file_list, (list, tuple)):
        #     print('The file_list argument must be a list or tuple')
        #     self.abf_files = None
        # else:
        self.abf_files = [AbfFile(items, file_path) for items in file_list]
        # TODO: Read and parse files to have signals to pass to SingleNeuron class
        if not isinstance(genotypes, (list, tuple)):
            print('The genotype argument must be a list or tuple for both cells in the pair')
        self.genotypes = genotypes

        if not isinstance(transmitters, (list, tuple)):
            print('The transmitter argument must be a list or tuple for both cells in the pair')
        self.transmitters = transmitters

        self.neurons = (SingleNeuron(transmitter=self.transmitters[0],
                                     genotype=self.genotypes[0],
                                     signals=[cell.ch1_signal for cell in self.abf_files]),
                        SingleNeuron(signals=[cell.ch2_signal for cell in self.abf_files],
                                     transmitter=self.transmitters[1],
                                     genotype=self.genotypes[1]))


class SingleNeuron:
    """A class that will contain the information on a single neuron, such as which channel, what genotype,
        what transmitter it uses, and which files it is on"""

    def __init__(self, signals=None, transmitter=None, genotype=None):
        self.signals = signals
        self.transmitter = transmitter
        self.genotype = genotype


class AbfFile:
    """A class that will contain the information on the files in the dataset, such as file names, types, recorded
    units, sampling rate, and recording date"""

    def __init__(self, file_name, path_to_file):
        data_dict = stio.read_abf(os.path.join(path_to_file, file_name + '.abf'))
        self.name = data_dict['file_name']
        self.sample_rate = data_dict['sampling_rate']
        self.ch1_signal = AnalogData(signal=data_dict['channel1'],
                                     time=data_dict['time'],
                                     units=data_dict['channel1_units'])
        self.ch2_signal = AnalogData(signal=data_dict['channel2'],
                                     time=data_dict['time'],
                                     units=data_dict['channel2_units'])


class AnalogData:
    def __init__(self, signal=None, time=None, units=None):
        self.signal = signal
        self.time = time
        self.units = units
