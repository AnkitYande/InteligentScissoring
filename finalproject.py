import numpy as np
import cv2 as cv # OpenCV
import enum

from graph import Graph
from fill import FloodFill
from bresenham import bresenham

tool = 0

readyToDraw = False
dijkstraCompleted = False
allPaths = []
selectedPix = []
seed_x = seed_y = None
delta_x = delta_y = 0


def mouse_callback(event,x,y,flags,param):
    global img
    global imgOG
    global imgDest
    global g
    global allPaths
    global readyToDraw
    global dijkstraCompleted
    global selectedPix
    global seed_x 
    global seed_y
    global tool

    h,w,d = img.shape
    
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
                f.fill(allPaths, x, y, w, h)
                print("floodfill completed")
                selectedPix = f.selectedCells
                for i in f.selectedCells:
                    pix_y = i // w
                    pix_x = i - pix_y*w
                    imgDest[pix_y][pix_x] = img[pix_y][pix_x]
                    # img[pix_y][pix_x] = (255,255,255)

        elif tool == 1:
            if readyToDraw: 
                if(seed_x != None and seed_y != None):
                    print("running bresenham", seed_x, seed_y, x, y)
                    bresenham(seed_x, seed_y, x, y, w, h, allPaths)
                    for i in allPaths:
                        pix_y = i // w
                        pix_x = i - pix_y*w
                        img[pix_x][pix_y] = (255,0,255)
                else:
                    allPaths.append( y*w+x )

                seed_x = x
                seed_y = y
            else:
                print("filling x,y")
                f = FloodFill(w,h)
                f.fill(allPaths, x, y, w, h)
                print("coloring")
                selectedPix = f.selectedCells
                for i in f.selectedCells:
                    pix_y = i // w
                    pix_x= i - pix_y*w
                    imgDest[pix_y][pix_x] = img[pix_y][pix_x]
                    # img[pix_y][pix_x] = (255,255,255)
            


    elif event== 0: #cv.EVENT_MOUSEMOVE
        if tool == 0:
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
        readyToDraw = False
        
        if tool == 0 :
            dijkstraCompleted = False
            i = seed_x+seed_y*w
            while(not len(g.parent) == 0 and g.parent[i] != -1):
                allPaths.append(i)
                i = g.parent[i]
            # print(allPaths)
        elif (tool == 1):
            pix_y = allPaths[0] // w
            pix_x = allPaths[0] - pix_y*w
            bresenham(seed_x, seed_y, pix_x, pix_y, w, h, allPaths)
            for i in allPaths:
                pix_y = i // w
                pix_x = i - pix_y*w
                img[pix_y][pix_x] = (0,255,0)
            


def arrowCallback():
    global img
    global imgDest
    global imgDestOG
    global selectedPix
    global delta_x
    global delta_y
    h, w, d = img.shape

    imgDest = imgDestOG.copy()
    print("moving", delta_x, delta_y)
    for pix in selectedPix:
        pix_y = pix // w
        pix_x = pix - pix_y*w
        imgDest[pix_y + delta_y][pix_x + delta_x] = img[pix_y][pix_x]

# def copyCallback(f, selectedPix):
#     print("filling x,y")
#     f.fill(allPaths, x, y, w, h)
#     print("floodfill completed")
#     selectedPix = f.filledCells

# def pasteCallback(f, img, imgDest):    
#     for i in f.filledCells:
#         pix_y = i // w
#         pix_x = i - pix_y*w
#         imgDest[pix_y][pix_x] = img[pix_y][pix_x]

########## preprocessing ##########
print("loading image")
img = cv.imread("./imgs/goodboi.jpg") 
imgOG = cv.imread("./imgs/goodboi.jpg") 
imgDest = cv.imread("./imgs/owl.png") 
imgDestOG = cv.imread("./imgs/owl.png") 
imgFinal = []
h,w,d = img.shape

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
    imgFinal = np.zeros_like(img2)
    for y in range(1, h-2):
        for x in range(1, w-2):
            localPixels = np.array([[ img2[y-1][x-1],  img2[y-1][x],  img2[y-1][x+1]],
                                    [ img2[y  ][x-1],  img2[y  ][x],  img2[y  ][x+1]],
                                    [ img2[y+1][x-1],  img2[y+1][x],  img2[y+1][x+1]]])
            
            transformPixelsV = kernelV * localPixels / 4
            scoreV = transformPixelsV.sum()
            
            transformPixelsH = kernelH * localPixels / 4
            scoreH = transformPixelsH.sum()
            
            imgFinal[y][x] = ( scoreV**2 + scoreH**2 )**0.5
    
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
                    g.addEdge(y*w+x, b*w+a, imgFinal[b][a])
    print("graph for scissoring completed")


######### rendering ##########
readyToDraw = True
cv.namedWindow('image post detection')
cv.namedWindow('image')
cv.namedWindow('imageDest')
f = FloodFill(w,h)


while(True):
    
    cv.setMouseCallback('image', mouse_callback)
    k = cv.waitKey(20)
    if k & 0xFF == 27: # escape - exit window
        break
    
    # if k & 0xFF == 99: #C
    #     print("C")
    #     delta_y -=5
    #     copyCallback(f, selectedPix)
    # if k & 0xFF == 118: #V
    #     print("V")
    #     delta_x -=5
    #     pasteCallback(f, img, imgDest)

    if k & 0xFF == 119: #W
        print("W")
        delta_y -=5
        arrowCallback()
    if k & 0xFF == 97: #A
        print("A")
        delta_x -=5
        arrowCallback()
    if k & 0xFF == 115: #S
        print("S")
        delta_y +=5
        arrowCallback()
    if k & 0xFF == 100: #D
        print("D")
        delta_x +=5
        arrowCallback()
        
    if k & 0xFF == 49: #1
        tool = 0
    if k & 0xFF == 50: #2
        tool = 1
    if k & 0xFF == 51: #3
        tool = 2
    
    cv.imshow('image',img)
    cv.imshow('imageDest',imgDest)
    if(tool == 0):
        cv.imshow('image post detection',imgFinal)

cv.destroyAllWindows()


# def main():
# if __name__ == "__main__":
#     main()