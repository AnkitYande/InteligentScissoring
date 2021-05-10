
import sys

class FloodFill():

    def __init__(self, w, h):
        self.selectedCells = []

    def fill(self, pathList, x, y, width, height):
        # result is the list of locations; pass it in in main code
        toFill = set()
        toFill.add((x,y))
        while not len(toFill) == 0:
            (x,y) = toFill.pop()
            loc = y*width + x
            #print(loc)
            if (loc in pathList) or y < 0 or x < 0 or x >= width or y >= height or (loc in self.selectedCells):
                continue
            self.selectedCells.append(loc)
            toFill.add((x+1, y))
            toFill.add((x-1, y))
            toFill.add((x, y+1))
            toFill.add((x, y-1))


    # def fill(self, pathList, x, y, width, height):
    #     # result is the list of locations; pass it in in main code
    #     print(pathList)
    #     loc = y*width + x
    #     if (loc in pathList) or y < 0 or x < 0 or x >= width or y >= height or (loc in self.filledCells):
    #         return
    #     # print(loc)

    #     self.filledCells.append(loc)

    #     self.fill(pathList, x+1, y, width, height)
    #     self.fill(pathList, x-1, y, width, height)
    #     self.fill(pathList, x, y+1, width, height)
    #     self.fill(pathList, x, y-1, width, height)

            


