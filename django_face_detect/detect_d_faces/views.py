from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
import argparse
import cv2

filename= None



# Create your views here.
def index(request):


    if request.method=='POST' and request.FILES['myfile']:

        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)


        # construct the argument parse and parse the arguments


        # load our serialized model from disk

        net = cv2.dnn.readNetFromCaffe('/home/sairam/Desktop/face_detect/django_face_detect/detect_d_faces/deploy.prototxt.txt','/home/sairam/Desktop/face_detect/django_face_detect/detect_d_faces/res10_300x300_ssd_iter_140000.caffemodel' )

        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        image = cv2.imread('/home/sairam/Desktop/face_detect/django_face_detect/'+fs.url(filename))
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        	(300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the detections and
        # predictions

        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
        	# extract the confidence (i.e., probability) associated with the
        	# prediction
        	confidence = detections[0, 0, i, 2]

        	# filter out weak detections by ensuring the `confidence` is
        	# greater than the minimum confidence
        	if confidence > 0.5 :
        		# compute the (x, y)-coordinates of the bounding box for the
        		# object
        		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        		(startX, startY, endX, endY) = box.astype("int")

        		# draw the bounding box of the face along with the associated
        		# probability
        		text = "{:.2f}%".format(confidence * 100)
        		y = startY - 10 if startY - 10 > 10 else startY + 10
        		cv2.rectangle(image, (startX, startY), (endX, endY),
        			(0, 0, 255), 2)
        		cv2.putText(image, text, (startX, y),
        			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # show the output image
        cv2.imshow("Output", image)
        cv2.imwrite("output"+fs.url(filename),image)
        fs.delete(filename)
        cv2.waitKey(0)


    return render(request,'index.html')
