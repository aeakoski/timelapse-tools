import pathlib
import struct
import shutil
import os
from tqdm import tqdm
import sys
import numpy as np


import cv2
import json
from matplotlib import pyplot as plt


from PIL import Image, ImageEnhance, ImageStat

def brightness( im_file, isObject = False ):

    if isObject:
        im = im_file.convert('L')
    else:
        im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]

def doHistogram(img_filename):
    #load file as pillow Image
    img = Image.open(img_filename)
    # convert to grayscale
    imgray = img.convert(mode='L')
    #convert to NumPy array
    img_array = np.asarray(imgray)

    """
    STEP 1: Normalized cumulative histogram
    """
    #flatten image array and calculate histogram via binning
    histogram_array = np.bincount(img_array.flatten(), minlength=256)

    #normalize
    num_pixels = np.sum(histogram_array)
    histogram_array = histogram_array/num_pixels

    #normalized cumulative histogram
    chistogram_array = np.cumsum(histogram_array)

    """
    STEP 2: Pixel mapping lookup table
    """
    transform_map = np.floor(255 * chistogram_array).astype(np.uint8)

    """
    STEP 3: Transformation
    """
    # flatten image array into 1D list
    img_list = list(img_array.flatten())

    # transform pixel values to equalize
    eq_img_list = [transform_map[p] for p in img_list]

    # reshape and write back into img_array
    eq_img_array = np.reshape(np.asarray(eq_img_list), img_array.shape)

    #convert NumPy array to pillow Image and write to file
    eq_img = Image.fromarray(eq_img_array, mode='L')
    eq_img.show()



def doBrightness(photoPath):
    b = brightness(photoPath)
    c = 0
    img = Image.open(photoPath)
    threshold = 153
    while ((b < (threshold - 2)) or ((threshold + 2) < b)):
        filter = ImageEnhance.Brightness(img)
        if b < threshold:
            print("up")
            img = filter.enhance(1.03)
        else:
            print("down")
            img = filter.enhance(0.97)

        b = brightness(img, True)
        print(b)
        c+=1
        if 100 < c:
            break

    img_old = Image.open(photoPath)
    Image.fromarray(np.hstack((np.array(img_old),np.array(img)))).show()










def read_this(image_file, gray_scale=False):
    image_src = cv2.imread(image_file)
    if gray_scale:
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
    else:
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
    return image_src


def equalize_this(image_file, with_plot=False, gray_scale=False):
    image_src = read_this(image_file=image_file, gray_scale=gray_scale)
    if not gray_scale:
        r_image, g_image, b_image = cv2.split(image_src)

        r_image_eq = cv2.equalizeHist(r_image)
        g_image_eq = cv2.equalizeHist(g_image)
        b_image_eq = cv2.equalizeHist(b_image)

        image_eq = cv2.merge((r_image_eq, g_image_eq, b_image_eq))
        cmap_val = None
    else:
        image_eq = cv2.equalizeHist(image_src)
        cmap_val = 'gray'

    if with_plot:
        fig = plt.figure(figsize=(10, 20))
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.axis("off")
        ax1.title.set_text('Original')
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.axis("off")
        ax2.title.set_text("Equalized")

        print("Showing iamge")
        ax1.imshow(image_src, cmap=cmap_val)
        ax2.imshow(image_eq, cmap=cmap_val)


        return True
    return image_eq



def main():

    #print(brightness(sys.argv[1]))
    #doBrightness(sys.argv[1])
    #doHistogram(sys.argv[1])
    equalize_this(image_file=sys.argv[1], with_plot=True)
    equalize_this(image_file=sys.argv[2], with_plot=True)
    plt.show()
    print("Done")

main()
