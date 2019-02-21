import os, random , argparse, cv2
from shutil import copyfile, rmtree

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--allFramesCSV', type=str, help='path of retinanetAllFrames.csv', dest='allFramesCSV')
parser.add_argument('-r', '--trainRatio', type=float, help='ratio of training samples from 0 to 1', dest='trainRatio')
args = parser.parse_args()

allFramesCSV = args.allFramesCSV
trainRatio = args.trainRatio
with open(allFramesCSV, 'r') as f:
    entries = f.read().splitlines()

random.shuffle(entries)
split = int(trainRatio*len(entries))

trainSet = entries[:split]
testSet = entries[split:]

folder, _ = os.path.split(allFramesCSV)

print('total: ', len(entries))
print('train: ', split)
print('test:  ', len(entries) - split)

with open(os.path.join(folder, 'retinanetAllFrames_TrainingSet.csv'), 'w') as f:
    f.write('\n'.join(trainSet))

with open(os.path.join(folder, 'retinanetAllFrames_TestSet.csv'), 'w') as f:
    f.write('\n'.join(testSet))

