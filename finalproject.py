import numpy as np
import cv2 as cv # OpenCV
import queue  
from collections import defaultdict
import sys
 

readyToDraw = False

class Heap():
 
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []
 
    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode
 
    # A utility function to swap two nodes
    # of min heap. Needed for min heapify
    def swapMinHeapNode(self,a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
 
    # A standard function to heapify at given idx
    # This function also updates position of nodes
    # when they are swapped.Position is needed
    # for decreaseKey()
    def minHeapify(self, idx):
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2
 
        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left
 
        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right
 
        # The nodes to be swapped in min
        # heap if idx is not smallest
        if smallest != idx:
 
            # Swap positions
            self.pos[ self.array[smallest][0]] = idx
            self.pos[ self.array[idx][0]] = smallest
 
            # Swap nodes
            self.swapMinHeapNode(smallest, idx)
 
            self.minHeapify(smallest)
 
    # Standard function to extract minimum
    # node from heap
    def extractMin(self):
 
        # Return NULL wif heap is empty
        if self.isEmpty() == True:
            return
 
        # Store the root node
        root = self.array[0]
 
        # Replace root node with last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
 
        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
 
        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)
 
        return root
 
    def isEmpty(self):
        return True if self.size == 0 else False
 
    def decreaseKey(self, v, dist):
 
        # Get the index of v in  heap array
 
        i = int(self.pos[v])
        # print(i)
 
        # Get the node and update its dist value
        self.array[i][1] = dist
 
        # Travel up while the complete tree is
        # not hepified. This is a O(Logn) loop
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
 
            # Swap this node with its parent
            self.pos[ self.array[i][0] ] = (i-1)/2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swapMinHeapNode(i, (i - 1)//2 )
 
            # move to parent index
            i = (i - 1) // 2
 
    # A utility function to check if a given
    # vertex 'v' is in min heap or not
    def isInMinHeap(self, v):
 
        if self.pos[v] < self.size:
            return True
        return False
 
 
def printArr(dist, n):
    print("Vertex\tDistance from source")
    for i in range(n):
        print ("%d\t\t%d" % (i,dist[i]))
 
 
class Graph():
 
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)
        self.parent = []
 
    # Adds an edge to an undirected graph
    def addEdge(self, src, dest, weight):
 
        # Add an edge from src to dest.  A new node
        # is added to the adjacency list of src. The
        # node is added at the beginning. The first
        # element of the node has the destination
        # and the second elements has the weight
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
 
        # Since graph is undirected, add an edge
        # from dest to src also
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

    # Function to print shortest path
    # from source to j
    # using parent array
    def printPath(self, parent, j):
          
        #Base Case : If j is source
        if parent[j] == -1 : 
            print(j)
            return
        self.printPath(parent , parent[j])
        print(j , end = ', ')

    # A utility function to print
    # the constructed distance
    # array
    def printSolution(self, src, dist):
        print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)):
            print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i])),
            self.printPath(self.parent,i)
        print("Solution Printed")
 
    # The main function that calulates distances
    # of shortest paths from src to all vertices.
    # It is a O(ELogV) function
    def dijkstra(self, src):
 
        V = self.V  # Get the number of vertices in graph
        dist = []   # dist values used to pick minimum
                    # weight edge in cut

        # parent = []
        
        # minHeap represents set E
        minHeap = Heap()
 
        #  Initialize min heap with all vertices.
        # dist value of all vertices
        for v in range(V):
            dist.append(sys.maxsize)
            self.parent.append(-1)
            minHeap.array.append( minHeap.
                                newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)
 
        # Make dist value of src vertex as 0 so
        # that it is extracted first
        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])
 
        # Initially size of min heap is equal to V
        minHeap.size = V
 
        # In the following loop,
        # min heap contains all nodes
        # whose shortest distance is not yet finalized.
        while minHeap.isEmpty() == False:
 
            # Extract the vertex
            # with minimum distance value
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]
 
            # Traverse through all adjacent vertices of
            # u (the extracted vertex) and update their
            # distance values
            for pCrawl in self.graph[u]:
 
                v = pCrawl[0]
 
                # If shortest distance to v is not finalized
                # yet, and distance to v through u is less
                # than its previously calculated distance
                if minHeap.isInMinHeap(v) and dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]:
                    dist[v] = pCrawl[1] + dist[u]
                    self.parent[v] = u
                    # update distance value
                    # in min heap also
                    minHeap.decreaseKey(v, dist[v])
 
        #self.printSolution(src, dist)
 


seed_x = seed_y = None
dijkstraCompleted = False
# img = []

def mouse_callback(event,x,y,flags,param):
    global img
    global imgOG

    h,w = imgFinal.shape
    if event== 1:   #cv.EVENT_LBUTTONDOWN
        global dijkstraCompleted
        dijkstraCompleted = False
        global seed_x 
        seed_x = x
        global seed_y 
        seed_y = y
        # seed = 5 * 24 + 17
        seed = x+y*w
        

        print("New seed at:", x,y, w, h, seed)
        print("performing dijkstra")
        g.dijkstra(seed)
        dijkstraCompleted = True
        print("dijkstra complete")
    elif event== 0: #cv.EVENT_MOUSEMOVE
        if dijkstraCompleted :
            i = x+y*w
            # i =  20 * 24 + 21
            img = cv.imread("./imgs/owl.png") 
            cv.circle(img,(seed_x,seed_y),5,(0,255,0),-1)

            while(not len(g.parent) == 0 and g.parent[i] != -1):
                i = g.parent[i]
                pix_y = i // w
                pix_x = i - pix_y*w
                # print(pix_x,pix_y, i)
                cv.circle(img,(pix_x,pix_y),1,(255,0,0),-1)

            cv.imshow('image',img)
            # print("end at", x,y)
            # mouse_x = x
            # mouse_y = y
            # cv.circle(imgFinal,(x,y),10,(255,0,0),-1)
            # if(seed_x != None and seed_y != None):
                # path = ourDijkstra(imgFinal, seed_x, seed_y, x, y)
                # print(len(path))
                # for pixel in path:
                #     cv.circle(imgFinal,(pixel[0],pixel[1]),1,(255,0,0),-1)
            # w,h = imgFinal.shape



########## preprocessing ##########

print("loading image")
img = cv.imread("./imgs/owl.png") 
imgOG = cv.imread("./imgs/owl.png") 

print("preprocessing")
img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert to graysacle
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

#### create graph

#draw image

g = Graph(h*w)

'''
1 1 1 1
1 1 0 1
1 1 0 1
1 1 1 1
'''

print("creating graph for scissoring")
for y in range(h):
    for x in range(w):
        
        for b in range(y-1, y+2):
            for a in range(x-1, x+2):
                if (a < 0 or a >= w or b < 0 or b >= h or (y == b and x == a)): # Check that [row, col] is not out of bounds
                    continue
                g.addEdge(y*w+x, b*w+a, abs(imgFinal[b][a]))
print("graph for scissoring completed")
readyToDraw = True


cv.namedWindow('image post detection')
cv.namedWindow('image')

while(True):
    cv.imshow('image post detection',imgFinal)
    
    if(readyToDraw):
        seed = cv.setMouseCallback('image', mouse_callback)
    cv.imshow('image',img)
        
    if cv.waitKey(20) & 0xFF == 27:
        break
    
    cv.imshow('image',img)

cv.destroyAllWindows()


# def main():
# if __name__ == "__main__":
#     main()