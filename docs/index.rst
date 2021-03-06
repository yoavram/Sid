.. Sid documentation master file, created by
   sphinx-quickstart on Sun Oct 25 14:56:48 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sid: image processing for seed images
=======================================

|PyPi| |Supported Python versions| |License| |Build Status| |Docs| |codecov.io| |Zenodo| |FigShare|


**Author**: `Yoav Ram <http://www.yoavram.com>`_

**Source code**: `GitHub <https://github.com/yoavram/Sid/>`_

**Dataset**: `FigShare <http://doi.org/10.6084/m9.figshare.11446380>`_

Sid is an open-source Python package for image processing of plant seed images, specifically *Lamium amplexicaule*.

Requirements
------------

- Python
- PIL/Pillow
- numpy
- scipy
- scikit-image
- matplotlib
- watchdog
- click
- pywin32 (on Windows)

For testing and documentation:

- nose
- coverage
- sphinx

Install
-------

1. Install the `Anaconda Python distribution <https://www.anaconda.com/downloads>`_.

2. Update all Python packages using :command:`conda`:

>>> conda update --all --yes

3. Install Sid using :command:`pip`:

>>> pip install Sid

4. Check that Sid was installed properly by running the :command:`take_cover` script:

>>> take_cover --version
Sid, version x.x.x

where ``x.x.x`` will be replaced by the current version (|release|).

.. tip::

	When installing on **Windows**, if you get an error trying to install *pywin32* or *pypiwin32*, try to run:

	>>> conda install pywin32 --yes

Upgrade
^^^^^^^

To upgrade to the newest version of Sid (|release|):

>>> conda update --all --yes
>>> pip install --upgrade Sid
>>> take_cover --version
Sid, version x.x.x

Usage
-----

Use by running:

>>> take_cover

The script will first ask for a folder name - this will be the working directory from which the script will read ``.jpg`` files and to which it will write ``.png`` and ``.csv`` files.

The script will then ask if the folder should be processed Continuously or once.

For more options, see the help message:

>>> take_cover --help

Continuous processing
^^^^^^^^^^^^^^^^^^^^^

In this case the script will wait for new ``.jpg`` files in the folder. When a new ``.jpg`` file is created, the script will process it, creating ``.png`` files with the color spaces and the segmentation checkpoints, open the segmentation image, and will print the final stats to the screen.

Single processing
^^^^^^^^^^^^^^^^^

In this case the script will go over all ``.jpg`` files in the folder and process them. It will produce ``.png`` files with the color spaces and the segmentation checkpoints and two ``.csv`` files: one with the final stats for each ``.jpg`` file and one with the histograms that were used to find the features on the seed (background, eliosom, cover). 

Configuration file
^^^^^^^^^^^^^^^^^^

:file:`take_cover.json` is the configuration file which includes values of different parameters of the algorithm, including segmentation thresholds. 

Support
-------

Please contact `Yoav Ram <http://www.yoavram.com>`_ with questions and comments.

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
- Documentation is hosted by `Read The Docs <http://sid.readthedocs.org/>`_
- Documentation is built with `Sphinx <http://sphinx-doc.org/>`_

License
-------

Sid source code and examples are licensed under the terms of the `MIT license <http://opensource.org/licenses/MIT>`_.

Sid documentation, examples, and other materials are licensed under the terms of the `Creative Commons Attribution 4.0 International (CC BY 4.0) license <https://creativecommons.org/licenses/by/4.0/>`_

.. |PyPi| image:: https://img.shields.io/pypi/v/Sid.svg
   :target: https://pypi.python.org/pypi/Sid/
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/Sid.svg
   :target: https://pypi.python.org/pypi/Sid/
.. |License| image:: https://img.shields.io/pypi/l/Sid.svg
   :target: https://github.com/yoavram/Sid/blob/master/LICENCE.txt
.. |Build Status| image:: https://travis-ci.org/yoavram/Sid.svg?branch=master
    :target: https://travis-ci.org/yoavram/Sid
.. |Docs| image:: https://readthedocs.org/projects/sid/badge/?version=latest
   :target: http://sid.readthedocs.org/en/latest/?badge=latest
.. |codecov.io| image:: http://codecov.io/github/yoavram/Sid/coverage.svg?branch=master
   :target: http://codecov.io/github/yoavram/Sid
.. |Zenodo| image:: https://zenodo.org/badge/16996832.svg
   :target: https://zenodo.org/badge/latestdoi/16996832
.. |FigShare| image:: https://img.shields.io/badge/Dataset-FigShare-blueviolet
   :target: http://doi.org/10.6084/m9.figshare.11446380.v1
