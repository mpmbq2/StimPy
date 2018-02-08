from neo.io import AxonIO
import numpy as np
from .classes import AbfFile
#from .classes import MiniFile
from .classes import AnalogData


def read_neo(path):

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

        channel1 = np.empty((len(block[0].segments), block[0].segments[0].analogsignals[0].size))
        channel1_units = block[0].segments[0].analogsignals[0].units
        channel1_sampling = block[0].segments[0].analogsignals[0].sampling_rate
        channel2 = np.empty((len(block[0].segments), block[0].segments[0].analogsignals[1].size))
        channel2_units = block[0].segments[0].analogsignals[1].units
        channel2_sampling = block[0].segments[0].analogsignals[1].sampling_rate
        t = block[0].segments[0].analogsignals[0].times.magnitude
        for idx, seg in enumerate(block[0].segments):
            channel1[idx] = seg.analogsignals[0].T
            channel2[idx] = seg.analogsignals[1].T
            #channel1[idx] = seg.analogsignals[0]
            #channel2[idx] = seg.analogsignals[1]
        channel_1 = AnalogData(
            signal=channel1,
            time=t,
            units=channel1_units,
            sampling_rate=channel1_sampling
            )
        channel_2 = AnalogData(
            signal=channel2,
            time=t,
            units=channel2_units,
            sampling_rate=channel2_sampling)

    else:
        raise Exception('File {0} either has too many channels, or no channels.'.format(path))

    return AbfFile(
        [channel_1, channel_2],
        file_name=block[0].file_origin,
        date=block[0].rec_datetime)


# def read_mini(path):
#
#     # Read abf file with neo
#     reader = AxonIO(filename=path)
#     block = reader.read()
#
#     # Extract analog signals
#     if len(block[0].segments[0].analogsignals) == 1:
#         channel1 = np.empty(block[0].segments[0].analogsignals[0].T.shape)
#         channel1_units = block[0].segments[0].analogsignals[0].units
#         channel2 = None
#         channel2_units = None
#         t = block[0].segments[0].analogsignals[0].times.magnitude
#         for idx, seg in enumerate(block[0].segments):
#             channel1[idx] = seg.analogsignals[0].T
#     #
#     #     return {'file_name': block.file_origin,
#     #             'recording_date': block.rec_datetime,
#     #             'time': t,
#     #             'channel1': channel1,
#
#     elif len(block[0].segments[0].analogsignals) == 2:
#
#         channel1 = np.empty((len(block[0].segments), block[0].segments[0].analogsignals[0].size))
#         channel1_units = block[0].segments[0].analogsignals[0].units
#         channel1_sampling = block[0].segments[0].analogsignals[0].sampling_rate
#         channel2 = np.empty((len(block[0].segments), block[0].segments[0].analogsignals[1].size))
#         channel2_units = block[0].segments[0].analogsignals[1].units
#         channel2_sampling = block[0].segments[0].analogsignals[1].sampling_rate
#         t = block[0].segments[0].analogsignals[0].times.magnitude
#         for idx, seg in enumerate(block[0].segments):
#             channel1[idx] = seg.analogsignals[0].T
#             channel2[idx] = seg.analogsignals[1].T
#             #channel1[idx] = seg.analogsignals[0]
#             #channel2[idx] = seg.analogsignals[1]
#         channel_1 = AnalogData(
#             signal=channel1,
#             time=t,
#             units=channel1_units,
#             sampling_rate=channel1_sampling
#             )
#         channel_2 = AnalogData(
#             signal=channel2,
#             time=t,
#             units=channel2_units,
#             sampling_rate=channel2_sampling)
#
#     else:
#         raise Exception('File {0} either has too many channels, or no channels.'.format(path))
#
#     return MiniFile(
#         [channel_1, channel_2],
#         file_name=block[0].file_origin,
#         date=block[0].rec_datetime)
