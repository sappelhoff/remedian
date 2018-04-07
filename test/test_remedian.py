"""Tests for the Remedian class."""

from remedian.remedian import Remedian
import numpy as np


def test_initial_values():
    """Test the initial values."""
    random_shape = np.random.randint(1, 100, np.random.randint(1, 5, 1)[0])
    obs_size = np.random.random((random_shape)).shape
    n_obs = np.random.randint(0, 100, 1)[0]
    t = np.random.randint(0, 100, 1)[0]
    r = Remedian(obs_size, n_obs, t)
    assert r.obs_size == list(obs_size)
    assert r.n_obs == n_obs
    assert r.t == t
