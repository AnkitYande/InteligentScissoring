from tkinter import * #tkinter
from tkinter import filedialog
from PIL import ImageTk, Image #pillow
import cv2 as cv # OpenCV
import numpy as np #NumPy

from bresenham import bresenham
from graph import Graph
from fill import FloodFill

root = Tk()
root.title("Final Project")
tool = IntVar()
focus = IntVar()
prevTool = 0

IMAGE1 = None
IMAGE1_EDIT = None
IMAGE1_OG = None
IMAGE1_EDGES = None
showImg1Edges = False

IMAGE2 = None
IMAGE2_EDIT = None
IMAGE2_OG = None
IMAGE2_EDGES = None
showImg2Edges = False

SELECTED_IMAGE = None

g1 = g2 = None

selectionComplete = False
dijkstraComplete = False
allPaths = []
selectedPix = []
seed_x = seed_y = None

def initializeDijkstra(IMAGE, imageNumber):
    global dijkstraComplete
    global IMAGE1_EDGES
    global IMAGE2_EDGES
    global g1
    global g2
    dijkstraComplete = False
    h,w,d = IMAGE.shape
    ######### preprocessing ##########
    print("preprocessing")
    img2 = cv.cvtColor(IMAGE, cv.COLOR_RGB2GRAY) # convert to graysacle
    img2 = cv.GaussianBlur(img2,(5,5),cv.BORDER_DEFAULT) # Gaussian Blur the image
    print("preprocessing completed")

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
            
            transformPixelsV = kernelV * localPixels
            scoreV = transformPixelsV.sum()
            
            transformPixelsH = kernelH * localPixels
            scoreH = transformPixelsH.sum()
            
            imgFinal[y][x] = ( scoreV**2 + scoreH**2 )**0.5

    imgFinal = imgFinal.max()-imgFinal
    print("edge detection completed")

    ######### scissoring graph ##########
    print("creating graph for scissoring")
    g = None
    if imageNumber == "img1":
        IMAGE1_EDGES = imgFinal
        g1 = Graph(h*w)
        g = g1
    else:
        IMAGE2_EDGES = imgFinal
        g2 = Graph(h*w)
        g = g2

    for y in range(h):
        for x in range(w):
            
            for b in range(y-1, y+2):
                for a in range(x-1, x+2):
                    if (a < 0 or a >= w or b < 0 or b >= h or (y == b and x == a)): # Check that [row, col] is not out of bounds
                        continue
                    g.addEdge(y*w+x, b*w+a, abs(imgFinal[b][a]))
    print("graph for scissoring completed")
    return(imgFinal)
    

def copy(image, x, y):
    global selectedPix
    global allPaths
    selectedPix = []
    print("copying")
    h,w,d = image.shape
    f = FloodFill(w,h)
    f.fill(allPaths, x, y, w, h)
    selectedPix = f.selectedCells
    # selectedPix.sort()
    print("copying completed")
    
