from sqlalchemy import Integer, ForeignKey, Column, Table, String, Binary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
import stio
# import os
# import pandas as pd

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)


class NeuronPair(Base):
    """
    A class that will relate neurons to each other
    """
    # SqlAlchemy Initialization
    __tablename__ = 'pairs'

    id = Column(Integer, primary_key=True)
    neurons = relationship('SingleNeuron', back_populates='source_pair')
    abf_files = relationship('AbfFile', back_populates='source_pair')

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

        self.neurons = (SingleNeuron(Base,
                                     transmitter=self.transmitters[0],
                                     genotype=self.genotypes[0],
                                     signals=[cell.ch1_signal for cell in self.abf_files]),
                        SingleNeuron(Base,
                                     signals=[cell.ch2_signal for cell in self.abf_files],
                                     transmitter=self.transmitters[1],
                                     genotype=self.genotypes[1]))


class SingleNeuron(Base):
    """A class that will contain the information on a single neuron, such as which channel, what genotype,
        what transmitter it uses, and which files it is on"""
    # SqlAlchemy Initialization
    __tablename__ = 'neurons'

    id = Column(Integer, primary_key=True)
    transmitter = Column(String, nullable=True)
    genotype = Column(String, nullable=True)
    pair_id = Column(Integer, ForeignKey('pairs.id'))

    signals = relationship('AnalogData', back_populates='neuron')
    source_pair = relationship('NeuronPair', back_populates='neurons')

    def __init__(self, signals=None, transmitter=None, genotype=None):
        self.signals = signals
        self.transmitter = transmitter
        self.genotype = genotype


class AbfFile(Base):
    """A class that will contain the information on the files in the dataset, such as file names, types, recorded
    units, sampling rate, and recording date"""
    # SqlAlchemy Initialization
    __tablename__ = 'abf_files'

    id = Column(Integer, primary_key=True)
    pair_id = Column(Integer, ForeignKey('pairs.id'))
    name = Column(String, nullable=False)
    # type = Column(String, nullable=False)
    # channel1_units = Column(String, nullable=False)
    # channel2_units = Column(String, nullable=False)# Could go in a Channel object?
    sample_rate = Column(Integer, nullable=False)

    source_pair = relationship('NeuronPair', back_populates='abf_files')
    channels = relationship('AnalogData', back_populates='abf_file')

    def __init__(self, file_name, path_to_file):
        data_dict = stio.read_abf(os.path.join(path_to_file, file_name+'.abf'))
        self.name = data_dict['file_name']
        self.sample_rate = data_dict['sampling_rate']
        self.ch1_signal = AnalogData(signal=data_dict['channel1'],
                                     time=data_dict['time'],
                                     units=data_dict['channel1_units'])
        self.ch2_signal = AnalogData(signal=data_dict['channel2'],
                                     time=data_dict['time'],
                                     units=data_dict['channel2_units'])


class AnalogData(Base):
    # SqlAlchemy Initialization
    __tablename__ = 'analog_data'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('abf_files.id'))
    neuron_id = Column(Integer, ForeignKey('neurons.id'))
    units = Column(String, nullable=False)
    signal = Column(Binary, nullable=False)
    time = Column(Binary, nullable=False)

    abf_file = relationship('AbfFile', back_populates='channels')
    neuron = relationship('SingleNeuron', back_populates='signals')

    def __init__(self, signal=None, time=None, units=None):
        self.signal = signal
        self.time = time
        self.units = units


Base.metadata.create_all(engine)