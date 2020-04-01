

.. image:: https://travis-ci.org/sappelhoff/remedian.svg?branch=master
   :target: https://travis-ci.org/sappelhoff/remedian
   :alt: Build Status


.. image:: https://codecov.io/gh/sappelhoff/remedian/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/sappelhoff/remedian
   :alt: codecov


.. image:: https://readthedocs.org/projects/remedian/badge/?version=latest
   :target: http://remedian.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://badge.fury.io/py/remedian.svg
   :target: https://badge.fury.io/py/remedian
   :alt: PyPI version


remedian
========

See `the documentation <http://remedian.readthedocs.io/en/latest/>`_!

.. docs_readme_include_label

The  Remedian:  A  Robust  Averaging  Method  for  Large  Data  Sets - Python
implementation

This algorithm is used to approximate the median of several data chunks if
these data chunks cannot (or should not) be loaded into memory at once.

Given a data chunk of size ``obs_size``, and ``t`` data chunks overall, the
Remedian class sets up a number ``k_arrs`` of arrays of length ``n_obs``.

The median of the ``t`` data chunks of size ``obs_size`` is then approximated
as follows: One data chunk after another is fed into the ``n_obs`` positions
of the first array. When the first array is full, its median is calculated
and stored in the first position of the second array. After this, the first
array is re-used to fill the second position of the second array, etc.
When the second array is full, the median of its values is stored in the
first position of the third array, and so on.

The final "Remedian" is the median of the last array, after all ``t`` data
chunks have been fed into the object.

Installation
============

``remedian`` runs on Python 3 with ``numpy`` as its only dependency.
You can install ``remedian`` with ``pip`` ``pip install remedian``.

Installation of development version
===================================

#. activate your python environment
#. ``git clone https://www.github.com/sappelhoff/remedian``
#. ``cd remedian``
#. ``pip install -r requirements-dev.txt``
#. ``pip install -r requirements.txt``
#. ``pip install -e .``
#. then you should be able to ``from remedian import Remedian``

Usage
=====

See the `examples <https://remedian.readthedocs.io/en/latest/auto_examples/index.html>`_.

CONTRIBUTIONS WELCOME
=====================

This is a very basic package currently and there are many enhancements that
could be made. If you want to work on this, please write a GitHub issue or
submit a Pull Request.

References
==========
#. P.J. Rousseeuw, G.W. Bassett Jr., "The remedian: A robust averaging method
   for large data sets", Journal of the American Statistical Association, vol.
   85 (1990), pp. 97-104

#. M. Chao, G. Lin, "The asymptotic distributions of the remedians", Journal of
   Statistical Planning and Inference, vol. 37 (1993), pp. 1-11

#. Domenico Cantone, Micha Hofri, "Further analysis of the remedian algorithm",
   Theoretical Computer Science, vol. 495 (2013), pp. 1-16
