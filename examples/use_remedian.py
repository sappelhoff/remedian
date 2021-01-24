"""
============
Use Remedian
============

.. currentmodule:: remedian

This example exists to demonstrate the basic usage of
:class:`remedian.Remedian`.

"""  # noqa: D205 D400

# Authors: Stefan Appelhoff <stefan.appelhoff@mailbox.org>
# License: MIT

###############################################################################
# First we import what we need for this example.
import matplotlib.pyplot as plt
import numpy as np
from remedian import Remedian

###############################################################################
# Now we make up some data SHAPE reflecting the shape of the data that we
# want to calculate the Remedian on.
# We can have data of any shape ... e.g., 3D:
data_shape = (2, 3, 4)

###############################################################################
# Now we have to decide how many data observations we want to load into
# memory at a time before computing a first intermediate median from it
n_obs = 100

###############################################################################
# Pick some example number ... assume we have ``t`` arrays of shape
# ``data_shape`` that we want to summarize with Remedian
t = 500

###############################################################################
# Initialize the object
r = Remedian(data_shape, n_obs, t)

###############################################################################
# Feed it the data ... for now, we just generate the data randomly on the go
# ... also save the actual data for comparison with true median
my_data = []
for obs_i in range(t):
    obs = np.random.random(data_shape)  # We just generate some random data
    r.add_obs(obs)
    my_data.append(obs)  # save random data for later (for example purposes)

###############################################################################
# Now we have the Remedian in ``r.remedian``
# Let's summarize the results
x = np.median(np.asarray(my_data).squeeze(), axis=0)  # the *true* median
y = r.remedian  # the *remedian*
xydiff = x-y


###############################################################################
# Now let's make a plot! We force the 3D data to 2D using
# :func:`numpy.reshape`.

# For colorbar scaling
vmax = np.max([np.abs(x), np.abs(y), np.abs(xydiff)])
vmin = -vmax


fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

for data_to_plot, ax, name in zip([x, y, xydiff], [ax1, ax2, ax3],
                                  ['True median', 'Remedian', 'Difference']):
    im = ax.imshow(data_to_plot.reshape(1, -1), aspect='auto', cmap='bwr',
                   vmin=vmin, vmax=vmax)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(name)

cbar = plt.colorbar(im, ax=ax)
