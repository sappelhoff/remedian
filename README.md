[![Build Status](https://travis-ci.org/sappelhoff/remedian.svg?branch=master)](https://travis-ci.org/sappelhoff/remedian)

[![codecov](https://codecov.io/gh/sappelhoff/remedian/branch/master/graph/badge.svg)](https://codecov.io/gh/sappelhoff/remedian)

[![Documentation Status](https://readthedocs.org/projects/remedian/badge/?version=latest)](http://remedian.readthedocs.io/en/latest/?badge=latest)

# remedian
The  Remedian:  A  Robust  Averaging  Method  for  Large  Data  Sets - Python implementation

This algorithm is used to approximate the median of several data chunks if
these data chunks cannot (or should not) be loaded into memory at once.

Given a data chunk of size `obs_size`, and `t` data chunks overall, the
Remedian class sets up a number `k_arrs` of arrays of length `n_obs`.

The median of the `t` data chunks of size `obs_size` is then approximated
as follows: One data chunk after another is fed into the `n_obs` positions
of the first array. When the first array is full, its median is calculated
and stored in the first position of the second array. After this, the first
array is re-used to fill the second position of the second array, etc.
When the second array is full, the median of its values is stored in the
first position of the third array, and so on.

The final "Remedian" is the median of the last array, after all `t` data
chunks have been fed into the object.

References
----------
1.  P.J. Rousseeuw, G.W. Bassett Jr., "The remedian:
   A robust averaging method for large data sets", Journal
   of the American Statistical Association, vol. 85 (1990),
   pp. 97-104

2. M. Chao, G. Lin, "The asymptotic distributions of
  the remedians", Journal of Statistical Planning and
  Inference, vol. 37 (1993), pp. 1-11

3. Domenico Cantone, Micha Hofri, "Further analysis of
   the remedian algorithm", Theoretical Computer Science,
   vol. 495 (2013), pp. 1-16

# Installation

1. activate your python environment
2. `git clone https://www.github.com/sappelhoff/remedian`
3. `cd remedian`
4. `pip install -r requirements.txt`
5. `pip install -e .`
6. then you should be able to `from remedian.remedian import Remedian`

# Examples

```python
import matplotlib.pyplot as plt
import numpy as np
from remedian.remedian import Remedian

# We can have data of any shape ... e.g., 3D:
data_shape = (2,3,4)

# Now we have to decide how many data observations we want to load into
# memory at a time before computing a first intermediate median from it
n_obs = 100

# Pick some example number ... assume we have `t` arrays of shape `data_shape`
# that we want to summarize with Remedian
t = 500

# Initialize the object
r = Remedian(data_shape, n_obs, t)

# Feed it the data ... for now, we just generate the data randomly on the go
# ... also save the actual data for comparison with true median
res = []
for obs_i in range(t):
    obs = np.random.random(data_shape)
    r.add_obs(obs)
    res.append(obs)

# Now we have the Remedian in `r.remedian`
# Let's summarize the results
x = np.median(np.asarray(res).squeeze(), axis=0)
y = r.remedian
xydiff = x-y


# For colorbar scaling
vmin = np.min([x.min(), y.min(), xydiff.min()])
vmax = np.max([x.max(), y.max(), xydiff.max()])
vmin = -1*np.max(np.abs([vmin, vmax]))
vmax = np.max(np.abs([vmin, vmax]))

# Plot it
plt.close('all')

plt.subplot(131)
plt.imshow(x.reshape(1,-1), aspect='auto', cmap='bwr', vmin=vmin, vmax=vmax)
plt.axis('off')
plt.title('True median')

plt.subplot(132)
plt.imshow(y.reshape(1,-1), aspect='auto', cmap='bwr', vmin=vmin, vmax=vmax)
plt.axis('off')
plt.title('Remedian')

plt.subplot(133)
plt.imshow(xydiff.reshape(1,-1), aspect='auto', cmap='bwr', vmin=vmin, vmax=vmax)
plt.axis('off')
plt.colorbar()
plt.title('Difference')

```

![](example_pic.png?raw=true)

We can see some slight differences, but it's a good approximation.
