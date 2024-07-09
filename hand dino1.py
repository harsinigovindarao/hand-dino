#Find contours
#image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('gradient.png',0)
ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
try:
# Find contour with maximum area
    contour = max(contours, key=lambda x: cv2.contourArea(x))
# Create bounding rectangle around the contour
    x, y, w, h = cv2.boundingRect(contour)
finally:
    cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)
# Find convex hull
hull = cv2.convexHull(contour)
# Draw contour
drawing = np.zeros(crop_image.shape, np.uint8)
cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)
# Fi convexity defects
hull = cv2.convexHull(contour, returnPoints=False)
defects = cv2.convexityDefects(contour, hull)
# Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger
# tips) for all defects
count_defects = 0
for i in range(defects.shape[0]):
    s, e, f, d = defects[i, 0]
start = tuple(contour[s][0])
end = tuple(contour[e][0])
far = tuple(contour[f][0])
a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14
# if angle >= 90 draw a circle at the far point
if angle <= 90:
    count_defects += 1
cv2.circle(crop_image, far, 1, [0, 0, 255], -1)
cv2.line(crop_image, start, end, [0, 255, 0], 2)
# Press SPACE if condition is match
if count_defects >= 4:
    pyautogui.press('space')
cv2.putText(frame, "JUMP", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
