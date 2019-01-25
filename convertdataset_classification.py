import numpy as np
from PIL import Image
import os

def get_imagecenter(xmin, ymin, xmax, ymax):
    return ((xmin+xmax)/2., (ymin+ymax)/2.)

def get_imagevertex(xcen, ycen, roi_size):
    xmin = xcen - roi_size/2
    ymin = ycen - roi_size/2
    xmax = xcen + roi_size/2
    ymax = ycen + roi_size/2
    return (xmin, ymin, xmax, ymax)

def main(csv_file, roi_size, csv_outputname, path, class_map):
    class_folder = [os.path.join(path, c) for c in class_map.keys()]
    class_counter = [0]*len(class_map.keys())

    for folder in class_folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

    data = np.genfromtxt(csv_file, delimiter = ',', encoding = 'utf-8',
                        names = ['im_name', 'xmin', 'ymin', 'xmax', 'ymax', 'class_name'], 
                        dtype = ['U200', 'f16', 'f16', 'f16', 'f16', 'U200'])

    csv_output = open(csv_outputname, 'w')

    for im_name, xmin, ymin, xmax, ymax, class_name in data:
        im = Image.open(os.path.join(path, im_name))
        width, height = im.size
        xcen, ycen = get_imagecenter(xmin, ymin, xmax, ymax)
        sub_xmin, sub_ymin, sub_xmax, sub_ymax = get_imagevertex(xcen, ycen, roi_size)

        # check if the sub-image outside the margin
        if sub_xmin < 0: continue
        if sub_ymin < 0: continue
        if sub_xmax >= width: continue
        if sub_ymax >= height: continue

        # (left, upper, right, lower), upper left is (0, 0)
        sub_im = im.crop((sub_xmin, sub_ymin, sub_xmax, sub_ymax))
        class_num = class_map[class_name]
        img_savename = "%s/class%s_%05d.png"%(class_folder[class_num], str(class_num), class_counter[class_num])
        sub_im.save(img_savename)
        class_counter[class_num] = class_counter[class_num] + 1
        csv_output.write('%s,%d\n'%(img_savename, class_num))

    csv_output.close()

