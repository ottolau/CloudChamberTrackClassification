'''
This script runs through all sub-folders which has a summary.csv to:
    - copy all entries in the summary.csv and save them in 'retinanetTracks.csv', and
    - pick 100 frames that (i) are not listed in the summary.csv and (ii) no pixel value exceeds 25, and save them in 'retinanetEmptyFrames.csv'
All above are duplicated to 'retinanetAllFrames.csv'
The script also makes a 'retinanetClassMap.csv'.
The last two files are for training.
All files are saved under the input folder.
'''

import os, random , argparse, cv2
from shutil import copyfile, rmtree

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--folderDir', type=str, help='folder that contains all summary.csv in its sub-folder', dest='folderDir')
args = parser.parse_args()

inputDir = args.folderDir
trackFrames = ''
emptyFrames = ''


for item in os.listdir(inputDir):
    path = os.path.join(inputDir, item)
    if not os.path.isdir(path):
        continue
    print(path, '\nEmpty Frame.....0%', end='\r')
    try:
        with open(os.path.join(path, 'summary.csv'), 'r') as f:
            tmp = f.read()
            for line in tmp.split('\n'):
                if line == '':
                    continue
                trackFrames += '%s/%s\n'%(path, line)
        #Randomly pick n = 100 frames not listed
        files = os.listdir(path)
        random.shuffle(files)
        cnt = 0
        try:
            rmtree(os.path.join(path, 'emptyFrames'))
        except:
            pass
        os.mkdir(os.path.join(path, 'emptyFrames'))
        for file in files:
            if file[-4:] == '.png':
                if file[:-4] in tmp:
                    continue
                elif not any((cv2.imread('%s/%s'%(path,file)) > 25).flatten()):
                    emptyFrames += '%s/%s,,,,,\n'%(path, file)
                    copyfile('%s/%s'%(path, file), os.path.join(path, 'emptyFrames', file))
                    cnt += 1
                    if cnt == 100:
                        print('Empty Frame...Done!', end='')
                        break
                    elif cnt%10 == 0:
                        print('Empty Frame.....%d%%'%cnt , end = '\r')
        print('\n')
    except Exception as e:
        print(e)
        continue

with open(os.path.join(inputDir, 'retinanetLabelledTracks.csv'), 'w') as f:
    f.write(trackFrames)

with open(os.path.join(inputDir, 'retinanetEmptyFrames.csv'), 'w') as f:
    f.write(emptyFrames)

with open(os.path.join(inputDir, 'retinanetAllFrames.csv'), 'w') as f:
    f.write(trackFrames+emptyFrames)

with open(os.path.join(inputDir, 'retinanetClassMap.csv'), 'w') as f:
    f.write('alpha,0\nbeta,1\nmuon,2')

