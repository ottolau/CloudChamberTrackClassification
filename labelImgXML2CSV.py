import xml2csv, convertdataset_classification
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--folderDir', type=str, help='Input data folder directory', dest='folderDir', default='Data')
args = parser.parse_args()

foldersDir = args.folderDir
allClass   = ['alpha', 'beta', 'muon']

class_map  = {c:n for n,c in enumerate(allClass)}
class_mapRev = {n:c for c,n in class_map.items()}
#convert xml to csv, generate a summary and a mapping csv, crop photos
for folder in os.listdir(foldersDir):
    path = os.path.join(foldersDir, folder)
    if os.path.isdir(path):
        print(folder)
        summaryCSV = os.path.join(path, 'summary.csv')
        mappingCSV = os.path.join(path, 'mapping.csv')

        xml2csv.batchxml2csv(path, False, summaryCSV)
        convertdataset_classification.main(summaryCSV, 256, mappingCSV, path, class_map)

#generate merged summary file
tmp = str()
class_paths = {n:list() for n in class_map.values()}
for root, dirs, files in os.walk(foldersDir):
    for file in files:
        if file =='mapping.csv':
            print(root)
            data = np.genfromtxt(os.path.join(root,file), delimiter = ',',
                                 encoding = 'utf-8', 
                                 names = ['im_name', 'class_num'],
                                 dtype = ['U200', 'i8'])
            for row in data:
                class_paths[row['class_num']].append(row['im_name'])

#gen summarys for respectively all particles, and each of the particles
with open(os.path.join(foldersDir, 'mapping_all.csv'), 'w') as f:
    f.write('Id,Target\n')
    for class_num, im_names in class_paths.items():
        with open(os.path.join(foldersDir, 'mapping_%s.csv'%class_mapRev[class_num]), 'w') as g:
            for im_name in im_names:
                f.write('%s,%d\n'%(im_name, class_num))
                g.write('%s,%d\n'%(im_name, class_num))


