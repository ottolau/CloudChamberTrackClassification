# CloudChamberTrackClassification

This is a STEM outreach project aiming to identify cloud chamber tracks using machine learning. This repository contains only version 1 of our project, which is the track classification. The repositiry contains a real-time MNIST example cloned from https://github.com/matiascaputti/real-time-MNIST.

## Getting Started

This project is implemented in Keras with TensorFlow as the backend. The code required numpy, scipy, matplotlib, opencv, TensorFlow and Keras to run.

## Preparing training set

### Preprocessing

The training dataset is prepared with the cloud chamber in the Chinese University of Hong Kong. In order to get a better training result, the training video is pre-processed with the following algorithm:

* [BackgroundSubtraction](https://github.com/mwkwok/videoBKGSubtractAndFrameOutput) - The algorithm developed by Raymond Kwok to subtract the background of the video.

### Labelling the training set

Since the same training set can also be used for the object detection, the data is labelled in object detection format and then converts to the format for classification using `convertdataset_classification.py`.

The CSV file with annotations should contain one annotation per line. Images with multiple bounding boxes should use one row per bounding box. Note that indexing for pixel values starts at 0. The expected format of each line is:

```
path/to/image.jpg,x1,y1,x2,y2,class_name
```

The annotation file can be prepared by [labelImg](https://github.com/tzutalin/labelImg). For converting the annotation file to the images and the `mapping.csv` used in this project, put the data under folder `Data` and run:

```
python labelImgXML2CSV.py -i [folderDir]
```

The `mapping.csv` contains the path to the image and the class of it.

### Training

The training is done based on transfer training with the base model VGG16. The expected image format is PNG. The notebook of the training process is in `keras/cloudchamberAI_v1_train.ipynb`


