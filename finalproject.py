import numpy as np
import cv2 as cv # OpenCV
import enum

from graph import Graph
from fill import FloodFill
from bresenham import bresenham

tool = 1

readyToDraw = False
dijkstraCompleted = False
allPaths = []
seed_x = seed_y = None
        

def mouse_callback(event,x,y,flags,param):
    global img
    global imgOG
    global g
    global allPaths
    global readyToDraw
    global dijkstraCompleted
    global seed_x 
    global seed_y
    global tool

    # h,w = imgFinal.shape
    
    if event== 1: 
        if tool == 0: 
            if readyToDraw:   #cv.EVENT_LBUTTONDOWN
                
                imgOG = img.copy()
                dijkstraCompleted = False
                seed_x = x
                seed_y = y
                seed = x+y*w
                print("New seed at:", x,y, seed)
                
                i = seed_x+seed_y*w
                while(not len(g.parent) == 0 and g.parent[i] != -1):
                    allPaths.append(i)
                    i = g.parent[i]

                print("performing dijkstra")
                g.parent = []
                g.dijkstra(seed)
                dijkstraCompleted = True
                print("dijkstra complete")
                
            else:
                print("filling x,y")
                f = FloodFill(w,h)
                f.fill(allPaths, x, y, w, h, img)
                print("floodfill completed")
                for i in f.filledCells:
                    pix_y = i // w
                    pix_x = i - pix_y*w
                    img[pix_y][pix_x] = (0,0,255)
        
        elif tool == 1:
            if(seed_x != None and seed_y != None):
                print("running bresenham", seed_x, seed_y, x, y)
                bresenham(seed_x, seed_y, x, y, img)
            seed_x = x
            seed_y = y
            


    elif event== 0: #cv.EVENT_MOUSEMOVE
        if dijkstraCompleted :
            i = x+y*w
            img = imgOG.copy() #reset image
            cv.circle(img,(seed_x,seed_y),5,(0,255,0),-1)

            while(not len(g.parent) == 0 and g.parent[i] != -1):
                i = g.parent[i]
                pix_y = i // w
                pix_x = i - pix_y*w
                cv.circle(img,(pix_x,pix_y),1,(255,0,0),-1) #draw path 
    
    elif event== 2: #cv.EVENT_RBUTTONDOWN
        print("path completed!")
        imgOG = img.copy()
        dijkstraCompleted = False
        readyToDraw = False
        i = seed_x+seed_y*w
        while(not len(g.parent) == 0 and g.parent[i] != -1):
            allPaths.append(i)
            i = g.parent[i]
        # print(allPaths)




########## preprocessing ##########
print("loading image")
img = cv.imread("./imgs/owl.png") 
imgOG = cv.imread("./imgs/owl.png") 
imgFinal = []

print("preprocessing")
img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert to graysacle
img2 = cv.GaussianBlur(img2,(5,5),cv.BORDER_DEFAULT) # Gaussian Blur the image
print("preprocessing completed")

if(tool == 0):
    ######### edge detection ##########
    print("edge detection")
    #Horizontal and Vertical Sobel kernels
    kernelH = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]]) 
                    
    kernelV = np.array([[ 1,  2,  1],
                        [ 0,  0,  0],
                        [-1, -2, -1]])

    #aply kernels to image
    w,h = img2.shape
    imgFinal = np.zeros_like(img2)
    for y in range(3, h-2):
        for x in range(3, w-2):
            localPixels = np.array([[ img2[x-1][y-1],  img2[x][y-1],  img2[x+1][y-1]],
                                    [ img2[x-1][y],    img2[x][y],    img2[x+1][y]  ],
                                    [ img2[x-1][y+1],  img2[x][y+1],  img2[x+1][y+1]]])
            
            transformPixelsV = kernelV * localPixels
            scoreV = transformPixelsV.sum()
            
            transformPixelsH = kernelH * localPixels
            scoreH = transformPixelsH.sum()
            
            imgFinal[x][y] = ( scoreV**2 + scoreH**2 )**0.5

    imgFinal = imgFinal.max()-imgFinal
    print("edge detection completed")


    ######### scissoring graph ##########
    print("creating graph for scissoring")
    g = Graph(h*w)
    for y in range(h):
        for x in range(w):
            
            for b in range(y-1, y+2):
                for a in range(x-1, x+2):
                    if (a < 0 or a >= w or b < 0 or b >= h or (y == b and x == a)): # Check that [row, col] is not out of bounds
                        continue
                    g.addEdge(y*w+x, b*w+a, abs(imgFinal[b][a]))
    print("graph for scissoring completed")


######### rendering ##########
readyToDraw = True
cv.namedWindow('image post detection')
cv.namedWindow('image')

while(True):
    
    cv.setMouseCallback('image', mouse_callback)
    
    if cv.waitKey(20) & 0xFF == 27:
        break
    
    cv.imshow('image',img)
    # cv.imshow('image post detection',imgFinal)

cv.destroyAllWindows()


# def main():
# if __name__ == "__main__":
#     main()