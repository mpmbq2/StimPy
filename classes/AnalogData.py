import numpy as np


class AnalogData:
    def __init__(self, signal=None, time=None, units=None):
        self.signal = signal
        self.time = time
        self.units = units
