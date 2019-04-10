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
import argparse
import imutils
import dlib
import pickle
from imutils.face_utils import FaceAligner
#=============================================================================
#given a new image ,and all the existing encoded of the authorised people ,find out
#who thie person is or none of the existing perons
def who_is_it(img,recognizer,le, model):

    #encoding = img_to_encoding(img,model) # image is a path
    encoding = img_encode(img,model) #image is a croped cv read array
    #encoding = encoding.flatten()

    # perform classification to recognize the face
    preds = recognizer.predict_proba(encoding)[0]
    j = np.argmax(preds)
    proba = preds[j]
    name = le.classes_[j]
    
    return name, proba 

#------------------------------------------------------------------------------------
def recognize_faces_in_cam(recognizer,le,detector,model):
    cv2.namedWindow("Face Recognizer")
    vc = cv2.VideoCapture(0)

    predictor = dlib.shape_predictor(args["shape"])
    fa = FaceAligner(predictor, desiredFaceWidth=256)

    #load the front face classifier
    font = cv2.FONT_HERSHEY_SIMPLEX
    while vc.isOpened():
        _, frame = vc.read()
        height, width, channels = frame.shape

        frame = imutils.resize(frame, width=800)
        (h, w) = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


	# construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
        rects = detector(gray,2)

	# loop over the detections
        for rect in rects:
            if rect:
                faceAligned = fa.align(frame, gray, rect)
                (x,y,h,w) = rect_to_bb(rect)

                startY = y
                endY = y+h 
                startX=x
                endX=x+w
                
                face = frame[startY:endY, startX:endX]

                #cv2.imshow("Face Alighed", faceAligned)
                #cv2.imshow("Face Original", face)

                identity, prob= who_is_it(faceAligned,recognizer,le, model)
                
                if identity is not None:
                    text = "{}: {:.2f}%".format(identity, prob * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    frame = cv2.rectangle(frame,(startX, startY),(endX, endY),(255,255,255),2)
                    cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            
        key = cv2.waitKey(100)
        cv2.imshow("Face Recognizer", frame)
        
        if key == 27: # exit on ESC
            break

    vc.release()
    cv2.destroyAllWindows()

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
ap.add_argument("-s", "--shape", required=True,
	help="path to label shape predictor")
args = vars(ap.parse_args())

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())
print("Rcogniser deserilised!")

detector = dlib.get_frontal_face_detector()
print("detectro loaded!")

#create a model for the face image
FRmodel = faceRecoModel(input_shape=(3, 96, 96))

#load the trained model use the predefined triplet_loss function
load_weights_from_FaceNet(FRmodel)
print("Weight and Model Loaded!")

recognize_faces_in_cam(recognizer,le,detector,FRmodel)





