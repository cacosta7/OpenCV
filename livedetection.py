# import the opencv library
import cv2
import numpy as np 

params = cv2.SimpleBlobDetector_Params()
# parameters for screws
params.maxArea = 1000
params.minArea = 125
params.minThreshold = 55
params.maxThreshold = 150
params.filterByCircularity = False
params.filterByInertia = True
params.maxInertiaRatio = .75
params.minInertiaRatio = .2
params.filterByConvexity = False

#sets up the detector to detect the blobs
detector = cv2.SimpleBlobDetector_create(params)

# define a video capture object
vid = cv2.VideoCapture(0)

while(True):
	
	# Capture the video frame
	# by frame
	ret, frame = vid.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#detect the blobs
	keypoints = detector.detect(gray)

	#Convert keypoints to a list of (x, y) tuples
	points = [k.pt for k in keypoints]

	#Draw the contours of the blobs
	contours = np.array([points], dtype=np.int32)
	cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

	#Draw Red circles around detected blob
	#imgKeyPts = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	#draw the contours of the blobs
	frameContours = frame.copy()
	#cv2.drawContours(frameContours, contours, -1, (0, 255, 0), 1)

	#Counts all of the objects found
	#counter = str(len(keypoints))
	#font = cv2.FONT_HERSHEY_SIMPLEX
	#cv2.putText(imgKeyPts, counter, (7,60), font, 2, (0,255,0), 3, cv2.LINE_AA)
	
	# Display the resulting frame
	cv2.imshow('Blobs', frame)

	# c is used to break the loop and leave us with the last captured frame
	if cv2.waitKey(1) & 0xFF == ord('c'):
		break

cv2.waitKey()

# After the loop release the cap object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()