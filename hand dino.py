#Find contours
#image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
try:
# Find contour with maximum area
    contour = max(contours, key=lambda x: cv2.contourArea(x))
# Create bounding rectangle around the contour
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)
# Find convex hull
    hull = cv2.convexHull(contour)
# Draw contour
    drawing = np.zeros(crop_image.shape, np.uint8)
finally:
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
