#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Sid.
# https://github.com/yoavram/Sid

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>
import os
from glob import glob
import json
import csv
from subprocess import Popen
import time
import datetime
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.events import FileCreatedEvent
import matplotlib.pyplot as plt
import numpy as np
from skimage import filters, color, measure
from skimage.morphology import dilation, erosion, square
from scipy.ndimage import label, binary_opening
from scipy.ndimage import filters as scipy_filters
from PIL import Image
import click
import pkg_resources
import Sid


ERROR_COLOR = 'red'
INFO_COLOR = 'cyan'
DETACHED_PROCESS = 0x00000008
EXTENSION = ".jpg"
DEFAULT_CONFIG_PATH = pkg_resources.resource_filename('Sid', os.path.splitext(os.path.basename(__file__))[0] + '.json')
CONFIG = {}
NOW = datetime.datetime.now().ctime()

echo = click.echo

def echo_error(message):
    click.secho("Error: %s" % message, fg=ERROR_COLOR)

def echo_info(message):
    click.secho(message, fg=INFO_COLOR)

def ioerror_to_click_exception(io_error):
    if io_error.message:
        message = io_error.message
    else:
        message = 'Make sure that the file is not open and you have permission to write to this path.'
    raise click.FileError(io_error.filename, hint=message)


def where(ctx, param, value):    
    if not value or ctx.resilient_parsing:
        return
    path = Sid.__file__
    folder = os.path.split(path)[0]
    click.secho(click.format_filename(folder))
    ctx.exit()


def logo(ctx, param, value):    
    if not value or ctx.resilient_parsing:
        return    
    click.secho(Sid.__logo__, fg=INFO_COLOR)
    ctx.exit()



# Image processing functions

def to_gray(image_rgb):
    return 255 - color.rgb2gray(image_rgb) * 255


def to_bw(image_gray):
    image_bw = image_gray.copy()
    image_bw[image_gray <= 0] = 0
    image_bw[image_gray > 1] = 255
    return image_bw


def rgb2yuv(input): 
    # modified from https://gist.github.com/bombless/4286560
    R, G, B = input[:,:,0], input[:,:,1], input[:,:,2]
    Y = np.array(0.299 * R + 0.587 * G + 0.114 * B, dtype=input.dtype)
    U = np.array(-0.147 * R + -0.289 * G + 0.436 * B, dtype=input.dtype)
    V = np.array(0.615 * R + -0.515 * G + -0.100 * B, dtype=input.dtype)
    output = input.copy()
    output[:,:,0], output[:,:,1], output[:,:,2] = Y, U, V
    return output
color.rgb2yuv = rgb2yuv


def otsu_segmentation(image_gray):
    otsu_thresh = filters.threshold_otsu(image_gray)
    return image_gray >= otsu_thresh


def image_histogram(image_gray):
    fig, ax = plt.subplots(1, 1)
    counts, breaks = histogram(image_gray)
    ax.bar(breaks[:-1], counts, width=20, color="k")
    ax.set_xlabel("greyscale")
    ax.set_ylabel("count")    
    return fig, ax, counts, breaks


def plot_image(im, ax=None, cmap="Greys", title=None):
    if ax == None:
        fig, ax = plt.subplots(1,1)
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
    return {"rgb":img, "hsv":hsv, "xyz":xyz, "yuv":yuv, "lab":lab, "hed":hed, "cie":cie, "gray":gray}


def plot_color_spaces(color_spaces, cmap="Greys"):    
    fig, ax = plt.subplots(1, len(color_spaces), figsize=(20,8))
    for i, (k, v) in enumerate(sorted(color_spaces.items())):
        ax[i].imshow(v, cmap=cmap)
        ax[i].set_xticks([])
        ax[i].set_yticks([])
        ax[i].set_title(k)
    fig.tight_layout()
    return fig, ax


def triplot_image(img, title=''):
    fig, ax = plt.subplots(1, 3, figsize=(10,8))
    for i, v in enumerate(['R ','G ','B ']):
        ax[i].imshow(img[:,:,i], cmap="Greys")
        ax[i].set_xticks([])
        ax[i].set_yticks([])
        ax[i].set_title(v + title)
    fig.tight_layout()
    return fig,ax


