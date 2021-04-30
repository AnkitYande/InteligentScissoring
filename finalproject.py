import numpy as np
import cv2 as cv # OpenCV
import queue  

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

# def dijkstra(graph, source, dest):  
#     q = queue.PriorityQueue()
#     parents = []
#     distances = []
#     start_weight = float("inf")

#     for i in graph.get_vertex():
#         weight = start_weight
#         if source == i:
#             weight = 0
#         distances.append(weight)
#         parents.append(None)

#     q.put(([0, source]))

#     while not q.empty():
#         v_tuple = q.get()
#         v = v_tuple[1]

#         for e in graph.get_edge(v):
#             candidate_distance = distances[v] + e.weight
#             if distances[e.vertex] > candidate_distance:
#                 distances[e.vertex] = candidate_distance
#                 parents[e.vertex] = v
#                 q.put(([distances[e.vertex], e.vertex]))

#     shortest_path = []
#     end = dest
#     while end is not None:
#         shortest_path.append(end)
#         end = parents[end]

#     shortest_path.reverse()

#     return shortest_path, distances[dest]

### 2d array of pixels, startposx, startposy, currmouse_x, currmouse_y


def ourDijkstra(imgArr, seed_y, seed_x, mouse_y, mouse_x):
    # imgArr = imgFinal
    # print(seed_y, seed_x, mouse_y, mouse_x)

    w,h = imgArr.shape
    # print(w,h)
    weightsArr = np.full_like( imgArr, float("-inf"))
    parentsPath = np.full_like( imgArr, None, dtype=object)
    q = queue.PriorityQueue()

    weightsArr[seed_x, seed_y] = 0
    q.put( (seed_x, seed_y) )

    i = 0
    while not q.empty():
        currcoords = q.get()
        curr_x = currcoords[0] 
        curr_y = currcoords[1]
        print(curr_x, curr_y)
        i = i+1
        if(i == 100):
            return

        for col in range(curr_y-1, curr_y+2):
            for row in range(curr_x-1, curr_x+2):
                ## checking all neighbors of the current pixel
                if (row < 0 or row >= w or col < 0 or col >= h or (curr_y == col and curr_x == row)): # Check that [row, col] is not out of bounds
                    continue
                else:
                    candidateWeight = weightsArr[curr_x, curr_y] + imgArr[row, col]
                    print("checking", row, col, " weight:", candidateWeight)
                    if weightsArr[row, col] < candidateWeight:
                        weightsArr[row, col] = candidateWeight
                        parentsPath[row, col] = (curr_x, curr_y)
                        q.put((row, col))
                        # print("adding to queue")
        
        # print("parent of", parentsPath[curr_x, curr_y], "is", curr_x, curr_y)
    ##Once we have calculated the costs and determined the shortest path
    # print(parentsPath)
    shortest_path = []
    end = (mouse_x, mouse_y)
    while end is not None:
        shortest_path.append(end)
        end = parentsPath[end[0], end[1]]
    
    print(shortest_path)
    return shortest_path


seed_x = seed_y = None
def mouse_callback(event,x,y,flags,param):
    if event== 1:   #cv.EVENT_LBUTTONDOWN
        print("New seed at:", x,y)
        global seed_x 
        seed_x = x
        global seed_y 
        seed_y = y
    elif event== 4: #cv.EVENT_MOUSEMOVE
        print("end at", x,y)
        mouse_x = x
        mouse_y = y
        # cv.circle(imgFinal,(x,y),10,(255,0,0),-1)
        if(seed_x != None and seed_y != None):
            path = ourDijkstra(imgFinal, seed_x, seed_y, x, y)
            # print(len(path))
            for pixel in path:
                cv.circle(imgFinal,(pixel[0],pixel[1]),1,(255,0,0),-1)
        

########## preprocessing ##########

img = cv.imread("./imgs/pix.png") 
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert to graysacle
# img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
img = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT) # Gaussian Blur the image

######### edge detection ##########

#Horizontal and Vertical Sobel kernels
kernelH = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]]) 
                
kernelV = np.array([[ 1,  2,  1],
                    [ 0,  0,  0],
                    [-1, -2, -1]])

#aply kernels to image
w,h = img.shape
print(w,h)
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

res = ourDijkstra(imgFinal, 10, 5, 10, 20)
print(res)
# cv.setMouseCallback('image', mouse_callback)
# scissorCoords = list(x, y) ## this is a list of coordinates on the scissor path; starts with mouse x, y

while(True):
    cv.imshow('image',imgFinal)
    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()


# def main():
# if __name__ == "__main__":
#     main()