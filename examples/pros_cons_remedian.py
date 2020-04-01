"""
=========================
Pros and Cons of Remedian
=========================

In this example we test :class:`remedian.Remedian` against :func:`numpy.median`
in terms of three parameters:

- computation time
- mean squared error compared to true median
- memory needed for computation

"""

# Authors: Stefan Appelhoff <stefan.appelhoff@mailbox.org>
# License: MIT

###############################################################################
# First we import what we need for this example.
from timeit import default_timer as timer

import matplotlib.pyplot as plt
import numpy as np
from remedian import Remedian

###############################################################################
# We start by generating two datasets that we want to compute the median of
# along the last dimension (or approximate the median via Remedian).

n = 500  # this is the dimension across which we want to compute the median
data_shape = (50, 50, n)
data_unif = np.random.random(data_shape)
data_norm = np.random.randn(*data_shape)

###############################################################################
# Now let's measure three parameters: The time it takes to compute the
# Remedian, the memory it needs to keep the data loaded, and the mean
# squared error compared to the *true* median.
#
# We will do this for different Remedian ``n_obs`` parameters. ``n_obs``
# determines how many intermediate medians are taken to approximate the median.
# Low ``n_obs`` means little memory required, but also a more noisy estimation
# of the median. High ``n_obs`` or ``n_obs`` equal to ``n`` equals the *true*
# median.

datas = [data_unif, data_norm]
n_obses = range(2, n+1)  # n_obs cannot be 1 or smaller

# The three parameters we want to collect data on
memory_needed = np.zeros((len(datas), len(n_obses)))
compute_times = np.zeros((len(datas), len(n_obses)))
mses = np.zeros((len(datas), len(n_obses)))

# Start collecting the data across our two generated datasets
for idata, data in enumerate(datas):

    # calculate true median for this dataset
    median = np.median(data, axis=-1)

    # Calculate the Remedian for this dataset, given differen ``n_obs`` params
    for in_obs, n_obs in enumerate(n_obses):

        start = timer()
        # New Remedian object
        rem = Remedian(data_shape[:-1], n_obs, n)

        # calculate the remedian
        for data_idx in range(n):
            rem.add_obs(data[..., data_idx])

        approx_median = rem.remedian
        end = timer()

        # Time elapsed in seconds
        compute_times[idata, in_obs] = end - start

        # Memory needed in bytes
        memory_needed[idata, in_obs] = n_obs * (data[..., data_idx].size *
                                                data[..., data_idx].itemsize)

        # mean square error from true median
        mses[idata, in_obs] = np.mean((approx_median-median)**2)

###############################################################################
# We ran our data collection for ``n_obs`` parameters up to ``n``, which
# equals the median as given by :func:`np.median`. Let's plot the results.

fig, axs = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True)

names = ['memory_needed_[bytes]', 'computation_time_[s]', 'mean_squared_error']
results = [memory_needed, compute_times, mses]
for ax, name, result in zip(axs, names, results):

    ax.plot(n_obses, result[0, ...], label='data_unif')
    ax.plot(n_obses, result[1, ...], label='data_norm')
    ax.axvline(n_obses[-1], color='black', linestyle='--',
               label='*true* median')

    ax.set_ylabel(name)
    if name.startswith('memory'):
        ax.legend()

ax.set_xlabel('`n_obs` parameter')
fig.tight_layout()

###############################################################################
# In summary:
#
# - Remedian needs less memory than the *true* median
# - Remedian's ``n_obs`` parameter can be set in a "good" or "bad" way
#   regarding the mean squared error compared to the *true* median
# - Remedian's timing seems to be relatively unaffected by the ``n_obs``
#   parameter, and close to the timing of the *true* median.