def smooth(img):
    if len(img.shape) == 2:
        return scipy_filters.convolve(img, np.ones((10, 10)) / 100, mode='mirror')
    elif len(img.shape) == 3:
        R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]
        R, G, B = smooth(R), smooth(G), smooth(B)
        output = img.copy()
        output[:,:,0], output[:,:,1], output[:,:,2] = R, G, B
        return output       
    else:
        raise NotImplementedError()


def add_image(image, ax=None, cmap="Greys"):    
    if ax == None:
        fig, ax = plt.subplots(1,1)
    ax.imshow(image, cmap=cmap)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


def plot_hist(image, ax, th=None, title=""):
    counts, bins, patches = ax.hist(image.flatten(), density=True, bins=20, color='w')
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_yticks(ax.get_yticks()[::2])
    if th:
        ax.axvline(x=th, color='r')
        ax.set_title("%s histogram\nth=%.2f" % (title, th))
    else:
        ax.set_title("%s histogram" % title)
    return ax, dict(zip(bins, counts))


def process_image(image_id):
    echo_info("Starting {0}".format(image_id))
    try:        
        image = Image.open("{0}{1}".format(image_id, EXTENSION))
    except IOError as e:
        ioerror_to_click_exception(e)
    w,h = image.size

    image_rgb = np.array(image)
    color_spaces = all_color_spaces(image_rgb)
    fig,ax = plot_color_spaces(color_spaces)
    fig.savefig("{0}_colorspaces.png".format(image_id))
    
    fig,ax = plt.subplots(4, 4, figsize=(10,8))
    plot_image(image_rgb, ax=ax[0,0], title="original")

# bg
    gray = color_spaces["gray"]
    plot_image(gray, ax=ax[0,0], title="gray")
    otsu_th = filters.threshold_otsu(gray)
    mean_th = gray.mean()
    bg_th = otsu_th if otsu_th > CONFIG["min_otsu_th"] else mean_th
    bg = gray > bg_th
    plot_image(bg, ax=ax[0,1], title="mask th=%.4f" % bg_th)
    axis, bg_histogram = plot_hist(gray[gray<1], ax[0,2], th=bg_th, title="gray")
    axis.axvline(x=mean_th, color='b', ls='--', label="mean")
    axis.axvline(x=otsu_th, color='g', ls='--', label="otsu")
    axis.legend(loc="upper left", fontsize=10)
    bg = binary_opening(bg, square(CONFIG["binary_opening_size"]), CONFIG["binary_opening_iters"])
    bg_no_dilation = bg.copy()
    bg_for_cover = dilation(bg, square(CONFIG["cover_dilation_size"]))
    bg_for_eliosom = dilation(bg, square(CONFIG["eliosom_dilation_size"]))
    bg = dilation(bg, square(CONFIG["dilation_size"]))
    bg = bg > 0
    bg_for_cover = bg_for_cover > 0
    bg_for_eliosom = bg_for_eliosom > 0
    fg = ~bg
    fg_for_cover = ~bg_for_cover
    fg_for_eliosom = ~bg_for_eliosom
    plot_image(bg, ax=ax[0,3], title="bg - bin open & dilation")

# labels
    label_im, nb_labels = label(bg==0)
    regions = measure.regionprops(label_im)#, properties=['Area', 'Perimeter'])
    props = regions[0]
    centroid_x, centroid_y = props['centroid']
    
# eliosom
    plot_image(color_spaces['lab'][:,:,2], ax=ax[1, 0], title="lab B")
    lab_smooth_B = smooth(color_spaces["lab"])[:, :, 2]
    plot_image(lab_smooth_B, ax=ax[1, 1], title="lab smooth B")
    eliosom_th = filters.threshold_yen(lab_smooth_B) * CONFIG["eliosom_th_factor"]
    axis, eliosom_histogram = plot_hist(lab_smooth_B, ax[1, 2], th=eliosom_th, title="lab smooth B")
    eliosom_mask = lab_smooth_B > eliosom_th
    eliosom_mask = eliosom_mask & fg_for_eliosom
    eliosom_mask[:,:int(centroid_y)] = False
    img_eliosom = image_rgb.copy()
    img_eliosom[eliosom_mask] = (255, 0, 0)
    plot_image(img_eliosom, ax[1, 3], title="eliosom")

