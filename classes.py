import os
import pandas as pd
from sqlalchemy import Integer, ForeignKey, Column, Table, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

neuron_file_association = Table('neuron_file_association', Base.metadata,
                                Column('neuron_id', Integer, ForeignKey('neuron.id')),
                                Column('file_id', Integer, ForeignKey('abf_file.id')))

Pair
    - ID (1)

File
    - ID
    - Pair_ID (1)
    - Name
    - Type
    - Channel1 (neuron_id = 1)
    - Channel2 (neuron_id = 2)

Data
    - ID
    - File
    - (int) channel_number
    - data_array

Neuron
    - ID
    - genome
    - trans
    - PSC Name
    - Pair
    -File

neurons = []
for neuron, in session.query(Neuron).join(File, on(channel1, Neuron.id).filter(genome = 'potato'):
    neurons.push(neuron)



File -> X Segments  ->  Channel vector
                    ->  Channel vector

File    ->  Channel array
        ->  Channel array

Pair    ->  Neuron
        ->  Neuron

SELECT data_array
FROM Channel
    Join Neuron ON Neuron.id = Channel.Neuron_id
    Join File ON File.id = Channel.file_id
WHERE
    Neuron.genome = 'gaba'
    AND neuron.trans = 'potato'




Segment
    - ID
    -file_id
    -order
    - mark
    - max

Neuron
    - ID
    - Genome
    - Trans
    - File_1 -> AT -> File

SELECT *
FROM PSC
    JOIN Neuron ON Neuron.ID = PSC.Neuron_ID
    JOIN Pair ON Pair.neuron = neuron.id
    JOIN File ON Pair.id = File.pair_id
WHERE Neuron.trans = 'gaba'\
    AND File.Type = 'Dyno';

(Pair.channel_1.type =='gaba' && Pair.channel.type == 'glu') || (Pair.channel[0].type =='glu' && Pair.channel[1].type == 'gaba')

Test.Neuron_Channel[0]

class Pair(Base):
    '''A class that will relate neurons to each other'''
    # SqlAlchemy Initialization
    __tablename__ = 'pairs'

    id = Column(Integer, primary_key=True)
    neuron_1 = relationship('Neuron')
    neuron_2 = relationship('Neuron')


class Neuron(Base):
    '''A class that will contain the information on a single neuron, such as which channel, what genotype,
        what transmitter it uses, and which files it is on'''
    # SqlAlchemy Initialization
    __tablename__ = 'neurons'

    id = Column(Integer, primary_key=True)
    abf_files = relationship('AbfFile', secondary='neuron_file_association', back_populates='neurons')
    transmitter = Column(String, nullable=True)
    genotype = Column(String, nullable=False)
    # pair_id = Column(Integer, ForeignKey('pairs.id'))


class AbfFile(Base):
    '''A class that will contain the information on the files in the dataset, such as file names, types, recorded
    units, sampling rate, and recording date'''
    # SqlAlchemy Initialization
    __tablename__ = 'abf_files'

    id = Column(Integer, primary_key=True)
    pair_id = relationship('Pair')
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    # channel1_units = Column(String, nullable=False)
    # channel2_units = Column(String, nullable=False)# Could go in a Channel object?
    sample_rate = Column(Integer, nullable=False)
    neurons = relationship('Neuron', secondary='neuron_file_association', back_populates='abf_files')
    # channels = Column(Integer, nullable=False)

class Channel(Base):
    # SqlAlchemy Initialization
    __tablename__ = 'abf_files'

    id = Column(Integer, primary_key=True)
    file_id = relationship('Segment')

