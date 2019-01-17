import numpy as np
from PIL import Image
import os

#path = 'Data/V_20190114_183508_OC0'
path = 'Data/First100_FromWing'

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
    class_folder = [path + '/alpha', path + '/beta', path + '/muon']
    class_counter = [0, 0, 0]

    list_im_name, list_xmin, list_ymin, list_xmax, list_ymax, list_class_name = np.loadtxt(csv_file, delimiter=',', dtype={'names': ('im_name', 'xmin', 'ymin', 'xmax', 'ymax', 'class_name'), 'formats': ('|S100', np.float, np.float, np.float, np.float, '|S15')}, unpack=True)

    csv_output = open(csv_outputname, 'w+')
    for im_name, xmin, ymin, xmax, ymax, class_name in zip(list_im_name, list_xmin, list_ymin, list_xmax, list_ymax, list_class_name):
        im = Image.open(path + '/' + im_name)
        width, height = im.size
        xcen, ycen = get_imagecenter(xmin, ymin, xmax, ymax)
        sub_xmin, sub_ymin, sub_xmax, sub_ymax = get_imagevertex(xcen, ycen, roi_size)
        # check if the sub-image outside the margin
        if sub_xmin < 0: continue
        if sub_ymin < 0: continue
        if sub_xmax > width: continue
        if sub_ymax > height: continue

        # (left, upper, right, lower), upper left is (0, 0)
        sub_im = im.crop((sub_xmin, sub_ymin, sub_xmax, sub_ymax))
        class_num = class_map[class_name]
        img_savename = "%s/class%s_%05d.png"%(class_folder[class_num], str(class_num), class_counter[class_num])
        sub_im.save(img_savename)
        class_counter[class_num] = class_counter[class_num] + 1
        csv_output.write('%s,%d\n'%(img_savename, class_num))

    csv_output.close()

if __name__ == "__main__":
    tmp = ''
    #path = '/home/raymondkwok/data/cloudchamber/V_20190114_183508_OC0'
    for root, dirs, files in os.walk(path):
        for f in files:
            if f[-4:] == '.csv':
                with open(path + '/' + f,'r') as handle:
                    for line in handle.readlines()[1:]:
                        tmp += line.replace('\n','')
                        tmp += '\n'
    with open(path + '/summary.csv','w') as handle:
        handle.write(tmp)
    csv_file = path + '/summary.csv'
    roi_size = 256
    output_csv = path + '/mapping.csv'
    main(csv_file, roi_size, output_csv)

