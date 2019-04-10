from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.engine.topology import Layer
from keras import backend as K
K.set_image_data_format('channels_first')
import cv2
import os
import numpy as np
from numpy import genfromtxt
import pandas as pd
import tensorflow as tf
from fr_utils import *
from inception_blocks_v2 import *
#from webcam import *
import sys
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.face_utils import rect_to_bb
from imutils import paths
import argparse
import imutils
import dlib
import pickle
#=============================================================================
#given a new image ,and all the existing encoded of the authorised people ,find out
#who thie person is or none of the existing perons
def who_is_it(img,recognizer,le, model):
    encoding = img_encode(img,model) #image is a croped cv read array
    preds = recognizer.predict_proba(encoding)[0]
    j = np.argmax(preds)
    proba = preds[j]
    name = le.classes_[j]
    
    return name, proba 

#------------------------------------------------------------------------------------
def recognize_faces_in_cam(image,recognizer,le,detector,model):
    cv2.namedWindow("Face Recognizer")
    font = cv2.FONT_HERSHEY_SIMPLEX#set the font
    
    frame = cv2.imread(image)
    height, width, channels = frame.shape

    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]

    # construct a blob from the image
    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    detector.setInput(imageBlob)
    detections = detector.forward()
    all_identities = {} #to store the result of {person:prob,...}

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > args["confidence"]:
            # compute the (x, y)-coordinates of the bounding box for
            # the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            # extract the face ROI
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            
            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
            	continue
            
            #affine align the image 
            identity, prob= who_is_it(face,recognizer,le, model)
            
            if identity is not None:
                text = "{}: {:.2f}%".format(identity, prob * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                frame = cv2.rectangle(frame,(startX, startY),(endX, endY),(255,255,255),2)
                cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                all_identities[identity] = prob
        
        key = cv2.waitKey(100)
        cv2.imshow("Face Recognizer", frame)
        
        if key == 27: # exit on ESC
            break

    return all_identities

#cv2.destroyAllWindows()

#==================================================================================
## construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
args = vars(ap.parse_args())

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())
print("Rcogniser deserilised!")

protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
print("detectro loaded!")

#create a model for the face image
FRmodel = faceRecoModel(input_shape=(3, 96, 96))

#load the trained model use the predefined triplet_loss function
load_weights_from_FaceNet(FRmodel)
print("Weight and Model Loaded!")


imagePaths = list(paths.list_images("test"))
correct = 0 #keep track of the correct image recognised
total_rec = 0 #keep track of the total image recognised

for (i, imagePath) in enumerate(imagePaths):
    name = imagePath.split(os.path.sep)[-2] #get the name of the person (the dir name)
    #return dict of {person:prob,...}
    all_identities = recognize_faces_in_cam(imagePath,recognizer,le,detector,FRmodel)
    for person in all_identities: #check if recognised face contains the correct person
        print(name," get recognised as:", person,"with prb:",all_identities[person])
        if name == person:
            correct += 1 #correct rec
    total_rec += 1

#finish all the rec calculate total
print("Test Finished with accuracy of:",round(correct/total_rec,2))








