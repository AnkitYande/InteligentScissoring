from tkinter import * #tkinter
from tkinter import filedialog
from PIL import ImageTk, Image #pillow
import cv2 as cv # OpenCV
import numpy as np #NumPY

from bresenham import bresenham
from graph import Graph
from fill import FloodFill

root = Tk()
root.title("Final Project")
tool = IntVar()
focus = IntVar()

IMAGE1 = None
IMAGE1_OG = None
IMAGE1_FINAL = None
IMAGE2 = None
IMAGE2_OG = None
IMAGE2_FINAL = None
SELECTED_IMAGE = None
g1 = g2 = None

selectionComplete = False
allPaths = []
selectedPix = []
seed_x = seed_y = None

def initializeDijkstra(IMAGE, imageNumber):
    # global g1
    # global g2
    w,h,d = IMAGE.shape
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
    for y in range(3, h-2):
        for x in range(3, w-2):
            localPixels = np.array([[ img2[x-1][y-1],  img2[x][y-1],  img2[x+1][y-1]],
                                    [ img2[x-1][y],    img2[x][y],    img2[x+1][y]  ],
                                    [ img2[x-1][y+1],  img2[x][y+1],  img2[x+1][y+1]]])
            
            transformPixelsV = kernelV * localPixels / 4
            scoreV = transformPixelsV.sum()
            
            transformPixelsH = kernelH * localPixels / 4
            scoreH = transformPixelsH.sum()
            
            imgFinal[x][y] = ( scoreV**2 + scoreH**2 )**0.5

    imgFinal = imgFinal.max()-imgFinal
    print("edge detection completed")

    ######### scissoring graph ##########
    print("creating graph for scissoring")
    g = None
    if imageNumber == "img1":
        g1 = Graph(h*w)
        g = g1
    else:
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

def copy(image, x, y):
    global selectedPix
    global allPaths
    print("copying")
    h,w,d = image.shape
    f = FloodFill(w,h)
    f.fill(allPaths, x, y, w, h)
    selectedPix = f.selectedCells
    selectedPix.sort()
    print("copying completed")
    
def paste(imgDest, img, imageNumber, x, y):
    global selectedPix
    h,w,d = img.shape
    print("pasting")

    #print(img)
    delta_y = (selectedPix[0]//w)
    delta_x = x - (selectedPix[0]- delta_y*w)
    delta_y = y - delta_y

    for i in selectedPix:
        pix_y = i // w
        pix_x = i - pix_y*w
        imgDest[pix_y + delta_y][pix_x + delta_x] = img[pix_y][pix_x]
        # img[pix_y][pix_x] = (255,255,255)
    
    drawImage(imgDest, imageNumber)
    print("pasting completed")

def openSrc():
    global IMAGE1
    root.filename = filedialog.askopenfilename(initialdir="./imgs", title="Select A File", filetypes=(("jpg files", "*.jpg"),("png files", "*.png")))
    img = cv.imread(root.filename)
    IMAGE1 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    IMAGE1_OG = IMAGE1.copy()
    #IMAGE1_FINAL = initializeDijkstra(IMAGE1, "img1")
    drawImage(IMAGE1, "img1")

def openDest():
    global IMAGE2
    root.filename = filedialog.askopenfilename(initialdir="./imgs", title="Select A File", filetypes=(("jpg files", "*.jpg"),("png files", "*.png")))
    img = cv.imread(root.filename)
    IMAGE2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    IMAGE2_OG = IMAGE2.copy()
    #IMAGE2_FINAL = initializeDijkstra(IMAGE2, "img2")
    drawImage(IMAGE2, "img2")

def polygons(x, y, IMAGE, imageNumber, allPaths):
    global seed_x
    global seed_y

    h,w,d = IMAGE.shape
    if(seed_x != None and seed_y != None):
        print("running bresenham", seed_x, seed_y, x, y)
        bresenham(seed_x, seed_y, x, y, w, h, allPaths)
        for i in allPaths:
            pix_y = i // w
            pix_x = i - pix_y*w
            IMAGE[pix_y][pix_x] = (255,0,255)
        drawImage(IMAGE, imageNumber)
    else:
        allPaths.append( y*w+x ) # this works bc mutable list
    
    seed_x = x
    seed_y = y

    
def left_click(eventorigin):
    global x,y
    global IMAGE1
    global IMAGE2
    global allPaths
    global seed_x
    global seed_y
    global selectionComplete
    global SELECTED_IMAGE

    caller = eventorigin.widget
    x = eventorigin.x
    y = eventorigin.y
    
    imageUsed = None
    imageUsedNum = None

    if str(caller) == ".img1" :
        if focus == 2:
            allPaths = []
            seed_x = seed_y = None
            selectionComplete = False
        imageUsed = IMAGE1
        imageUsedNum = "img1"
        focus.set(1)
    elif str(caller) == ".img2" :
        if focus.get() == 1:
            allPaths = []
            seed_x = seed_y = None
            selectionComplete = False
        imageUsed = IMAGE2
        imageUsedNum = "img2"
        focus.set(2)

    if not selectionComplete:
        if tool.get() == 0 and imageUsedNum != None:
            polygons(x,y, imageUsed, imageUsedNum, allPaths)
    
    if tool.get() == 3 and imageUsedNum != None:  
        if selectionComplete:
            copy(imageUsed, x, y)
            SELECTED_IMAGE = imageUsed
        else:
            print("ERROR: NOTHING SELECTED")
    if tool.get() == 4:
        if len(selectedPix) != 0 and SELECTED_IMAGE.any() != None:
            paste(imageUsed, SELECTED_IMAGE, imageUsedNum, x, y) # pasted into, copied from
        else:
            print("ERROR: NOTHING COPIED")

def right_click(eventorigin):
    global seed_x
    global seed_y
    global allPaths
    global selectionComplete

    caller = eventorigin.widget
    x = eventorigin.x
    y = eventorigin.y

    imageUsed = None
    imageUsedNum = None

    if str(caller) == ".img1" :
        imageUsed = IMAGE1
        imageUsedNum = "img1"

    elif str(caller) == ".img2" :
        imageUsed = IMAGE2
        imageUsedNum = "img2"


    if not selectionComplete:
        if tool.get() == 0:
            h,w,d = imageUsed.shape
            pix_y = allPaths[0] // w
            pix_x = allPaths[0] - pix_y*w
            polygons(pix_x, pix_y, imageUsed, imageUsedNum, allPaths)
            selectionComplete = True

    # allPaths = []
    # seed_x = seed_y = None

        
    


def mouse_motion(eventorigin):
    global x,y
    x = eventorigin.x
    y = eventorigin.y
    caller = eventorigin.widget
    if str(caller) == ".!label" :
        print("image 0)", x,y)
        focus = 0
    elif str(caller) == ".!label2" :
        print("image 1)",x,y)
        focus = 2

f1 = Frame(root)
b1 = Radiobutton(f1, 
                text="Polygon Selection",
                padx = 20, 
                variable=tool, 
                value=0).pack(side="left")
b2 = Radiobutton(f1, 
                text="Inteligent Scissoring",
                padx = 20, 
                variable=tool, 
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

src_open_btn = Button(root, text="Select Source Image", command=openSrc)
dest_open_btn = Button(root, text="Select Destination Image", command=openDest)

f1.grid(row=0, column=0, columnspan = 2, sticky="nsew")
src_open_btn.grid(row=1, column=0)
dest_open_btn.grid(row=1, column=1)

root.bind("<Button 1>", left_click)
root.bind("<Button 2>", right_click)
root.bind('<Motion>', mouse_motion)

root.mainloop()