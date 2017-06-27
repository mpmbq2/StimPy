import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/home/matt/PycharmProjects')
from StimPy import minis
import numpy as np
import matplotlib.pyplot as plt

#file_path = '/home/matt/Data/patch_data/dnm1_ftfl/cortical/170425_170428/\
#170425/2017_04_25_0013.abf'
file_path = '/home/matt/Data/patch_data/dyn1/170222/170221_0046.abf'

recording = minis.MiniRec(file_path)

recording.filter(ftype='bessel', freq=750.0)

events = recording.detect()
