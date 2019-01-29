# import the necessary packages
import argparse
import cv2
import numpy as np
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from keras.models import load_model

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = [(-1,-1),(-1,-1)]
cropping = False
roi_size = 256
vgg16_shape = 224
skip_evaluation = False
model = load_model('keras/ccAI_model.h5')
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(vgg16_shape, vgg16_shape, 3)) 

allClass   = ['alpha', 'beta', 'muon']
class_map  = {n:c for n,c in enumerate(allClass)}

def crop_square(event, x, y, flags, param):
	# grab references to the global variables
    global refPt, cropping
    refPt = [(x-roi_size/2, y-roi_size/2)]
    refPt.append((x+roi_size/2, y+roi_size/2))

def evaluate_class(roi):
    img = roi[:,:,:3]
    test_image = np.squeeze(cv2.resize(roi, (vgg16_shape, vgg16_shape), interpolation=cv2.INTER_LINEAR)*255).astype(int)
    test_image = np.expand_dims(test_image, axis=0)
    test_image = preprocess_input(test_image, mode='tf')
    test_image = base_model.predict(test_image)
    model_inputshape = test_image.shape[1]*test_image.shape[2]*test_image.shape[3]
    test_image = test_image.reshape(test_image.shape[0], model_inputshape)
    test_image = test_image/test_image.max()
    pred = model.predict_classes(test_image)[0]
    LABEL_TEXT = class_map[pred]
    print LABEL_TEXT
    LABEL_COLOR = (0,255,0)
    cv2.putText(roi, LABEL_TEXT, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, LABEL_COLOR, 2)
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
 
# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", crop_square)
 
# keep looping until the 'q' key is pressed
while True:
    # reset to the plain image
    image = clone.copy()
	# draw a rectangle around the region of interest
    cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

	# if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
	    image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
	    break

    # if the user pressed "q", then stop looping
    if key == ord("q"):
        skip_evaluation = True
        break

# if there are two reference points, then crop the region of interest
# from teh image and display it
if not skip_evaluation and len(refPt) == 2:
    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    evaluate_class(roi)
 
# close all open windows
cv2.destroyAllWindows()

