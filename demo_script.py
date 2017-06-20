import StimPy as sp
import numpy as np


MiniFile = sp.file_open(file)

MiniFile.filter(Hz)

MiniFile.extract(epsc,ipsc,both)

MiniFile.view_minis()

MiniFile.save_minis(path)