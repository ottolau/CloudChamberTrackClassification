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

def main(csv_file, roi_size, csv_outputname):
    class_map = {"alpha": 0, "beta": 1, "muon": 2}
    class_folder = ["", "", ""]
    class_counter = [0, 0, 0]

    csv_input = np.loadtxt(csv_file, delimiter=',', dtype={'names': ('im_name', 'xmin', 'ymin', 'xmax', 'ymax', 'class_name'), 'formats': ('|S15', np.float, np.float, np.float, np.float, '|S15')}, unpack=True)

    csv_output = open(csv_outputname, 'w')
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

        # (left, upper, right, lower), upper left is (0, 0)
        sub_im = im.crop((sub_xmin, sub_ymin, sub_xmax, sub_ymax))
        class_num = class_map[class_name]
        img_savename = "%s/class%s_%05d.png"%(class_folder[class_num], str(class_num), class_counter[class_num]
        sub_im.save(img_savename)
        class_counter[class_num] = class_counter[class_num] + 1
        csv_output.write('%s,%d\n'%(img_savename, class_num))

     csv_output.close()

if __name__ == "__main__":
    csv_file = ''
    roi_size = 256
    output_csv = ''
    main(csv_file, roi_size, output_csv)

