import cv2
import numpy as np
from functions import *
import time

#########################################################################################################################

def Blob_Detect():

    global detected
    detected = False
    
    # Set up the SimpleBlobDetector with default parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 50
    params.maxThreshold = 256

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 500
    #params.maxArea = 10000

    # Filter by Color (black=0)
    params.filterByColor = True
    params.blobColor = 255

    # Filter by Circularity
    params.filterByCircularity = False

    # Filter by Convexity
    params.filterByConvexity = False

    # Filter by InertiaRatio
    params.filterByInertia = False

    # Distance Between Blobs
    params.minDistBetweenBlobs = 0

    # Do detecting
    detector = cv2.SimpleBlobDetector_create(params)

    # find key points for blob detection
    keypoints = detector.detect(image)

    if keypoints:
        detected = True

    # create black screen on which shapes are drawn
    blank = np.zeros((1,1))

    blobs = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return blobs

#########################################################################################################################


# Open communication with Arduino
arduino = Open_Comms()

# Turn on solenoid
arduino.write(str.encode('1'))      

i = 1           # Index for picture numbers
ready = True    # Flag for telling when foram is NEW and not just the same one

# Open video capture (change argument to 0 for live camera feed)
cap = cv2.VideoCapture('SD_foramsPassage.mp4')

# capture first image to get baseline with no forams in frame
ret,image = cap.read()
image = cv2.resize(image,(1200,700))

# shrink focus of image to make contrast better
image = image[10:600, 250:1000]

# get baseline value of initial frame for comparison
initial_pixel_val = (cv2.integral(image))
min_val = int(np.mean(initial_pixel_val))

print(min_val)  # for testing purposes only

# Set min value for deciding if a foram is in frame
min_val += 75000

while True:    
    ret,image = cap.read()
    if not ret:
        break
    image = cv2.resize(image,(1200,700))
    image = image[10:600, 250:1000]
    cv2.imshow('Forams',Blob_Detect())
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    pixel_val = int(np.mean(cv2.integral(image)))
    if (pixel_val > min_val) and (ready == True) and (detected == True):
        cv2.imwrite('Forams_' + str(i) + '.png',image)  # Store image of foram
        print(pixel_val, "Foram Found")         # For testing and debugging purposes only
        time.sleep(0.5)                         # Wait 500 ms
        arduino.write(str.encode('0'))          # Turn solenoid off to let foram pass
        ready = False                           # Set flag to false
        i+=1                                    # Update index for numbering pictures

    # If no forams in frame, reset flags
    if pixel_val < (min_val - 50000):
        arduino.write(str.encode('1'))          # Turn solenoid back on to catch next foram
        ready = True
        detected = False
      
cv2.destroyAllWindows()
arduino.write(str.encode('0'))
