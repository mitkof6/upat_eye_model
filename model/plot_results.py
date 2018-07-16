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


def smooth(x):
    from scipy.signal import medfilt, gauss_spline
    return medfilt(x, 1)
    # return x

###############################################################################


# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_State_h15v0kv0.sto'
# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_Statesh0v15kv0.sto'
# state = 'UPAT_Eye_Model_Passive_Pulleys_v3_Statesh-15v15kv0.sto'
state = 'UPAT_Eye_Model_Passive_Pulleys_v3_Statesh15v-15kv0002.sto'

header, labels, data = readMotionFile(state)

data = np.array(data)
time = np.array(data[:, 0])
coordinates = [1, 2, 3]
speeds = [7, 8, 9]
activations = index_containing_substring(labels, 'activation')

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), sharey=False)
[
    ax[0].plot(time, np.rad2deg(data[:, coordinate]),
               label=labels[coordinate][2:],)
    for coordinate in coordinates
]
ax[0].legend()
ax[0].set_xlabel('time $(s)$')
ax[0].set_ylabel('coordinates (deg)')
[
    ax[1].plot(time,
               np.rad2deg(data[:, speed]),
               label=labels[speed][2:])
    for speed in speeds
]
ax[1].legend()
ax[1].set_xlabel('time (s)')
ax[1].set_ylabel('speeds (deg / s)')

[
    ax[2].plot(
        time,
        smooth(data[:, activation]),
        label=labels[activation][2:-11],
        linestyle='-') for activation in activations
]
ax[2].legend()
ax[2].set_xlabel('time $(s)$')
ax[2].set_ylabel('activations')
ax[2].set_ylim([0, 1])

fig.tight_layout()
fig.savefig(state[:-4] + '.pdf', dpi=300)
