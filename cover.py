from skimage import filter, color
from skimage.morphology import square
from PIL import Image
from scipy import ndimage
from numpy import array
import sys
from os import path
from glob import glob
import matplotlib.pyplot as plt

def process_file(filename):
	print "Processing %s" % filename
	img_rgb = array(Image.open(filename))
	img_gray = color.rgb2gray(img_rgb)
	th = img_gray.mean()
	#print "Threshold:", th
	mask = ~(img_gray <= th)
	blur = filter.rank.median(mask, square(5))
	edges = filter.canny(img_gray, sigma=1)
	edges = filter.rank.maximum(edges, square(5))
	mask_edges = edges.astype(mask.dtype) + mask
	filled = ndimage.morphology.binary_fill_holes(mask_edges)
	print "Black: %.5f" % ((blur == 255).sum()/float(filled.sum()))

def process_folder(dirname):
	print "Processing %s" % dirname
	files = glob(dirname+'/*.tif')
	files += glob(dirname+'/*.tiff')
	files += glob(dirname+'/*.jpg')
	files += glob(dirname+'/*.jpeg')
	print "Found %d images in %s" % (len(files), dirname)
	for filename in files:
		process_file(filename)

if __name__ == '__main__':
	args = sys.argv
	if len(args) == 1:
		print "Usage: python %s <filename> " % args[0]
		print
		sys.exit()
	filename = args[1]
	if len(args) > 2:
		sigma = float(args[2])
	else:
		sigma = 256/40.

	if path.isdir(filename):
		process_folder(filename)
	else:
		process_file(filename)

