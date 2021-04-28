import numpy as np
import cv2 as cv # OpenCV

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

# line drawing
drawing = False # true if mouse is pressed
pt1_x , pt1_y = None , None
# mouse callback function
def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing

    if event== 1: #cv.EVENT_LBUTTONDOWN
        drawing=True
        pt1_x,pt1_y=x,y

    elif event== 0: #cv.EVENT_MOUSEMOVE
        if drawing==True:
            cv.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=3)
            pt1_x,pt1_y=x,y
    elif event== 4: #cv.EVENT_LBUTTONUP
        drawing=False
        cv.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=3)   

#preprocessing
img = cv.imread("./abraham_sarah_0.jpg") 
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to graysacle
img = cv.cvtColor(img, cv.COLOR_GRAY2RGB) #convert to graysacle

blur_img = cv.GaussianBlur(img,(3,3),cv.BORDER_DEFAULT) #Gaussian Blur the image

# img = np.zeros((512,512,3), np.uint8)
#draw image
cv.namedWindow('image')
cv.setMouseCallback('image',line_drawing)
while(1):
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()