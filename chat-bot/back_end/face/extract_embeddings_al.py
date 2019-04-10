# USAGE
# python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle \
#	--detector face_detection_model --embedding-model openface_nn4.small2.v1.t7

# import the necessary packages
from imutils import paths
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
from build_data import *
#from webcam import *
import sys
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import pickle

from PIL import Image
import glob
from imutils.face_utils import FaceAligner


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--embeddings", required=True,
	help="path to output serialized db of facial embeddings")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-s", "--shape", required=True,
	help="path to shape predictor")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])

# load our serialized face embedding model from disk
print("[INFO] loading open face model..")

#create a model for the face image
embedder = faceRecoModel(input_shape=(3, 96, 96))
#load the trained model use the predefined triplet_loss function
load_weights_from_FaceNet(embedder)
print("Weight and Model Loaded!")

print("detector loaded!")

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# initialize our lists of extracted facial embeddings and
# corresponding people names
knownEmbeddings = []
knownNames = []

#load the aligner class with shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape"])
fa = FaceAligner(predictor, desiredFaceWidth=256)


# initialize the total number of faces processed
total = 0

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
        	len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        print(name)
        
        
        # load the image, resize it to have a width of 600 pixels (while
        # maintaining the aspect ratio), and then grab the image
        # dimensions
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=800)
        (h, w) = image.shape[:2]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
        	cv2.resize(image, (300, 300)), 1.0, (300, 300),
        	(104.0, 177.0, 123.0), swapRB=False, crop=False)
        
        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        rects = detector(gray, 2)

        # ensure at least one face was found
        for rect in rects:
            if rect:
                (x,y,h,w) = rect_to_bb(rect)
                face = image[y:y+h,x:x+w]
                #align the face before encoing
                faceAligned = fa.align(image, gray,rect )

                #do another crop on the aligned faces
                gray_aligned = cv2.cvtColor(faceAligned, cv2.COLOR_BGR2GRAY)
                rects_aligned = detector(gray_aligned,2)

                for rect_aligned in rects_aligned:
                    if rect_aligned:
                        (x,y,h,w) = rect_to_bb(rect_aligned)
                        face_crop = faceAligned[y:y+h,x:x+w]
                
                        cv2.imshow("faceAligned",face_crop)
                        cv2.imshow("faceoriginal",face)
        
                        cv2.waitKey(0)
                        #now we have the face ecode the face
                        vec = img_encode(face_crop,embedder)
                        # add the name of the person + corresponding face
                        # embedding to their respective lists
                        knownNames.append(name)
                        knownEmbeddings.append(vec.flatten())
                        total += 1
        
# dump the facial embeddings + names to disk
print("[INFO] serializing {} encodings...".format(total))
data = {"embeddings": knownEmbeddings, "names": knownNames}
f = open(args["embeddings"], "wb")
f.write(pickle.dumps(data))
f.close()
