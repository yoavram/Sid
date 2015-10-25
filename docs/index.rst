.. Sid documentation master file, created by
   sphinx-quickstart on Sun Oct 25 14:56:48 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sid: image processing for seed images
=======================================

|PyPi| |Supported Python versions| |License| |Build Status| |Docs| |codecov.io| 


**Author**: `Yoav Ram <http://www.yoavram.com>`_
**Source code**: `GitHub <https://github.com/yoavram/Sid/>`_

Sid is an open-source Python package for image processing of plant seed images, specifically *Lamium amplexicaule*.

Requirements
------------

- Python 2.7
- PIL/Pillow
- numpy
- scipy.ndimage
- scikit-image
- matplotlib
- watchdog
- click

For testing and documentation:

- nose
- coverage
- sphinx

Install
-------

1. Install the `Anaconda Python 2.7 distribution <https://www.continuum.io/downloads>`_.
2. Install Sid using :command:`pip`:

>>> pip install Sid

3. Check that Sid was installed properly by running the :command:`take_cover` script:

>>> take_cover --version
Sid, version x.x.x

where ``x.x.x`` will be replaced by the current version (|release|).

Usage
-----

Use by running:

>>> take_cover

The script will first ask for a folder name - this will be the working directory from which the script will read ``.jpg`` files and to which it will write ``.png`` and _csv_ files.

The script will then ask if the folder should be prcoessed Continuously or once.

For more options, see the help message:

>>> take_cover --help

Continuous processing
^^^^^^^^^^^^^^^^^^^^^

In this case the script will wait for new ``.jpg`` files in the folder. When a new ``.jpg`` file is created, the script will process it, creating ``.png`` files with the color spaces and the segmentation checkpoints, open the segmentation image, and will print the final stats to the screen.

Single processing
^^^^^^^^^^^^^^^^^

In this case the script will go over all ``.jpg`` files in the folder and process them. It will produce ``.png`` files with the color spaces and the segmentation checkpoints and two _csv_ files: one with the final stats for each ``.jpg`` file and one with the histograms that were used to find the features on the seed (background, eliosom, cover). 

Configuration file
^^^^^^^^^^^^^^^^^^

:file:`take_cover.json` is the configuration file which includes values of different parameters of the algorithm, including segmentation thresholds. 

Support
-------

Don't hesitate to contact `Yoav Ram <http://www.yoavram.com>`_ with questions and comments.

Bugs and feature requests can be opened on `GitHub Issues <https://github.com/yoavram/Sid/issues>`_

Developers
----------

Developers should clone the repository from GitHub and install it in *editable* mode:

>>> git clone https://github.com/yoavram/Sid.git
>>> cd Sid
>>> pip install -e .

- Source code is hosted by `GitHub <https://github.com/yoavram/Sid>`_
- Testing is done with ``nosetests Sid/tests``
- Continuous integration and deployment is performed by `Travis-CI <https://travis-ci.org/yoavram/Sid>`_
- Code coverage is tracked by `codecov.io <http://codecov.io/github/yoavram/Sid>`_
- Package is hosted on `PyPi <https://pypi.python.org/pypi/Sid/>`_
- Documentation is hosted by `PythonHosted <http://pythonhosted.org/Sid/>`_
- Documentation is built with `Sphinx <http://sphinx-doc.org/>`_

Licence
-------

Sid source code and examples are licensed under the terms of the `MIT licence <http://opensource.org/licenses/MIT>`_.

Sid documentation, examples, and other materials are licensed under the terms of the `Creative Commons Attribution 4.0 International (CC BY 4.0) licence <https://creativecommons.org/licenses/by/4.0/>`_

.. |PyPi| image:: https://img.shields.io/pypi/v/Sid.svg
   :target: https://pypi.python.org/pypi/Sid/
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/Sid.svg
   :target: https://pypi.python.org/pypi/Sid/
.. |License| image:: https://img.shields.io/pypi/l/Sid.svg
   :target: https://github.com/yoavram/Sid/blob/master/LICENCE.txt
.. |Build Status| image:: https://travis-ci.org/yoavram/Sid.svg
   :target: https://travis-ci.org/yoavram/Sid
.. |Docs| image:: https://img.shields.io/badge/docs-latest-yellow.svg
   :target: http://pythonhosted.org/Sid/
.. |codecov.io| image:: http://codecov.io/github/yoavram/Sid/coverage.svg?branch=master
   :target: http://codecov.io/github/yoavram/Sid