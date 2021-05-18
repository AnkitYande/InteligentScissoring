# graphicsFinalProj
Final Project by Ankit Yande (asy364) and Nathan Gates (nag2486) for CS354.

Video Demo can be found at: https://youtu.be/UlC1-5gkNfI

Formal Report writeup can be found at: https://docs.google.com/document/d/15cI-ifh9AzsKH278Pd6mD-1tUbTExsjSYxVRVDPWQsM/edit?usp=sharing 

## To Build and Run:
Install Required libraries: tkinter, filedialog, pillow, OpenCV, and NumPy

Run python3 on gui.py

## Using our GUI
Upon running gui.py, the GUI will open. There are 5 tool buttons at the top, followed by three rows and two columns of image buttons. First, the user must load an image using either the **Select Image 1** or **Select Image 2 button**, which allow the user to open any image from their local file system into the GUI. From here the user can make selections to copy and pate between images.

Once any image is loaded, the user can use one of the three **selection tools** on the loaded images. 
* To use the **Polygon Selection tool**, the user must first provide a left click input at the desired location. All subsequent left clicks will draw a selection line between the previous endpoint and the click location. To complete the selection, the user must right click, and the software will intelligently close the selection by drawing between the last endpoint and the user's first left click.
* To use the **Intelligent Scissoring tool**, the user must provide a left click seed at the desired location. After the phrase "Dijkstra Completed" is printed to the user's terminal, the user can move the mouse around the image. The software will draw a line from the seed position to the mouse location while snapping to the closest edges. To create a dynamic selection, the user can simply left click multiple times to provide new seeds to the algorithm. The conjunctive path between all user selections will be drawn. To complete the selection, the user must right click, and the software will draw the selection from the previous seed to the right click location. This right click location must fully enclose the desired object to achieve desired results.
* To use the **Color Select tool**, the user must provide a left click at the desired location. The software will queue and check neighboring pixels' HSV values and their similarity to the initial click pixel. All pixels with HSV values similar to the initial pixel will be wrapped in a selection boundary when this algorithm terminates. 

*** Note: exactly one selection can be made at any given time without either copying or resetting ***
    
After a selection has been made, the user can **Copy** image data. The user must provide a left click anywhere within the bounds of the image; depending on whether the user clicks within the selection's interior or exterior determines which region will be copied - all pixels within the image boundaries and contained by the selection will be added to a copy buffer. Once the copy buffer has been filled, the previous selection is destroyed, but the data remains intact within the buffer to be copied. At this point, the user can either use the paste tool, or make a new selection.

After the copy buffer has been filled, the user is able to **Paste** onto any loaded target image. The user must provide a left click anywhere within the bounds of the image. All data within the copy buffer will be drawn starting at the user's left click location. Any paste operation which would draw pixels outside of the image boundaries will simply not draw these extraneous pixels, but still draw all pixels residing within the bounds. 
This operation can be repeated indefinitely on the same copy buffer, until the image is reset via reset button or a new selection has been copied into the copy buffer.

The user can reset the changes made to an image by simply clicking the **Reset Image** buttons, which will load the original, unaltered image data into the window. This is a full reset - there is no undo button to remove the previous change. 

The user can also toggle the image render of all perceived object edges. This allows the user to see the processed version of the image which serves as the backbone for the Intelligent Scissor tool. 

*** Note: This object edge image is only computed once upon loading any image into the GUI. The overhead cost of producing this image and its associated graph is high, which slows down the software. We elected to compute this exactly once at the start, rather than any time the intelligent scissor tool is selected, in the sake of saving user wait time and improving user experience. However, this reduces the accuracy of the Intelligent Scissor tool as more edits are made to the image, as the current image will deviate further from the initial image data that this graph depends on. ***
