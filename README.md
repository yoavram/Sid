# Sid
## Image processing scripts for seed pictures
![https://raw.githubusercontent.com/yoavram/Sid/master/Sid.png](https://raw.githubusercontent.com/yoavram/Sid/master/Sid.png)

Python scripts for image processing of photos of plant seeds, specifically _Lamium amplexicaule_.

## Requirements

- *Python 2.7*
- *PIL* - Image processing library. 
- *numpy* - The ultimate numerical python packge.
- *scipy* - The ultimate scientific python package (the _ndimage_  is required).
- *scikit-image* - Another image processing library

## Install

Python can be downloaded from [python.org](http://www.python.org/download/releases/2.7.6/)

Windows installers for *numpy*, *scipy*, *PILLOW* (*PIL* stand-in) and *scikit-image* can be downloaded from [Gohlke's website](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

Another option for windows is to use the [Anaconda python distribution](https://store.continuum.io/cshop/anaconda/) (free).

Sid can then be downloaded by cloning the repository:
```
git clone https://github.com/yoavram/Sid.git
```
of by downloading the repository as a [zip file](https://github.com/yoavram/Sid/archive/master.zip).

The only files that are required for analyzing seed photos are `take_cover.py` and `take_cover.json` (see details below).

## Usage

### take_cover.py

Use by running:
```
python take_cover.py
```
The script will first ask for a folder name - this will be the working directory from which the script will read _jpg_ files and to which it will write _png_ and _csv_ files.

The script will then ask if the folder should be prcoessed Continuously or once.

## Continuous processing

In this case the script will wait for new _jpg_ files in the folder. When a new _jpg_ file is created, the script will process it, creating _png_ files with the color spaces and the segmentation checkpoints, open the segmentation image, and will print the final stats to the screen.

## Single processing

In this case the script will go over all _jpg_ files in the folder and process them. It will produce _png_ files with the color spaces and the segmentation checkpoints and two _csv_ files: one with the final stats for each _jpg_ file and one with the histograms that were used to find the features on the seed (background, eliosom, cover). 

### take_cover.json

This is the configuration file which includes values of different parameters of the algorithm, including segmentation thresholds. 

## License

The scripts are available for use under the CC-BY-SA 3.0 license. If the scripts are used or remixed for use or support of an academic publication, please contact [Yoav Ram](https://github.com/yoavram) regarding proper attribution.

