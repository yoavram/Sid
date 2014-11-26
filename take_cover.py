from matplotlib.pyplot import *
from numpy import *

from skimage import data, filter, color, measure
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from skimage.morphology import dilation, erosion, square
from scipy.ndimage import filters, label, binary_opening, find_objects
from PIL import Image
import csv
from glob import glob
import os
import json

try:
        with open("take_cover.json") as f:
                params = json.load(f)
except Exception as e:
        print "Falied reading parameters file"
        raise e

# Image processing functions

def to_gray(image_rgb):
	return 255-color.rgb2gray(image_rgb)*255

def to_bw(image_gray):
	image_bw = image_gray.copy()
	image_bw[image_gray<=0] = 0
	image_bw[image_gray>1] = 255
	return image_bw

def rgb2yuv(input): # modified from https://gist.github.com/bombless/4286560
    R, G, B = input[:,:,0],input[:,:,1],input[:,:,2]
    Y = array(0.299 * R + 0.587 * G + 0.114 * B, dtype=input.dtype)
    U = array(-0.147 * R + -0.289 * G + 0.436 * B, dtype=input.dtype)
    V = array(0.615 * R + -0.515 * G + -0.100 * B, dtype=input.dtype)
    output = input.copy()
    output[:,:,0],output[:,:,1],output[:,:,2] = Y,U,V
    return output
color.rgb2yuv = rgb2yuv

def otsu_segmentation(image_gray):
	otsu_thresh = filter.threshold_otsu(image_gray)
	return image_gray >= otsu_thresh

def image_histogram(image_gray):
	fig, ax = subplots(1, 1)
	counts,breaks = histogram(image_gray)
	ax.bar(breaks[:-1], counts, width=20, color="k")
	ax.set_xlabel("greyscale")
	ax.set_ylabel("count")	
	return fig,ax,counts,breaks

def plot_image(im, ax=None, cmap="Greys", title=None):
    if ax == None:
        fig, ax = subplots(1,1)
    ax.imshow(im, cmap=cmap)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title)
    return ax

def all_color_spaces(img):
	hsv = color.rgb2hsv(img)
	xyz = color.rgb2xyz(img)
	yuv = color.rgb2yuv(img) # ycbcr
	lab = color.rgb2lab(img)
	hed = color.rgb2hed(img)
	cie = color.rgb2rgbcie(img)
	gray = color.rgb2gray(img)
	return {"rgb":img, "hsv":hsv,"xyz":xyz,"yuv":yuv,"lab":lab,"hed":hed,"cie":cie,"gray":gray}

def plot_color_spaces(color_spaces, cmap="Greys"):	
	fig, ax = subplots(1, len(color_spaces), figsize=(20,8))
	for i,(k,v) in enumerate(sorted(color_spaces.items())):
		ax[i].imshow(v, cmap=cmap)
		ax[i].set_xticks([])
		ax[i].set_yticks([])
		ax[i].set_title(k)
	fig.tight_layout()
	return fig,ax

def triplot_image(img, title=''):
	fig, ax = subplots(1, 3, figsize=(10,8))
	for i,v in enumerate(['R ','G ','B ']):
		ax[i].imshow(img[:,:,i], cmap="Greys")
		ax[i].set_xticks([])
		ax[i].set_yticks([])
		ax[i].set_title(v + title)
	fig.tight_layout()
	return fig,ax

def smooth(img):
    if len(img.shape) == 2:
        return filters.convolve(img, ones((10,10))/100, mode='mirror')
    elif len(img.shape) == 3:
        R, G, B = img[:,:,0],img[:,:,1],img[:,:,2]
        R, G, B = smooth(R), smooth(G), smooth(B)
        output = img.copy()
        output[:,:,0],output[:,:,1],output[:,:,2] = R, G, B
        return output       
    else:
        raise NotImplementedError()

