# This file contains the original code I used to detect object by using the contour area

import cv2

vid = cv2.VideoCapture(0)
_ , img = vid.read()
# creation of the pattern
# draws a bounding box over the image in order to find what to track
pattern = cv2.selectROI(img)
trained = img[int(pattern[1]):int(pattern[1]+pattern[3]),int(pattern[0]):int(pattern[0]+pattern[2])]
#cv2.imshow('cropped image', trained)
cv2.waitKey()
#cv2.destroyAllWindows()

# this function is used to find the contours in an image
def imageProcess(image):
    # turn the image gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur the grayed image
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    # canny the edges in the grayed/blurred image
    canny = cv2.Canny(blur, 55, 255)
    cv2.imshow('canny', canny)
    # find the contours in the processed image
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

base_contour = imageProcess(trained)

# wasn't able to to find the area of the contour until I added this for loop
for contour in base_contour:
    base_area = cv2.contourArea(contour)
    print('Contour area:', base_area)

    # Draw contour on image
    cv2.drawContours(trained, [contour], 0, (0, 255, 0), 1)
cv2.imshow("base",trained)
base_area = cv2.contourArea(contour[0])


while(True):
    # Capture the video frame by frame
    ret, frame = vid.read()

    # finds the countors
    contours = imageProcess(frame)

    # determines if the countors found in the images fit the criteria
    counter = 0
    for contour in contours:
        area = cv2.contourArea(contour)

        # if the contour fits, then draw it
        if base_area*.5 < area < base_area*1.5:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 1)
            counter = counter + 1

    #Counts all of the objects found and displays it
    counter = str(counter)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, counter, (7,60), font, 2, (0,255,0), 3, cv2.LINE_AA)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

print(f'{len(contours)} matches found')

cv2.waitKey()

# After the loop release the cap object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()

# create more functions, potentially classes
# add more object filtering to make the detection more accurate
# add functionality that allows the user to train a new pattern and track that pattern at the same time as other different patterns
# preferably also add a way to delete a trained pattern as well.
    # maybe use a list to keep track of the trained patterns??
# find a way to save the data of trained object so that we can pull that save data out and have the program automatically detect what that object is