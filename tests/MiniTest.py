import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/home/matt/PycharmProjects')
from StimPy import minis
import numpy as np
import matplotlib.pyplot as plt
from peakutils.baseline import baseline

file_path = '/home/matt/Data/patch_data/dnm1_ftfl/cortical/170425_170428/\
170425/2017_04_25_0044.abf'
#file_path = '/home/matt/Data/patch_data/dyn1/170222/170221_0046.abf'

recording = minis.MiniRec(file_path)

recording.filter(ftype='bessel', freq=1000.0)

events = recording.detect(method='derivative', threshold=25)
#events = recording.detect(template_type='ipsc')
baselined_events = list()
for e in events:
    base = baseline(-e, deg=2)
    baselined_events.append((e+base))
events = np.array(baselined_events)
plt.plot(events.T, alpha=0.1)
plt.plot(np.mean(events, axis=0))
plt.show()
