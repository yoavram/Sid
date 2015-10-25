# Sid
## Image processing for seed images

![Logo](https://raw.githubusercontent.com/yoavram/Sid/master/Sid.png)

Python script for image processing of plant seed images, specifically _Lamium amplexicaule_.

[![PyPI](https://img.shields.io/pypi/v/Sid.svg)](https://pypi.python.org/pypi/Sid/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/Sid.svg)](https://pypi.python.org/pypi/Sid/)
[![License](https://img.shields.io/pypi/l/Sid.svg)](https://github.com/yoavram/Sid/blob/master/LICENCE.txt)
[![Build Status](https://travis-ci.org/yoavram/Sid.svg)](https://travis-ci.org/yoavram/Sid)
[![codecov.io](http://codecov.io/github/yoavram/Sid/coverage.svg?branch=master)](http://codecov.io/github/yoavram/Sid)

## Requirements

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

## Install

1. Install the [Anaconda Python 2.7 distribution](https://www.continuum.io/downloads).
1. Install Sid using pip:
```
pip install Sid
```
1. Check that Sid was installed properly:
```
take_cover --version
```

### Developers

Sid can also be used by cloning the repository, usually for developing purposes:
```
git clone https://github.com/yoavram/Sid.git
```
or by downloading the repository as a [zip file](https://github.com/yoavram/Sid/archive/master.zip).

## Usage

### take_cover

Use by running:
```
take_cover
```
The script will first ask for a folder name - this will be the working directory from which the script will read _jpg_ files and to which it will write _png_ and _csv_ files.

The script will then ask if the folder should be prcoessed Continuously or once.

For more options, see the help message:
```
take_cover --help
```

## Continuous processing

In this case the script will wait for new _jpg_ files in the folder. When a new _jpg_ file is created, the script will process it, creating _png_ files with the color spaces and the segmentation checkpoints, open the segmentation image, and will print the final stats to the screen.

## Single processing

In this case the script will go over all _jpg_ files in the folder and process them. It will produce _png_ files with the color spaces and the segmentation checkpoints and two _csv_ files: one with the final stats for each _jpg_ file and one with the histograms that were used to find the features on the seed (background, eliosom, cover). 

### take_cover.json

This is the configuration file which includes values of different parameters of the algorithm, including segmentation thresholds. 

## Support
Don't hesitate to contact [Yoav Ram](http://www.yoavram.com) for questions and help.

Bugs and feature requests can be opened on [GitHub](https://github.com/yoavram/Sid/issues) 

[![GitHub issues](https://img.shields.io/github/issues/yoavram/Sid.svg)](https://github.com/yoavram/Sid)


## License

Sid source code and examples are licensed under the terms of the [MIT license](http://opensource.org/licenses/MIT).

Sid documentation, examples, and other materials are licensed under the terms of the [Creative Commons Attribution 4.0 International (CC BY 4.0) license](https://creativecommons.org/licenses/by/4.0/).

