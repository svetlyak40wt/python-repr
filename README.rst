========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        |
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-repr/badge/?style=flat
    :target: https://readthedocs.org/projects/python-repr
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/svetlyak40wt/python-repr.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/svetlyak40wt/python-repr

.. |requires| image:: https://requires.io/github/svetlyak40wt/python-repr/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/svetlyak40wt/python-repr/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/repr.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/repr

.. |downloads| image:: https://img.shields.io/pypi/dm/repr.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/repr

.. |wheel| image:: https://img.shields.io/pypi/wheel/repr.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/repr

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/repr.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/repr

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/repr.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/repr


.. end-badges

A shortcut to generate __repr__ methods.

* Free software: BSD license

Installation
============

::

    pip install repr

Documentation
=============

https://python-repr.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