def paste(imgDest, img, imgEdit, imageNumber, x, y):
    global selectedPix
    h,w,d = img.shape
    h2,w2,d2 = imgDest.shape
    print("pasting")

    #print(img)
    delta_y = (selectedPix[0]//w)
    delta_x = x - (selectedPix[0]- delta_y*w)
    delta_y = y - delta_y

    for i in selectedPix:
        pix_y = i // w
        pix_x = i - pix_y*w
        dest_y = pix_y + delta_y
        dest_x = pix_x + delta_x
        if not ((dest_y < 0) or (dest_y >= h2) or (dest_x < 0) or (dest_x >= w2)):
            imgDest[dest_y][dest_x] = img[pix_y][pix_x]
            imgEdit[dest_y][dest_x] = img[pix_y][pix_x]
    
    print("pasting completed")


def polygonSelection(x, y, IMAGE, imageNumber, allPaths):
    global seed_x
    global seed_y

    h,w,d = IMAGE.shape
    if(seed_x != None and seed_y != None):
        print("running bresenham", seed_x, seed_y, x, y)
        bresenham(seed_x, seed_y, x, y, w, h, allPaths)
        for i in allPaths:
            pix_y = i // w
            pix_x = i - pix_y*w
            IMAGE[pix_y][pix_x] = (255,0,0)
        drawImage(IMAGE, imageNumber)
    else:
        allPaths.append( y*w+x ) # this works bc mutable list
    
    seed_x = x
    seed_y = y


def runDijkstra(x, y, IMAGE, imageNumber, g, allPaths):
    global seed_x
    global seed_y
    h,w,d = IMAGE.shape
    seed_x = x
    seed_y = y
    seed = x+y*w
    print("New seed at:", x,y, seed)
    
    i = seed
    tempPaths = []
    while(not len(g.parent) == 0 and g.parent[i] != -1):
        tempPaths.append(i)
        i = g.parent[i]
    
    tempPaths.reverse()
    allPaths += tempPaths

    print("performing dijkstra")
    g.parent = []
    g.dijkstra(seed)
    print("dijkstra complete")

def scissoring(x, y, img, imgOG, imageNumber, g, allPaths):
    global seed_x
    global seed_y
    h,w,d = img.shape
    i = x+y*w
    img = imgOG.copy() #reset image
    cv.circle(img,(seed_x,seed_y),5,(0,255,0),-1)

    for pix in allPaths:
        pix_y = pix // w
        pix_x = pix - pix_y*w
        img[pix_y][pix_x] = (255,0,0)

    while(not len(g.parent) == 0 and g.parent[i] != -1):
        i = g.parent[i]
        pix_y = i // w
        pix_x = i - pix_y*w
        img[pix_y][pix_x] = (255,0,0)
    
    drawImage(img, imageNumber)


def left_click(eventorigin):
    global IMAGE1
    global IMAGE2
    global IMAGE1_EDIT
    global IMAGE2_EDIT
    global allPaths
    global selectedPix
    global seed_x
    global seed_y
    global selectionComplete
    global dijkstraComplete
    global SELECTED_IMAGE
    global prevTool
    
    caller = eventorigin.widget
    x = eventorigin.x
    y = eventorigin.y
    
    imageUsed = None
    imageEditUsed = None
    imageUsedNum = None
    graphUsed = None

    if str(caller) == ".img1" or str(caller) == ".img2" :

        if str(caller) == ".img1" :
            if focus.get() == 2:
                allPaths = []
                seed_x = seed_y = None
                selectionComplete = False
            imageUsed = IMAGE1
            imageEditUsed = IMAGE1_EDIT
            imageUsedNum = "img1"
            graphUsed = g1
            focus.set(1)
        elif str(caller) == ".img2" :
            if focus.get() == 1:
                allPaths = []
                seed_x = seed_y = None
                selectionComplete = False
            imageUsed = IMAGE2
            imageEditUsed = IMAGE2_EDIT
            imageUsedNum = "img2"
            graphUsed = g2
            focus.set(2)

        if not selectionComplete:
            if(allPaths):
                print(allPaths[0])
            if tool.get() == 0 and imageUsedNum != None:
                polygonSelection(x,y, imageUsed, imageUsedNum, allPaths)
                prevTool = 0

            elif tool.get() == 1 and imageUsedNum != None and graphUsed != None:
                dijkstraComplete = False
                runDijkstra(x,y,imageUsed, imageUsedNum, graphUsed, allPaths)
                dijkstraComplete = True

            elif tool.get() == 2 and imageUsedNum != None:
                h,w,d = imageUsed.shape
                hsv_img = cv.cvtColor(imageUsed.copy(), cv.COLOR_RGB2HSV)
                f = FloodFill(w,h)
                f.colorSelect(hsv_img, allPaths, x, y, w, h)
                selectedPix = f.selectedCells
                # selectedPix.sort()
                print("color picking completed")
                for i in allPaths:
                    pix_y = i // w
                    pix_x = i - pix_y*w
                    imageUsed[pix_y][pix_x] = (255,0,0)
                selectionComplete = True
                
                drawImage(imageUsed, imageUsedNum)

        if tool.get() == 3 and imageUsedNum != None:  
            if selectionComplete:
                copy(imageUsed, x, y)
                resetGlobals()
                imageUsed = imageEditUsed.copy()
                SELECTED_IMAGE = imageEditUsed.copy()
                drawImage(imageUsed, imageUsedNum)
            else:
                print("ERROR: NOTHING SELECTED")

        if tool.get() == 4 and imageUsedNum != None:
            if len(selectedPix) != 0 and SELECTED_IMAGE.any() != None:
                paste(imageUsed, SELECTED_IMAGE, imageEditUsed, imageUsedNum, x, y) 
                imageUsed = imageEditUsed.copy()
                drawImage(imageUsed, imageUsedNum)
            else:
                print("ERROR: NOTHING COPIED")
    

def right_click(eventorigin):
    global allPaths
    global selectionComplete
    global dijkstraComplete

    caller = eventorigin.widget
    x = eventorigin.x
    y = eventorigin.y

    imageUsed = None
    imageUsedNum = None
    graphUsed = None
    
    if str(caller) == ".img1" or str(caller) == ".img2" :

        if str(caller) == ".img1" :
            imageUsed = IMAGE1
            imageUsedNum = "img1"
            graphUsed = g1

        elif str(caller) == ".img2" :
            imageUsed = IMAGE2
            imageUsedNum = "img2"
            graphUsed = g2


        if not selectionComplete and imageUsedNum != None:
            h,w,d = imageUsed.shape
            if tool.get() == 0:
                pix_y = allPaths[0] // w
                pix_x = allPaths[0] - pix_y*w
                polygonSelection(pix_x, pix_y, imageUsed, imageUsedNum, allPaths)
                selectionComplete = True
                print("Selection Completed")
            if tool.get() == 1:
                i = seed_x+seed_y*w
                while(not len(graphUsed.parent) == 0 and graphUsed.parent[i] != -1):
                    allPaths.append(i)
                    i = graphUsed.parent[i]
                selectionComplete = True
                dijkstraComplete = False
                print("Selection Completed")


def mouse_motion(eventorigin):
    global IMAGE1
    global IMAGE2
    global dijkstraComplete
    global prevTool
    
    x = eventorigin.x
    y = eventorigin.y
    caller = eventorigin.widget
    
    imageUsed = None
    imageUsedNum = None
    imageOG = None
    graphUsed = None

    if str(caller) == ".img1" or str(caller) == ".img2" :

        if str(caller) == ".img1" :
            imageUsed = IMAGE1
            imageUsedNum = "img1"
            imageOG = IMAGE1_OG
            graphUsed = g1
        elif str(caller) == ".img2" :
            imageUsed = IMAGE2
            imageUsedNum = "img2"
            imageOG = IMAGE2_OG
            graphUsed = g2

        if(tool.get() == 1) and imageUsedNum != None:
            if(prevTool == 0 and graphUsed != None and seed_x != None):
                graphUsed.parent = []
                h,w,d = imageUsed.shape
                graphUsed.dijkstra(seed_y*w+seed_x)
                dijkstraComplete = True
                prevTool = 1
            if dijkstraComplete and not selectionComplete:
                scissoring(x,y,imageUsed, imageOG, imageUsedNum, graphUsed, allPaths)

def drawImage(IMAGE, imageNumber):
    global src_img
    global dest_img
    if imageNumber == "img1":
        src_img = Image.fromarray(IMAGE)
        src_img = ImageTk.PhotoImage(src_img)
        src_img_label = Label(image=src_img, name=imageNumber)
        src_img_label.grid(row=2, column=0)
    elif imageNumber == "img2":
        dest_img = Image.fromarray(IMAGE)
        dest_img = ImageTk.PhotoImage(dest_img)
        dest_img_label = Label(image=dest_img, name=imageNumber)
        dest_img_label.grid(row=2, column=1)

def openSrc():
    global IMAGE1
    global IMAGE1_OG
    global IMAGE1_EDIT
    global seed_x
    global seed_y
    seed_x = seed_y = None
    root.filename = filedialog.askopenfilename(initialdir="./imgs", title="Select A File", filetypes=(("jpg files", "*.jpg"),("png files", "*.png")))
    img = cv.imread(root.filename)
    IMAGE1 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    IMAGE1_OG = IMAGE1.copy()
    IMAGE1_EDIT = IMAGE1.copy()
    IMAGE1_EDGES = initializeDijkstra(IMAGE1, "img1")
    drawImage(IMAGE1, "img1")
    
def openDest():
    global IMAGE2
    global IMAGE2_OG
    global IMAGE2_EDIT
    global seed_x
    global seed_y
    seed_x = seed_y = None
    root.filename = filedialog.askopenfilename(initialdir="./imgs", title="Select A File", filetypes=(("jpg files", "*.jpg"),("png files", "*.png")))
    img = cv.imread(root.filename)
    IMAGE2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    IMAGE2_OG = IMAGE2.copy()
    IMAGE2_EDIT = IMAGE2.copy()
    IMAGE2_EDGES = initializeDijkstra(IMAGE2, "img2")
    drawImage(IMAGE2, "img2")

def resetGlobals():
    global allPaths
    global seed_x
    global seed_y
    global dijkstraComplete
    global selectionComplete
    
    selectionComplete = False
    dijkstraComplete = False
    seed_x = None
    seed_y = None
    allPaths = []

def resetSrc():
    resetGlobals()
    global IMAGE1
    global IMAGE1_OG
    global IMAGE1_EDIT
    global selectedPix
    selectedPix = []
    IMAGE1 = IMAGE1_OG.copy()
    IMAGE1_EDIT = IMAGE1.copy()
    drawImage(IMAGE1, "img1")

def resetDest():
    resetGlobals()
    global IMAGE2
    global IMAGE2_OG
    global IMAGE2_EDIT
    global selectedPix
    selectedPix = []
    IMAGE2 = IMAGE2_OG.copy()
    IMAGE2_EDIT = IMAGE2.copy()
    drawImage(IMAGE2, "img2")

def edgesSrc():
    global showImg1Edges
    showImg1Edges = not showImg1Edges
    if showImg1Edges:
        drawImage(IMAGE1_EDGES, "img1")
    else:
        drawImage(IMAGE1, "img1")

def edgesDest():
    global showImg2Edges
    showImg2Edges = not showImg2Edges
    if showImg2Edges:
        drawImage(IMAGE2_EDGES, "img2")
    else:
        drawImage(IMAGE2, "img2")


f1 = Frame(root)
b1 = Radiobutton(f1, 
                text="Polygon Selection",
                padx = 20, 
                variable=tool, 
                value=0).pack(side="left")
b2 = Radiobutton(f1, 
                text= "Intelligent Scissoring",
                padx = 20, 
                variable= tool, 
                value=1).pack(side="left")
b3 = Radiobutton(f1, 
                text="Color Fill Select",
                padx = 20, 
                variable=tool, 
                value=2).pack(side="left")
b4 = Radiobutton(f1, 
                text="Copy Tool",
                padx = 20, 
                variable=tool, 
                value=3).pack(side="left")
b5 = Radiobutton(f1, 
                text="Paste Tool",
                padx = 20, 
                variable=tool, 
                value=4).pack(side="left")


src_open_btn = Button(root, text="Select Image 1", command=openSrc)
dest_open_btn = Button(root, text="Select Image 2", command=openDest)

reset1_btn = Button(root, text="Reset Image 1", command=resetSrc)
reset2_btn = Button(root, text="Reset Image 2", command=resetDest)

edges1_btn = Button(root, text="Toggle Image 1 Edges", command=edgesSrc)
edges2_btn = Button(root, text="Toggle Image 2 Edges", command=edgesDest)

f1.grid(row=0, column=0, columnspan = 2, sticky="nsew")
src_open_btn.grid(row=1, column=0)
dest_open_btn.grid(row=1, column=1)
reset1_btn.grid(row=3, column=0)
reset2_btn.grid(row=3, column=1)
edges1_btn.grid(row=4, column=0)
edges2_btn.grid(row=4, column=1)

root.bind("<Button 1>", left_click)
root.bind("<Button 2>", right_click)
root.bind('<Motion>', mouse_motion)

root.mainloop()