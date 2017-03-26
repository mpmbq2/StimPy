class SingleNeuron:
    """A class that will contain the information on a single neuron, such as which channel, what genotype,
        what transmitter it uses, and which files it is on"""

    def __init__(self, signals=None, transmitter=None, genotype=None):
        self.signals = signals
        self.transmitter = transmitter
        self.genotype = genotype
