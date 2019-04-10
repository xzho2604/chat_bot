from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import cv2
import numpy as np
from face_lib import *

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
print("Rcogniser Loaded!")

protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
print("Detector loaded!")

#create a model for the face image
FRmodel = faceRecoModel(input_shape=(3, 96, 96))

#load the trained model use the predefined triplet_loss function
load_weights_from_FaceNet(FRmodel)
print("Weight and Model Loaded!")
print("Listening to the incoming request...")


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





#=============================================================================
app = Flask(__name__)
@app.route('/', methods=['POST'])
def network():
    #check the request's flag 
    req = request.get_json(silent=True, force=True) #req is a dict of returned jaso
    print(req)

    #show the received image
    cv2.imshow("Received Image",img)
    cv2.waitKey(0)

    #if request is to verify image check image img
    all_identities = recognize_faces_in_img(img,recognizer,le,detector,FRmodel)
    for person in all_identities: #check if recognised face contains the correct person
        print(person ,"is recognised with prob of", all_identities[person])
        #identify person and send back the result to the front end
        return "verified"

    #if the request is the feed back check feed back
    #if anser is yes keep going
    #TO DO

    #if answer is no encode the image and append to the embedding.pick and call train
    #TO DO




    return "got it" 



#=============================================================================
if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))
    app.run(debug=True)
 