def add_image(image, ax=None, cmap="Greys"):	
        if ax == None:
                fig, ax = subplots(1,1)
        ax.imshow(image, cmap=cmap)
        ax.set_xticks([])
        ax.set_yticks([])   
        return ax

def plot_hist(image, ax, th=None, title=""):
	ax.hist(image.flatten(), normed=True, bins=20, color='w')
        if th:
                ax.axvline(x=th, color='r')
                ax.set_title("%s histogram\nth=%.2f" % (title, th))
	else:
                ax.set_title("%s histogram" % title)
	return ax


# main function to process a single image
def process_image(image_id):
	print "Starting", image_id
	image = Image.open(image_id + ".jpg")
	w,h = image.size

	image_rgb = array(image)
	color_spaces = all_color_spaces(image_rgb)
	fig,ax = plot_color_spaces(color_spaces)
	fig.savefig(image_id  + "_colorspaces.png")
	
	fig,ax = subplots(4, 4, figsize=(10,8))
	plot_image(image_rgb, ax=ax[0,0], title="original")

# bg
        #print "bg"
	gray = color_spaces["gray"]
	plot_image(gray, ax=ax[0,0], title="gray")
	otsu_th = filter.threshold_otsu(gray)
	mean_th = gray.mean()
	th = otsu_th if otsu_th > params["min_otsu_th"] else mean_th
        bg = gray > th
        plot_image(bg, ax=ax[0,1], title="mask th=%.4f" % th)
	axis = plot_hist(gray[gray<1], ax[0,2], th=th, title="gray")
        axis.axvline(x=mean_th, color='b', label="mean")
        axis.axvline(x=otsu_th, color='g', label="otsu")
        axis.legend(loc="upper left")
        bg = binary_opening(bg, square(params["binary_opening_size"]), params["binary_opening_iters"])
        bg_for_cover =  dilation(bg, square(15))
        bg = dilation(bg, square(params["dilation_size"]))
        bg = bg > 0
        bg_for_cover = bg_for_cover > 0
        fg = ~bg
        fg_for_cover = ~bg_for_cover
        plot_image(bg, ax=ax[0,3], title="bg - bin open & dilation")

# labels
        label_im, nb_labels = label(bg==0)
	regions = measure.regionprops(label_im)#, properties=['Area', 'Perimeter'])
	props = regions[0]
	centroid_x, centroid_y = props['centroid']
	
# eliosom
        #print "eliosom"
	plot_image(color_spaces['lab'][:,:,2], ax=ax[1,0], title="lab B")
	lab_smooth_B = smooth(color_spaces["lab"])[:,:,2]
	plot_image(lab_smooth_B, ax=ax[1,1], title="lab smooth B")
	th = params["eliosom_th"]
        th = filter.threshold_yen(lab_smooth_B) * 1.2
	axis = plot_hist(lab_smooth_B, ax[1,2], th=th, title="lab smooth B")
	eliosom_mask = lab_smooth_B > th
	eliosom_mask = eliosom_mask & fg
	eliosom_mask[:,:centroid_y] = False
	img_eliosom = image_rgb.copy()
	img_eliosom[eliosom_mask] = (255,0,0)
	plot_image(img_eliosom, ax[1,3], title="eliosom")


# cover
        #print "cover"
        gray = color_spaces["gray"]
	plot_image(gray, ax=ax[2,0], title="gray")
	gray_smooth = smooth(color_spaces["gray"])      
	th = (gray[fg>0].mean())*1.1
        axis = plot_hist(gray, ax[2,2], th=th, title="gray")
	cover_mask = gray > th	
	cover_mask = (cover_mask & fg_for_cover) & ~eliosom_mask
	img_cover = image_rgb.copy()
	img_cover[cover_mask] = (0,255,0)
	plot_image(img_cover, ax[2,3], title="cover")