# labels without eliosom
    label_im, nb_labels = label((bg | eliosom_mask) == 0) 
    regions = measure.regionprops(label_im)#, properties=['Area', 'Perimeter'])
    props2 = regions[0]
    centroid_x, centroid_y = props['centroid']

# cover
    gray = color_spaces["gray"]
    plot_image(gray, ax=ax[2, 0], title="gray")
    cover_th = (gray[fg > 0].mean()) * CONFIG["cover_th_factor"]
    axis, cover_histogram = plot_hist(gray, ax[2, 2], th=cover_th, title="gray")
    cover_mask = gray > cover_th
    cover_mask = (cover_mask & fg_for_cover) & ~eliosom_mask
    img_cover = image_rgb.copy()
    img_cover[cover_mask] = (0, 255, 0)
    plot_image(img_cover, ax[2, 3], title="cover")
    ax[2, 1].set_xticks([])
    ax[2, 1].set_yticks([])
    ax[2, 1].text(0.1, 0.5, "This plot left blank")

# measure square
    image_yellow = image_rgb[:, :, 2] > CONFIG["ref_th"]
    plot_image(image_yellow, ax[3, 0], title="yellow mask")
    image_yellow = binary_opening(image_yellow, square(CONFIG["ref_binary_opening"]), 10)
    image_yellow = image_yellow ^ bg_no_dilation
    image_yellow = erosion(image_yellow, square(3))
    #plot_image(image_yellow, ax[3, 1], title="yellow xor bg")
    labels_yellow,n_yellow = label(image_yellow)
    regions_yellow = measure.regionprops(labels_yellow)
    regions_yellow.sort(key=lambda x: x.area, reverse=True)
    plot_image(labels_yellow, ax[3, 1], title="yellow ref")
        
# final
    output_img = image_rgb.copy()
    output_img[:, :] = (0, 0, 0)
    output_img[cover_mask] = (0, 255, 0)
    output_img[eliosom_mask] = (255, 0, 0)
    output_img[bg > 0] = (0, 0, 255)
    
    plot_image(image_rgb, ax[3, 2], title="original")
    ax[3, 0].axis('off')
    ax[3, 1].axis('off')
    plot_image(output_img, ax[3, 3], title="final")
    

    fig.tight_layout()
    fig.savefig("{0}_color_segmentation.png".format(image_id))
    plt.clf()
        
# stats
    stats = {
        'image_id':     image_id,
        "blue_area":    h * w - np.sum(output_img[:, :, 2] > 0),
        "cover_area":   np.sum(output_img[:, :, 1] > 0),
        "eliosom_area": np.sum(output_img[:, :, 0] > 0),
        "bg_th":        bg_th,
        "eliosom_th":   eliosom_th,
        "cover_th":     cover_th,
        "length":       props.major_axis_length,
        "width":        props.minor_axis_length,
        "area":         props.area,
        "perimeter":    props.perimeter,
        "seed_length":  props2.major_axis_length,
        "seed_width":   props2.minor_axis_length,
        "seed_area":    props2.area,
        "seed_perimeter":props2.perimeter,
        "orientation":  props.orientation,
        "ref_area":     regions_yellow[0].area,
        "ref_major_axis_length": regions_yellow[0].major_axis_length,
        "ref_minor_axis_length": regions_yellow[0].minor_axis_length
    }

# histograms
    histograms = {
                'bg': bg_histogram,
                'eliosom': eliosom_histogram,
                'cover': cover_histogram
    }

    return stats, histograms


