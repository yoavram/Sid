from skimage import filter, color
from PIL import Image
from scipy import ndimage
from numpy import array, median, unique
import sys
from os import path
from glob import glob

def process_file(filename):
	print "Processing %s" % filename
	image_rgb = array(Image.open(filename))
	image_gray = color.rgb2gray(image_rgb)
	image_blur = ndimage.gaussian_filter(image_gray, sigma=sigma)
	mask = image_blur > image_blur.mean()
	if median(image_gray) > 0.5:
		print "Reverting colors"
		mask = ~mask
	label_im, nb_labels = ndimage.label(mask)
	print "Found %d pieces" % nb_labels
	if nb_labels > 4:
		yes = raw_input("Continue? (y/n)")
		if yes != "y":
			return
	for i in range(1, nb_labels+1):
		slice_x,slice_y = ndimage.find_objects(label_im==i)[0]
		img = image_rgb[slice_x, slice_y]
		img_pil = Image.fromarray(img)
		outname = "%s_%d.jpg" % (filename, i)
		img_pil.save(outname)
		print "Saved to %s" % outname

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
		print "Usage: python %s <filename> [gaussian filter sigma (256/40)]" % args[0]
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