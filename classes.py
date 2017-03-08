import os
import pandas as pd
from sqlalchemy import Integer, ForeignKey, Column, Table, String, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from stio import read_abf

Base = declarative_base()

class NeuronPair(Base):
    '''A class that will relate neurons to each other'''
    # SqlAlchemy Initialization
    __tablename__ = 'pairs'

    id = Column(Integer, primary_key=True)
    neurons = relationship('Neuron', back_populates='pair')
    abf_files = relationship('AbfFiles', back_populates='pair')

    def __init__(self, file_list=None, genotype=None, transmitter=None):
        if not isinstance(file_list, (list, tuple)):
            print('The file_list argument must be a list or tuple')
            self.abf_files = None
        else:
            self.abf_files = file_list
            # TODO: Read and parse files to have signals to pass to SingleNeuron class
            # TODO: Need to figure out where to create AbfFile classes
            # TODO: Need to figure out where to create Signal classes
        if not isinstance(genotype, (list, tuple)):
            print('The genotype argument must be a list or tuple for both cells in the pair')

        if not isinstance(transmitter, (list, tuple)):
            print('The transmitter argument must be a list or tuple for both cells in the pair')

        read_abf()

        self.neurons = (SingleNeuron(Base, signals[0], transmitter[0], genotype[0]),
                        SingleNeuron(Base, signals[1], transmitter[1], genotype[1]))


class SingleNeuron(Base, genotype=None, transmitter=None, signal=None, units=None):
    '''A class that will contain the information on a single neuron, such as which channel, what genotype,
        what transmitter it uses, and which files it is on'''
    # SqlAlchemy Initialization
    __tablename__ = 'neurons'

    id = Column(Integer, primary_key=True)
    transmitter = Column(String, nullable=True)
    genotype = Column(String, nullable=False)
    pair_id = Column(Integer, ForeignKey('pairs.id'))
    signal = relationship('AnalogData', back_populates='neuron')

    def __init__(self, signal, transmitter, genotype):
        pass


class AbfFile(Base):
    '''A class that will contain the information on the files in the dataset, such as file names, types, recorded
    units, sampling rate, and recording date'''
    # SqlAlchemy Initialization
    __tablename__ = 'abf_files'

    id = Column(Integer, primary_key=True)
    pair_id = Column(Integer, ForeignKey('pairs.id'))
    pair = relationship("Pair", back_populates="pair")
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    # channel1_units = Column(String, nullable=False)
    # channel2_units = Column(String, nullable=False)# Could go in a Channel object?
    sample_rate = Column(Integer, nullable=False)
    signal = relationship('AnalogData', back_populates='abf_file')
    # channels = Column(Integer, nullable=False)

class AnalogData(Base):
    # SqlAlchemy Initialization
    __tablename__ = 'analog_data'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('abf_files.id'))
    neuron_id = Column(Integer, ForeignKey('neurons.id'))
    units = Column(String, nullable=False)
    signal = Column(Binary, nullable=False)
    time = Column(Binary, nullable=False)

