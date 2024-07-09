import cv2

vedio=cv2.vedioCapture(0)

while True:
    ret,frame=vedio.read()
    cv2.imshow("Frame",frame)
    k=cv2.waitkey(1)
    if k==ord('q'):
        break


vedio.release()
cv2.destroyAllWindows()
