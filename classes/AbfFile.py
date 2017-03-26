import stio
from .AnalogData import AnalogData


class AbfFile:
    """A class that will contain the information on the files in the dataset, such as file names, types, recorded
    units, sampling rate, and recording date"""

    def __init__(self, file_name, path_to_file):
        data_dict = stio.read_abf(os.path.join(path_to_file, file_name + '.abf'))
        self.name = data_dict['file_name']
        self.sample_rate = data_dict['sampling_rate']
        self.channel1 = AnalogData(signal=data_dict['channel1'],
                                     time=data_dict['time'],
                                     units=data_dict['channel1_units'])
        self.channel2 = AnalogData(signal=data_dict['channel2'],
                                     time=data_dict['time'],
                                     units=data_dict['channel2_units'])