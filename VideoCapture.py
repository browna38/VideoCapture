#!/usr/bin/env python

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import numpy

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

exceptedDate = 'Aurora Aerial'
# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()
csv.write("Date,Hour, Minute, Second, MicroSec,Name,x,y\n")

while(True):
  ret, frame = cap.read()

  if ret == True: 
    frame = imutils.resize(frame, frame_width)
    
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
    for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        center = "%d , %d" % ((x+w)/2,(y+h)/2)
        text = text + center
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
        timenow = datetime.datetime.now()
        if barcodeData == exceptedDate:
            csv.write("{},{},{},{},{},{},{},{}\n".format(datetime.date.today(),timenow.hour,timenow.minute,timenow.second,timenow.microsecond,
                barcodeData,(x+w)/2,(y+h)/2))
            csv.flush()
            found.add(barcodeData)
    
    # Write the frame into the file 'output.avi'
    out.write(frame)

    # Display the resulting frame    
    cv2.imshow('frame',frame)

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break  

# When everything done, release the video capture and video write objects
csv.close()
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows() 