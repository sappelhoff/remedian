"""Tests for the Remedian class."""

from nose.tools import assert_raises

import numpy as np

from remedian.remedian import Remedian


def test_wrong_input():
    """Test behavior if wrong input is given at initialization."""
    # No input
    try:
        Remedian()
    except TypeError:
        pass

    # obs_size is not a shape (tuple)
    try:
        Remedian(1, 2, 3)
    except TypeError:
        pass

    # Normal call of Remedian without error
    assert Remedian((1,), 2, 3)

    # Observations <= 1 are impossible
    for n_obs in range(-1, 2):
        try:
            print(n_obs)
            Remedian((1,), n_obs, 3)
        except ValueError:
            pass

    # Negative number of input arrays are impossible
    try:
        Remedian((1,), 2, -3)
    except ValueError:
        pass


def test_initial_values():
    """Test the initial values."""
    random_shape = np.random.randint(1, 100, np.random.randint(1, 5, 1)[0])
    obs_size = np.random.random((random_shape)).shape
    n_obs = np.random.randint(1, 100, 1)[0]
    t = np.random.randint(1, 100, 1)[0]
    r = Remedian(obs_size, n_obs, t)
    assert r.obs_size == list(obs_size)
    assert r.n_obs == n_obs
    assert r.t == t


def test_calc_remedian():
    """Test whether the calculation of a remedian works."""
    random_shape = np.random.randint(1, 3, np.random.randint(1, 3, 1)[0])
    obs_size = np.random.random((random_shape)).shape
    n_obs = np.random.randint(1, 50, 1)[0]
    t = np.random.randint(1, 50, 1)[0]
    r = Remedian(obs_size, n_obs, t)
    assert r.remedian is None
    for i in range(t):
        obs = np.random.random(obs_size)
        r.add_obs(obs)
    assert isinstance(r.remedian, np.ndarray)
    assert r.remedian.shape == obs_size


def test_too_many_obs():
    """Test behavior if more obs are given than t specifies."""
    obs_size = (2, 5)
    n_obs = 3
    t = 10
    r = Remedian(obs_size, n_obs, t)
    for i in range(t):
        obs = np.random.random(obs_size)
        r.add_obs(obs)

    # One more should be one too much
    assert_raises(AssertionError, r.add_obs(np.random.random(obs_size)))


def test_wrong_obs_size():
    """Test behavior if obs_size is unexpected at call to add_obs."""
    random_shape = np.random.randint(1, 3, np.random.randint(1, 3, 1)[0])
    obs_size = np.random.random((random_shape)).shape
    n_obs = np.random.randint(1, 50, 1)[0]
    t = np.random.randint(1, 50, 1)[0]
    r = Remedian(obs_size, n_obs, t)

    # We give a wrong obs_size
    wrong_obs_size = tuple(np.asarray(obs_size)+1)
    assert_raises(AssertionError, r.add_obs(np.random.random(wrong_obs_size)))


def test_true_median():
    """Test that Remedian==median if n_obs==t or n_obs>t."""
    obs_size = (2, 5)
    t = 10

    # Test for n_obs == t
    n_obs = t
    r = Remedian(obs_size, n_obs, t)

    res = []
    for i in range(t):
        obs = np.random.random(obs_size)
        r.add_obs(obs)
        res.append(obs)

    true_median = np.median(np.asarray(res).squeeze(), axis=0)
    remedian_median = r.remedian.squeeze()
    assert true_median.shape == remedian_median.shape
    np.testing.assert_array_equal(true_median, remedian_median)

    # Now test for n_obs > t
    n_obs = t + np.random.randint(1, 5, 1)[0]
    r = Remedian(obs_size, n_obs, t)

    res = []
    for i in range(t):
        obs = np.random.random(obs_size)
        r.add_obs(obs)
        res.append(obs)

    true_median = np.median(np.asarray(res).squeeze(), axis=0)
    remedian_median = r.remedian.squeeze()
    assert true_median.shape == remedian_median.shape
    np.testing.assert_array_equal(true_median, remedian_median)
