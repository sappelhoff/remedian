# -*- coding: utf-8 -*-
"""Contains an implementation of Remedian."""

# Author: Stefan Appelhoff <stefan.appelhoff@mailbox.org>
# License: MIT

import numpy as np


class Remedian():
    """Remedian object for a robust averaging method for large data sets.

    Implementation of the Remedian algorith, see [1], [2], [3] for references.

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


    Parameters
    ----------
    obs_size : ndarray
        The shape of each data chunk (=observation) to be fed into the Remedian
        object.

    n_obs : int
        The number of observations to be stored within each array.
        If `n_obs` >= `t`, Remedian will equal the median. Higher values of
        `n_obs` will lead to a better approximation of the median but will
        require more memory.

    t : int
        The total number of observations from which a median should be
        approximated.

    Attributes
    ----------
    obs_count : int
        Counter of number of observations that have already been given
        to the Remedian object.

    remedian : None | ndarray, shape(obs_size)
        The calculated remedian of the same shape as the input data.
        Will be None until all observations `n_obs` have been fed into
        the object using the add_obs method.

    References
    ----------
    .. [1] P.J. Rousseeuw, G.W. Bassett Jr., "The remedian:
       A robust averaging method for large data sets", Journal
       of the American Statistical Association, vol. 85 (1990),
       pp. 97-104

    .. [2]M. Chao, G. Lin, "The asymptotic distributions of
      the remedians", Journal of Statistical Planning and
      Inference, vol. 37 (1993), pp. 1-11

    .. [3] Domenico Cantone, Micha Hofri, "Further analysis of
       the remedian algorithm", Theoretical Computer Science,
       vol. 495 (2013), pp. 1-16

    """

    def __init__(self, obs_size, n_obs, t):
        """Initialize the Remedian object.

        See class docstring for more thorough information.

        Parameters
        ----------
        obs_size : ndarray
            size of the observations

        n_obs : int
            observations per array

        t : int
            number of total observations

        """
        # n_obs of <= 1 does not make sense
        try:
            assert n_obs > 1
        except AssertionError:
            raise ValueError('`n_obs` of <= 1 does not make sense.')

        self.obs_size = list(obs_size)
        self.n_obs = n_obs
        self.t = t

        # Calculate the number of arrays needed and their sizes
        self.k_arrs = self._calc_k_arrs()
        self.k_arr_sizes = self._calc_k_arr_sizes()

        # Initialize the arrays
        self.arrs = [np.zeros(self.obs_size+[s]) for s in self.k_arr_sizes]

        # counter for observations within each array
        self.obs_idx_counter = [0 for arr in range(self.k_arrs)]

        # Modulos of observations to assign to correct array later
        self.modulos = [self.n_obs**i for i in range(1, 1+self.k_arrs)]

        # Counter of received observations
        self.obs_count = 0

        # Set the median value to None until we have it
        self.remedian = None

    def _calc_k_arrs(self):
        """Calculate number of arrays to acommodate the observations."""
        tmp = self.n_obs
        k_arrs = 1
        while tmp <= self.t:
            tmp *= self.n_obs
            k_arrs += 1
        return k_arrs

    def _calc_k_arr_sizes(self):
        """Calculate the size of each array to accomodate the observations."""
        k_arr_sizes = [self.n_obs for i in range(self.k_arrs)]
        k_arr_sizes[-1] = int(np.ceil(self.t / (self.n_obs**(self.k_arrs-1))))
        return k_arr_sizes

    def add_obs(self, obs):
        """Add an observation to the Remedian.

        Parameters
        ----------
        obs : ndarray, shape(obs_size)

        """
        # We only work if:
        # ... we get an observation of correct size
        # ... we have not yet received all observations already
        try:
            assert list(obs.shape) == self.obs_size
        except AssertionError:
            print('Expected observation of size {}'.format(self.obs_size))
            print('... but received: {}'.format(list(obs.shape)))
            return None
        try:
            assert self.obs_count <= self.t-1
        except AssertionError:
            print('\nAlready collected '
                  '{} observations out of t={}'.format(self.obs_count, self.t))
            print('The remedian is {}'.format(self.remedian))
            return None

        # We accept a new observation
        self.obs_count += 1

        # Add the data to the first array
        # and increment the counter for the next data
        obs_idx = self.obs_idx_counter[0]
        self.arrs[0][..., obs_idx] = obs
        self.obs_idx_counter[0] += 1

        # We can notice whenever an array is full using modulo operations
        # on the observation counter self.obs_count.
        # When an array is full, calculate the median and put the result
        # into the next array. Then reset the counters and start filling
        # previous arrays again
        for arr_i, mod in enumerate(self.modulos):
            if self.obs_count % mod == 0:
                data = self.arrs[arr_i]
                m_tmp = np.median(data, axis=-1, overwrite_input=True)
                self.arrs[arr_i+1][..., self.obs_idx_counter[arr_i+1]] = m_tmp
                self.obs_idx_counter[arr_i+1] += 1
                self.obs_idx_counter[arr_i] = 0

        # If all observations have been received,
        # calculate the median of the last array.
        # This is the robust approximation of the median
        if self.obs_count == self.t:
            self.remedian = np.median(self.arrs[-1], axis=-1,
                                      overwrite_input=True)
