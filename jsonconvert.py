# Haven't started yet but this is where I will be adding the json capabilities
# this is just copied code from listdetect.py for now

import cv2

class Object:
    
    def __init__(self, name):
        self.name = name
        frame = None
        pattern = None
        trained = None
        contour = None
        area = None

    def imageProcess(self):
        # turn the image gray
        gray = cv2.cvtColor(self.trained, cv2.COLOR_BGR2GRAY)
        # blur the grayed image
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        # canny the edges in the grayed/blurred image
        canny = cv2.Canny(blur, 50, 255)
        cv2.imshow('canny', canny)
        # find the contours in the processed image
        contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    def trainPatttern(self):
        # select Region of Interest
        # allows the user to put a bounding box on an image
        self.pattern = cv2.selectROI(self.frame)
        # saves the image in the bounding box to trained
        self.trained = self.frame[int(self.pattern[1]):int(self.pattern[1]+self.pattern[3]),
                                int(self.pattern[0]):int(self.pattern[0]+self.pattern[2])]
        # the image is then processed
        self.contour = self.imageProcess()
        # the area of the image is found
        self.findArea()

    def findArea(self):
        for contour in self.contour:
            base_area = cv2.contourArea(contour)
            print('Contour area:', base_area)

            # Draw contour on image
            cv2.drawContours(self.trained, [contour], 0, (0, 255, 0), 1)
        cv2.imshow(self.name,self.trained)
        self.area = cv2.contourArea(self.contour[0])

vid = cv2.VideoCapture(0)
# creates an new objects for the area that will be searched
areaDetect = Object("SearchRegion")
search = False

patternList = []

while(True):
    # Capture the video frame by frame
    ret, frame = vid.read()
    areaDetect.trained = frame

    # trains a new pattern
    if cv2.waitKey(1) & 0xFF == ord('a'):
        name = input("Enter name for the new object: ")
        obj = Object(name)
        obj.frame = frame
        obj.trainPatttern()
        patternList.append(obj)
        search = True

    if(search):
    # finds the countors
        contours = areaDetect.imageProcess()
        
        # iterates through each object in the list
        for obj in patternList:
            # determines if the countors found in the images fit the criteria
            for contour in contours:
                area = cv2.contourArea(contour)

                # if the contour fits, then draw it
                if obj.area*.85 < area < obj.area*1.15:
                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 1)
        
    cv2.imshow("frame", frame)

    # end the program
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

for obj in patternList:
    print(obj.name, sep=' ')

# After the loop release the cap object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()