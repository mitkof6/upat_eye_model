#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def readMotionFile(filename):
    """Reads OpenSim .sto files.

    Parameters
    ----------
    filename: str
        absolute path to the .sto file

    Returns
    -------
    header: list of str
        the header of the .sto
    labels: list of str
        the labels of the columns
    data: list of lists
        an array of the data

    """

    if not os.path.exists(filename):
        print('file do not exists')

    file_id = open(filename, 'r')

    # read header
    next_line = file_id.readline()
    header = [next_line]
    nc = 0
    nr = 0
    while not 'endheader' in next_line:
        if 'datacolumns' in next_line:
            nc = int(next_line[next_line.index(' ') + 1:len(next_line)])
        elif 'datarows' in next_line:
            nr = int(next_line[next_line.index(' ') + 1:len(next_line)])
        elif 'nColumns' in next_line:
            nc = int(next_line[next_line.index('=') + 1:len(next_line)])
        elif 'nRows' in next_line:
            nr = int(next_line[next_line.index('=') + 1:len(next_line)])

        next_line = file_id.readline()
        header.append(next_line)

    # process column labels
    next_line = file_id.readline()
    if next_line.isspace() == True:
        next_line = file_id.readline()

    labels = next_line.split()

    # get data
    data = []
    for i in range(1, nr + 1):
        d = [float(x) for x in file_id.readline().split()]
        data.append(d)

    file_id.close()

    return header, labels, data


def index_containing_substring(list_str, pattern):
    """For a given list of strings finds the index of the element that contains the
    substring.

    Parameters
    ----------
    list_str: list of str

    pattern: str
         pattern


    Returns
    -------
    indices: list of int
         the indices where the pattern matches

    """
    indices = []
    for i, s in enumerate(list_str):
        if pattern in s:
            indices.append(i)

    return indices


def sigmoid(t, t0, A, B):
    """Implementation of smooth sigmoid function.

    Parameters
    ----------
    t: time to be evalutaed
    t0: delay
    A: magnitude
    B: slope

    Returns
    -------
    (y, y', y'')

    """
    return (A * (np.tanh(B * (t - t0)) + 1) / 2,
            A * B * (- np.tanh(B * (t - t0)) ** 2 + 1) / 2,
            - A * B ** 2 * (- np.tanh(B * (t - t0)) ** 2 + 1)
            * np.tanh(B * (t - t0)))


def smooth(x):
    from scipy.signal import medfilt, gauss_spline
    return medfilt(x, 1) # 7
    # return x


###############################################################################

# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_State_h15v0kv0.sto'
# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_Statesh0v15kv0.sto'
# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_Statesh-15v15kv0.sto'
# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_Statesh15v-15kv0002.sto'
state = 'UPAT_Eye_Model_Passive_Pulleys_v4_States_v4.sto'

header, labels, data = readMotionFile(state)

data = np.array(data)
time = np.array(data[:, 0])

# v4 is OpenSim v4.0 compatible thus the state are stored differently from
# OpenSim v3.3
if 'v4' in state:  # OpenSim v4.0
    coordinates = index_containing_substring(labels, 'value')[0:3]
    speeds = index_containing_substring(labels, 'speed')[0:3]
else:  # OpenSim v3.3
    coordinates = [1, 2, 3]
    speeds = [7, 8, 9]

activations = index_containing_substring(labels, 'activation')

theta = np.ceil(np.rad2deg(np.amax(data[:, coordinates])))
v = np.ceil(np.rad2deg(np.amax(data[:, speeds])))
t0 = 0.5
A = theta
B = 2 * v / theta
[x, v, a] = sigmoid(time, t0, A, B)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), sharey=False)
[
    ax[0].plot(time, np.rad2deg(data[:, coordinate]),
               label=labels[coordinate])
    for coordinate in coordinates
]
ax[0].plot(time, x, '--', label='desired')
ax[0].legend()
ax[0].set_xlabel('time $(s)$')
ax[0].set_ylabel('coordinates (deg)')

[
    ax[1].plot(time,
               np.rad2deg(data[:, speed]),
               label=labels[speed])
    for speed in speeds
]
ax[1].plot(time, v, '--', label='desired')
ax[1].legend()
ax[1].set_xlabel('time (s)')
ax[1].set_ylabel('velocities (deg / s)')

[
    ax[2].plot(
        time,
        smooth(data[:, activation]),
        label=labels[activation][2:-11],
        linestyle='-') for activation in activations
]
ax[2].legend()
ax[2].set_xlabel('time $(s)$')
ax[2].set_ylabel('muscle excitations')
ax[2].set_ylim([0, 1])

fig.tight_layout()
fig.savefig(state[:-4] + '.pdf', dpi=300)