def process_folder(path):
    files = glob(os.path.join(path, "*" + EXTENSION))
    stats_foutname = os.path.join(path, 'stats.csv')
    hist_foutname = os.path.join(path, 'histograms.csv')
    try:
        stats_fout = click.open_file(stats_foutname, 'w')
        hist_fout = click.open_file(hist_foutname, 'w')
    except IOError as e:
        ioerror_to_click_exception(e)
    stats_wr, hist_wr = None, None

    for fn in files:
        image_id = fn[:fn.index(EXTENSION)]
        stats, histograms = process_image(image_id)
        if stats_wr == None:
            stats_wr = csv.DictWriter(stats_fout, stats.keys())
            stats_wr.writeheader()
        if hist_wr == None:
            hist_wr = csv.writer(hist_fout)
            hist_wr.writerow(['image_id', 'mask', 'bin', 'count'])            
        stats_wr.writerow(stats)
        for mask,histogram in histograms.items():
            for bin,count in histogram.items():
                hist_wr.writerow([image_id, mask, bin, count])
    
    stats_fout.close()
    hist_fout.close()
    echo_info("Saved statistics to {0}".format(click.format_filename(stats_foutname)))
    echo_info("Saved histograms to {0}".format(click.format_filename(hist_foutname)))


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not isinstance(event,  FileCreatedEvent):
            return
        fn = event.src_path.lower()
        if not fn.endswith(EXTENSION):
            return
        echo_info("Processing new file {0}".format(fn))
        image_id = fn[:fn.index(EXTENSION)]
        stats,_ = process_image(image_id)
        echo_info("Proccesed file {0}".format(fn))
        echo_info("See folder for utility images")
        echo_info("############################")
        echo_info("Stats:")
        for k,v in sorted(stats.items()):
            echo("{0}: {1}".format(k, v))
        echo_info("############################")
        if CONFIG.get("autoview", False):
            cmd = [
                CONFIG.get("irfanview_path", "C:\Program Files\IrfanView\i_view32.exe"),
                '{0}_color_segmentation.png'.format(image_id)
            ]
            try:
                Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=DETACHED_PROCESS)
            except WindowsError as e:
                echo_error("Please make sure IrfanView is installed and the full path to i_view32.exe is given in the json configuration file.")
                raise e
        echo_info("Waiting for new images... (hit Ctrl-C to quit)")


def watch_folder(path):
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    echo_info("Watching folder {0} (hit Ctrl-C to quit)".format(path))
    observer.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        observer.stop()
    observer.join()
    return


@click.option('-v/-V', '--verbose/--no-verbose', default=True, 
    help="Print informational messages")
@click.option('--watch', type=click.Choice(['y', 'n', 'q']), prompt="Watch folder? (y - run continously; n - run once; q - quit)", 
    help="Watch the folder for new files (y), just process it once (n), or quit (q).")
@click.option('--where', is_flag=True, default=False, is_eager=True, callback=where, 
    help='Print the path where Sid is installed an exit.')
@click.option('--logo', is_flag=True, default=False, is_eager=True, callback=logo, 
    help='Print the Sid logo an exit.')
@click.option('--path', prompt="Please provide a folder name", type=click.Path(exists=True, readable=True), 
    help="Folder of images to process.")
@click.option('--config_path', default=DEFAULT_CONFIG_PATH, type=click.Path(exists=True, readable=True),
    help='Configuration file path.')
@click.version_option(version=Sid.__version__, prog_name=Sid.__name__)
@click.command()
def main(path, watch, config_path, verbose, where, logo):
    '''Process a folder of seed images, producing a table of statistics.
    See documentation http://sid.readthedocs.org.
    '''
    if not verbose:        
        global echo_info
        echo_info = lambda x: x
        import warnings
        warnings.simplefilter(action="ignore", category=FutureWarning)
        warnings.simplefilter(action="ignore", category=DeprecationWarning)

    global CONFIG
    try:
        with click.open_file(config_path, "r") as f:
            CONFIG = json.load(f)
    except IOError as e:
        ioerror_to_click_exception(e)

    echo_info("*" * 50)
    echo_info(Sid.__logo__)
    echo_info("*" * 50)    
    echo_info("{0}, version {1}".format(Sid.__name__, Sid.__version__).center(50))
    echo_info(NOW.center(50))
    echo_info("Configuration: {0}".format(click.format_filename(config_path)).center(50))
    echo_info("*" * 50)

    if watch == 'y':
        watch_folder(path)        
    elif watch == 'n':
        process_folder(path)
    elif watch == 'q':
        echo('Quitting')
    click.pause('Press any key to quit...')


if __name__ == '__main__':
    main()
