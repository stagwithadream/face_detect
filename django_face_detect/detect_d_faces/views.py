from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
import argparse
import cv2
from django.conf import settings
import os

filename= None


STATIC_DIR=settings.STATIC_DIR

def index(request):


    if request.method=='POST' and request.FILES['myfile']:

        myfile=request.FILES['myfile']
        fs=FileSystemStorage()


        filename=fs.save(myfile.name,myfile)
        os.rename(fs.url(filename),os.path.join(STATIC_DIR,'detect_d_faces/images/input/'+fs.url(filename)))
        print(os.path.join(STATIC_DIR,'detect_d_faces/images/input/'+fs.url(filename)))


        net = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR,'detect_d_faces/pyEssentials/deploy.prototxt.txt'),os.path.join(STATIC_DIR,'detect_d_faces/pyEssentials/res10_300x300_ssd_iter_140000.caffemodel') )

        image = cv2.imread(os.path.join(STATIC_DIR,'detect_d_faces/images/input/'+fs.url(filename)))
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        	(300, 300), (104.0, 177.0, 123.0))

        net.setInput(blob)
        detections = net.forward()


        for i in range(0, detections.shape[2]):

        	confidence = detections[0, 0, i, 2]


        	if confidence > 0.5 :

        		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        		(startX, startY, endX, endY) = box.astype("int")

        		text = "{:.2f}%".format(confidence * 100)
        		y = startY - 10 if startY - 10 > 10 else startY + 10
        		cv2.rectangle(image, (startX, startY), (endX, endY),
        			(0, 0, 255), 2)
        		cv2.putText(image, text, (startX, y),
        			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)



        cv2.imwrite(os.path.join(STATIC_DIR,'detect_d_faces/images/output/output.jpg'),image)
        return output_display(request)



    return render(request,'index.html')


def output_display(request):
    return render(request,'displayOutput.html')
