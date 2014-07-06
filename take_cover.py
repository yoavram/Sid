from skimage import data, filter, color
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def to_gray(image_rgb):
	return 255-color.rgb2gray(image_rgb)*255

def to_bw(image_gray):
	image_bw = image_gray.copy()
	image_bw[image_gray<=0] = 0
	image_bw[image_gray>1] = 255
	return image_bw


def otsu_segmentation(image_gray):
	otsu_thresh = filter.threshold_otsu(image_gray)
	return image_gray >= otsu_thresh

def image_histogram(image_gray):
	fig, ax = plt.subplots(1, 1)
	counts,breaks = np.histogram(image_gray)
	ax.bar(breaks[:-1], counts, width=20, color="k")
	ax.set_xlabel("greyscale")
	ax.set_ylabel("count")	
	return fig,ax,counts,breaks

th1,th2,th3 = 15, 110, 180
bg_color,cover_color,eliosom_color,uncover_color = 0,80,170,255
def trenary_segmentation(image_gray):
	image_tre = image_gray.copy()
	image_tre[image_gray <= th1] = bg_color
	image_tre[(image_gray <= th2) & (image_gray > th1)] = cover_color
	image_tre[(image_gray <= th3) & (image_gray > th2)] = eliosom_color
	image_tre[image_gray > th3] = uncover_color
	return image_tre

def add_image(image, ax=None, cmap="Greys"):	
    if ax == None:
        fig, ax = subplots(1,1)
    ax.imshow(image, cmap=cmap)
    ax.set_xticks([])
    ax.set_yticks([])   
    return ax

def process_image(image_id):
	image = Image.open(image_id + ".jpg")
	w,h = image.size
	fig, ax = plt.subplots(1, 5, figsize=(20,4), sharex=True, sharey=True)
	image_rgb = np.array(image)
	add_image(image_rgb, ax[0])

	image_gray = to_gray(image_rgb)
	add_image(image_gray, ax[1])
	image_bw = to_bw(image_gray)
	add_image(image_bw, ax[2])

	total_area = float(w*h)
	seed_area = float((image_bw==255).sum())

	image_otsu = otsu_segmentation(image_gray)
	add_image(image_otsu, ax[3])
	fig_hist,ax_hist,counts,breaks = image_histogram(image_gray)
	fig_hist.savefig(image_id + "_histogram.png")
	image_tre = trenary_segmentation(image_gray)
	add_image(image_tre, ax[4])

	fig.savefig(image_id + ".png")
	print "Saved images to %s" % image_id + ".png"

	print "image: %s" % image_id
	print "image area: %d" % total_area
	print "seed area: %d" % seed_area
	print "%% cover: %.3f" % ((image_tre == cover_color).sum() / seed_area)
	print "%% eliosom: %.3f" % ((image_tre == eliosom_color).sum() / seed_area)
	print "%% uncovered: %.3f" % ((image_tre == uncover_color).sum() / seed_area)

import sys
if len(sys.argv) != 2:
	print "Please provide a filename without the extensions (abc rather than abc.jpg)"
else:
	image_id = sys.argv[1]	
	process_image(image_id)

