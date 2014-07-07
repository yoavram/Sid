# Sid
## Image processing scripts for seed pictures

This repo contains experimental Python scripts for processing of pictures of plant seeds.

See the [notebook](http://nbviewer.ipython.org/github/yoavram/Sid/blob/master/IP%20lab.ipynb) for a walkthrough.

### Requirements

- *Python 2.7*
- *PIL* - Image processing library. 
- *numpy* - The ultimate numerical python packge.
- *scipy* - The ultimate scientific python package (the _ndimage_  is required).
- *scikit-image* - Another image processing library

### Install

Python can be downloaded from [python.org](http://www.python.org/download/releases/2.7.6/)

Windows installers can be downloaded from [Gohlke's website](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

Another option for windows is to use [Enthought python distribution (EPD)](https://www.enthought.com/products/epd/) for which [free academic licenses](https://www.enthought.com/products/canopy/academic/) are available.

### Usage

#### pieces.py

This script accepts either a filename of an image of a folder of _tif_ and _jpg_ files.
The script will go over the input images and look for "objects" (seeds) in them.
Each seed will be saved to a separate file.
When giving the script a high-resolution image you should use the second parameter, which is the "blur" parameter, and give a higher value like 50. Otherwise, the script will find many (>20) objects due to noise. This parameter is optional because it has a default value (256/40).

Use by running:
```
python pieces.py sunflower.jpg 5
```

#### cover.py

This script accepts either a filename of an image of a folder of _tif_ and _jpg_ files.
The script assumes that there is a single "seed" object in each image.
The script will try to meausre the amount of white cover on the face of the seed and will print out the ratio between the seed area and the white area on it.
Seed objects should be on a solid uniform background.

Use by running:
```
python cover.py sunflower.jpg_1.jpg
```


