import cv2
import imutils
import numpy as np
from keras.models import load_model

# get the reference to the webcam
CAMERA = cv2.VideoCapture(0)

CAPTURE_WIDTH = 900
ROI_LONG = 400 # Region Of Interest
MARGIN = 50
TOP = MARGIN
RIGHT = CAPTURE_WIDTH - MARGIN
BOTTOM = TOP + ROI_LONG
LEFT = RIGHT - ROI_LONG

model = load_model('keras/mnist_model.h5')
#model = load_model('MNIST_model.h5')

while(True):
    _, frame = CAMERA.read()
    frame = imutils.resize(frame, CAPTURE_WIDTH)
    # frame = cv2.flip(frame, 1)
    (height, width) = frame.shape[:2]

    # Add rectable to original frame
    cv2.rectangle(frame, (LEFT, TOP), (RIGHT, BOTTOM), (0,255,0), 2)

    # Cut ROI and preprocess
    roi = frame[TOP+2:BOTTOM-2, LEFT+2:RIGHT-2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #_, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV) # need fixes
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    #cv2.imshow("ROI", gray)

    # Predict and show prediction
    gray_small = imutils.resize(gray, 28)
    gray_small = gray_small.reshape(1,28,28,1)
    pred = model.predict_classes(gray_small)[0]
    LABEL_TEXT = str(pred)
    LABEL_COLOR = (0,255,0)
    cv2.putText(frame, LABEL_TEXT, (LEFT, TOP-7), cv2.FONT_HERSHEY_SIMPLEX, 1, LABEL_COLOR, 2)
    cv2.imshow("Frame", frame)

    example = np.squeeze(np.array(gray_small*255).astype("uint8"))
    cv2.imshow("ROI", example)

    # if the user pressed "q", then stop looping
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