# measure square
        image_yellow = image_rgb[:,:,2] > 200
        plot_image(image_yellow, ax[3,0], title="yellow mask")
        image_yellow = binary_opening(image_yellow, square(1), 10)
        labels_yellow,n_yellow = label(~image_yellow)
        regions_yellow = measure.regionprops(labels_yellow)
        regions_yellow.sort(key=lambda x: x.area, reverse=True)
        plot_image(labels_yellow, ax[3,1], title="yellow ref")
        
# final
        #print "final"
	output_img = image_rgb.copy()
	output_img[:,:] = (0,0,0)
	output_img[cover_mask] = (0,255,0)
	output_img[eliosom_mask] = (255,0,0)
	output_img[bg > 0] = (0,0,255)
	
	plot_image(image_rgb, ax[3,2], title="original")
	ax[3,0].axis('off')
	ax[3,1].axis('off')
	plot_image(output_img, ax[3,3], title="final")
	

	fig.tight_layout()
	fig.savefig(image_id + "_color_segmentation.png")
        fig.close()
        
# stats
	stats = {'image_id': image_id}
	stats["total_area"] =   h*w - sum(output_img[:,:,2] > 0)
	stats["cover_area"] =   sum(output_img[:,:,1] > 0)
	stats["eliosom_area"] = sum(output_img[:,:,0] > 0)
	stats["major_axis_length"] = props.major_axis_length
	stats["minor_axis_length"] = props.minor_axis_length
	stats["area"] = props.area
	stats["perimeter"] = props.perimeter
	stats["orientation"] = props.orientation
	stats["ref_area"] = regions_yellow[1].area
	stats["ref_major_axis_length"] = regions_yellow[1].major_axis_length
	stats["ref_minor_axis_length"] = regions_yellow[1].minor_axis_length

	return stats

def process_folder():
	files = glob("*.jpg")
	foutname = 'stats.csv'
	fout = open(foutname, 'w')
	wr = None
	for fn in files:
		image_id = fn[:fn.index(".jpg")]
		stats = process_image(image_id)
		if wr == None:
			wr = csv.DictWriter(fout, stats.keys())
			wr.writeheader()
		wr.writerow(stats)
	fout.close()
	print "Saved statistics to %s" % foutname


def watch_folder(path):	
	from watchdog.events import FileSystemEventHandler
	from watchdog.observers import Observer
	from watchdog.events import FileCreatedEvent#, LoggingEventHandler
	from subprocess import Popen
	DETACHED_PROCESS = 0x00000008
	
	#import logging
	import time
	class EventHandler(FileSystemEventHandler):
		def on_created(self, event):
			if not isinstance(event,  FileCreatedEvent):
				return
			fn = event.src_path.lower()
			if not fn.endswith(".jpg"):
				return
			print "Processing new file", fn
			image_id = fn[:fn.index(".jpg")]
			stats = process_image(image_id)
			print "Proccesed file", fn
			print "See folder for utility images"
			print "############################"
			print "Stats:"
			for k,v in sorted(stats.items()):
				print k,":",v
			print "############################"
			cmd = [
				"C:\Program Files\IrfanView\i_view32.exe",
				image_id + '_color_segmentation.png'
			]
			Popen(cmd,shell=False,stdin=None,stdout=None,stderr=None,close_fds=True,creationflags=DETACHED_PROCESS)
			print "Waiting for new images..."
	#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	event_handler = EventHandler()#LoggingEventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=False)
	print "Watching folder", path
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
	return
	image_id = fn[:fn.index(".jpg")]
	stats = process_image(image_id)
	
	
	


if __name__ == '__main__':
        try:
                foldername = raw_input("Please provide a folder name\n")
                if not os.path.exists(foldername):
                        print "Folder", foldername, "doesn't exist"
                        raw_input("Click enter to finish...")
                else:
                        use_watchdog = raw_input("Watch folder? (y - run continously; n - run once)").lower() == 'y'		
                        if use_watchdog:
                                watch_folder(foldername)
                        else:
                                os.chdir(foldername)
                                process_folder()
                                os.chdir("..")
        except Exception as e:
                print e
	raw_input("Click enter to finish...")
	
