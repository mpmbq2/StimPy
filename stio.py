from neo.io import AxonIO
import numpy as np


def abf_import(path):

    # Read abf file with neo
    reader = AxonIO(filename=path)
    block = reader.read()

    # Extract analog signals
    if len(block[0].segments[0].analogsignals) == 1:
        channel1 = np.empty(block[0].segments[0].analogsignals[0].T.shape)
        channel1_units = block[0].segments[0].analogsignals[0].units
        channel2 = None
        channel2_units = None
        t = block[0].segments[0].analogsignals[0].times.magnitude
        for idx, seg in enumerate(block[0].segments):
            channel1[idx] = seg.analogsignals[0].T
    #
    #     return {'file_name': block.file_origin,
    #             'recording_date': block.rec_datetime,
    #             'time': t,
    #             'channel1': channel1,

    elif len(block[0].segments[0].analogsignals) == 2:
        channel1 = np.empty(block[0].segments[0].analogsignals[0].shape)
        channel1_units = block[0].segments[0].analogsignals[0].units
        channel2 = np.empty(block[0].segments[0].analogsignals[0].shape)
        channel2_units = block[0].segments[0].analogsignals[0].units
        t = block[0].segments[0].analogsignals[0].times.magnitude
        for idx, seg in enumerate(block[0].segments):
            channel1[idx] = seg.analogsignals[0].T
            channel2[idx] = seg.analogsignals[1].T

    else:
        raise Exception('File {0} either has too many channels, or no channels.'.format(path))

    return {'file_name': block.file_origin,
            'recording_date': block.rec_datetime,
            'sampling_rate': block[0].segments[0].analogsignals[0].sampling_rate,
            'time': t,
            'channel1': channel1,
            'channel1_units': channel1_units,
            'channel2': channel2,
            'channel2_units': channel2_units}
