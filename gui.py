from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv # OpenCV

root = Tk()
root.title("Final Project")
tool = IntVar()


def openSrc():
    global src_img
    root.filename = filedialog.askopenfilename(initialdir="/Users/ankityande/Documents/UT/graphics/finalProg/imgs", title="Select A File", filetypes=(("jpg files", "*.jpg"),("png files", "*.png")))
    img = cv.imread(root.filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    src_img = ImageTk.PhotoImage(img)
    img_label = Label(image=src_img).grid(row=2, column=0)
def openDest():
    global dest_img
    root.filename = filedialog.askopenfilename(initialdir="/Users/ankityande/Documents/UT/graphicsfinalProg/imgs", title="Select A File", filetypes=(("jpg files", "*.jpg"),("png files", "*.png")))
    dest_img = ImageTk.PhotoImage(Image.open(root.filename))
    img_label = Label(image=dest_img).grid(row=2, column=1)
    
def getorigin(eventorigin):
      global x,y
      x = eventorigin.x
      y = eventorigin.y
      print(x,y)


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
               value=2).pack(side="left")
b5 = Radiobutton(f1, 
               text="Paste Tool",
               padx = 20, 
               variable=tool, 
               value=2).pack(side="left")

src_open_btn = Button(root, text="Select Source Image", command=openSrc)
dest_open_btn = Button(root, text="Select Destination Image", command=openDest)

f1.grid(row=0, column=0, columnspan = 2, sticky="nsew")

src_open_btn.grid(row=1, column=0)
dest_open_btn.grid(row=1, column=1)

root.mainloop()