#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64

from LockingQueue import LockingQueue

def extractFrame(fileName, outputBuffer, maxFramesToLoad=9999):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        #put image in buffer
        outputBuffer.put(image)
       
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1
    outputBuffer.put(None)
    print('Frame extraction complete')

def convertToGrayscale(inputBuffer, outputBuffer, maxFramesToLoad=9999):
    count = 0
    frame = inputBuffer.get()
    while count < maxFramesToLoad and frame is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        outputBuffer.put(gray)
        count += 1
        frame = inputBuffer.get()
    outputBuffer.put(None)


def displayFrames(inputBuffer):
    # initialize frame count
    count = 0
    while True:
        # get the next frame
        frame = inputBuffer.get()
        if frame is None:
            break

        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()

# filename of clip to load
filename = 'clip.mp4'

# shared queue  
imageQueue = LockingQueue()
grayQueue = LockingQueue()
# extract the frames
extractThread = threading.Thread(target=extractFrame, args=(filename, imageQueue))
grayThread = threading.Thread(target=convertToGrayscale, args=(imageQueue, grayQueue))
# display the frames
displayThread = threading.Thread(target=displayFrames, args= (grayQueue,))

extractThread.start()
grayThread.start()
displayThread.start()

extractThread.join()
grayThread.join()
displayThread.join()




