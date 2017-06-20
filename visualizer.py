import numpy as np
import matplotlib.pyplot as plt
import PyQt5


# TODO: Figure out how to actually visualize best. PyQt5? Bokeh? Plotly?
# I want to be able to visualize the minis, the full trace it came from, variable zoom on both.
# I want to be able to select "Keep/Discard" (via checkbox?) and get rid of or keep that mini.

class MiniViz:
	'''MiniViz allows visualization of extracted minis. It takes a dictionary as an argument. The dictionary should have
	come from the MiniFile class' "extract()" method. MiniViz should allow visualization of peaks, half-widths, risetimes, decays, etc.
    This will undoubltedly be the largest part of this project.
	'''

    def __init__(self, data_dict):
        
        self.full_trace = data_dict['Data']
        self.minis = data_dict['Minis']
        self.mini_meta = data_dict['Metadata']

    def main_window(self):
        # TODO: Implement opening of main window
        # TODO: Implement visualization of minis
        # TODO: Implement deselection of minis for rejection
        # TODO: Implement metadata saving; this is good short term goal because many of these can be concatenated
        # TODO: Implement visualization of full_trace