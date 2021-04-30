import numpy as np
import cv2 as cv # OpenCV
# np.set_printoptions(threshold=np.inf)

# drawing = False # true if mouse is pressed
# mode = True # if True, draw rectangle. Press 'm' to toggle to curve
# ix,iy = -1,-1
# line drawing
# drawing = False # true if mouse is pressed
# pt1_x , pt1_y = None , None
# mouse callback function
# def line_drawing(event,x,y,flags,param):
#     global pt1_x,pt1_y,drawing

#     if event== 1: #cv.EVENT_LBUTTONDOWN
#         drawing=True
#         pt1_x,pt1_y=x,y

#     elif event== 0: #cv.EVENT_MOUSEMOVE
#         if drawing==True:
#             cv.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=3)
#             pt1_x,pt1_y=x,y
#     elif event== 4: #cv.EVENT_LBUTTONUP
#         drawing=False
#         cv.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=3)   

def mouse_callback(event,x,y,flags,param):
    if event== 1:   #cv.EVENT_LBUTTONDOWN
         print("New seed at:", x,y)
    elif event== 0: #cv.EVENT_MOUSEMOVE
          print(x,y)

def main():
    #preprocessing
    img = cv.imread("./woman.jpg") 
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to graysacle
    # img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    img = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT) #Gaussian Blur the image

    #edge detection
    kernelH = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]]) 
                    
    kernelV = np.array([[ 1,  2,  1],
                        [ 0,  0,  0],
                        [-1, -2, -1]])

    w,h = img.shape
    imgFinal = np.zeros_like(img)
    for y in range(3, h-2):
        for x in range(3, w-2):
            localPixels = np.array([[ img[x-1][y-1],  img[x][y-1],  img[x+1][y-1]],
                                    [ img[x-1][y],    img[x][y],    img[x+1][y]  ],
                                    [ img[x-1][y+1],  img[x][y+1],  img[x+1][y+1]]])
            
            transformPixelsV = kernelV * localPixels
            scoreV = transformPixelsV.sum()/4
            
            transformPixelsH = kernelH * localPixels
            scoreH = transformPixelsH.sum()/4
            
            imgFinal[x][y] = ( scoreV**2 + scoreH**2 )**0.5

    imgFinal = imgFinal/imgFinal.max()

    #draw image
    cv.namedWindow('image')

    cv.setMouseCallback('image', mouse_callback)
    # scissorCoords = list(x, y) ## this is a list of coordinates on the scissor path; starts with mouse x, y

    while(True):
        cv.imshow('image',imgFinal)
        if cv.waitKey(20) & 0xFF == 27:
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()