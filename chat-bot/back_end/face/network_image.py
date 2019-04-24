from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import json
#from face_lib import *
from imageio import imread
import io
from flask_cors import CORS
import ast

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


#usage
# python network_image.py -d face_detection_model -r output/recognizer.pickle -l output/le.pickle
#=============================================================================
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
print("[Info] Rcogniser Loaded!")

protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
print("[Info] Detector Loaded!")

#set up the global graph
global graph
graph = tf.get_default_graph()

#create a model for the face image
FRmodel = faceRecoModel(input_shape=(3, 96, 96))

#load the trained model use the predefined triplet_loss function
load_weights_from_FaceNet(FRmodel)
print("[Info] Weight and Model Loaded!")
print("[Info] Face Verfication Server Started...")

#user name and id gloab dict
user_id = {"erik":1,"milo":2,"zen":3,"allan":4}
detect_confidence = 0.7 #confidence threshhold for detecting face

#=============================================================================
#take in a one dim array and will fold into (h,w) 2d np array
def fold(arr,h,w):
    arr = np.array(arr)
    arr=np.expand_dims(arr, axis=1)
    arr = arr.reshape(h,w)
    return arr

#------------------------------------------------------------------------------------
#given a new image ,and all the existing encoded of the authorised people ,find out
#who thie person is or none of the existing perons
def who_is_it(img,recognizer,le, model):
    with graph.as_default():
        encoding = img_encode(img,model) #image is a croped cv read array
    preds = recognizer.predict_proba(encoding)[0]
    j = np.argmax(preds)
    proba = preds[j]
    name = le.classes_[j]
    
    return name, proba 

#------------------------------------------------------------------------------------
def recognize_faces_in_img(image,recognizer,le,detector,model):
    #cv2.namedWindow("Face Recognizer")
    font = cv2.FONT_HERSHEY_SIMPLEX#set the font
    frame = image.astype(np.float32)
    height, width, channels = frame.shape

    #cv2.imwrite("loaded.jpeg",frame)

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
        if confidence > detect_confidence: 
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
            
            cv2.imwrite("face.jpeg",face)
            #affine align the image 
            identity, prob= who_is_it(face,recognizer,le, model)
            
            if identity is not None:
                text = "{}: {:.2f}%".format(identity, prob * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                frame = cv2.rectangle(frame,(startX, startY),(endX, endY),(255,255,255),2)
                cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                all_identities[identity] = prob

        cv2.imwrite("recognised.jpeg",frame) 

    return all_identities
#========================================================================================
app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def network():
    #check the request's flag 
    #req = request.get_json(silent=True, force=True) #req is a dict of returned jaso
    req = request.form.to_dict() 
    #print(req)
    r = ast.literal_eval(req['r'])
    g = ast.literal_eval(req ['g'])
    b = ast.literal_eval(req['b'])
    h = int(req['height'])
    w = int(req['width'])

    rr = fold(r,h,w)
    gg = fold(g,h,w)
    bb = fold(b,h,w)
    img_arr = np.dstack((bb,gg,rr))

    #print("Received image shape of:",img_arr.shape)
    #cv2.imwrite("received.jpeg",img_arr)

    #now we have the array of the image and need to pass to the verification network for recoginition
    all_identities = recognize_faces_in_img(img_arr,recognizer,le,detector,FRmodel)
    print(all_identities)

    
    answer= {}
    for person in all_identities: #check if recognised face contains the correct person
        answer ={"user":{"userName":person,"userID":user_id[person]}}  

        print("[Info] "person ,"is recognised with prob of", all_identities[person])
        print("[Info] This return to the front end:",answer)

        answer = json.dumps(answer) 
        return  jsonify(answer)#only return the first result
    
    #there is no person detected 
    return None


#=============================================================================
if __name__ == '__main__':
    app.run(debug=True)
