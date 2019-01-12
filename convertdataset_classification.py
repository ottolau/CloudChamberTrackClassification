import numpy as np
from PIL import Image

def get_imagecenter(xmin, ymin, xmax, ymax):
    return ((xmin+xmax)/2., (ymin+ymax)/2.)

def get_imagevertex(xcen, ycen, roi_size):
    xmin = xcen - roi_size/2
    ymin = ycen - roi_size/2
    xmax = xcen + roi_size/2
    ymax = ycen + roi_size/2
    return (xmin, ymin, xmax, ymax)

def main():
    csv_file = 
    class_map = {"alpha": 0, "beta": 1, "muon": 2}
    class_folder = ["", "", ""]
    class_counter = [0, 0, 0]

    roi_size = 256

    csv_input = np.genfromtxt(csv_file, delimiter=',', unpack=True)

    for im_name, xmin, ymin, xmax, ymax, class_name in csv_input:
        im = Image.open(im_name)
        xmax, ymax = im.size
        xcen, ycen = get_imagecenter(xmin, ymin, xmax, ymax)
        sub_xmin, sub_ymin, sub_xmax, sub_ymax = get_imagevertex(xcen, ycen, roi_size)
        # check if the sub-image outside the margin
        if sub_xmin < 0: continue
        if sub_ymin < 0: continue
        if sub_xmax > xmax: continue
        if sub_ymax > ymax: continue

        # (left, upper, right, lower)
        sub_im = im.crop((sub_xmin, sub_ymax, sub_xmax, sub_ymin))
        sub_im.save("%s/class%s_%05d.png"%(class_folder[class_map[class_name]], str(class_map[class_name]), class_counter[class_map[class_name]])
        class_counter[class_map[class_name]] = class_counter[class_map[class_name]] + 1


if __name__ == "__main__":
    main()

