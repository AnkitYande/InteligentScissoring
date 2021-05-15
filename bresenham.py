def bresenham(x1,y1,x2, y2, width, height, allPaths):

    dx = x2 - x1
    dy = y2 - y1
    dx_abs = abs(dx)
    dy_abs = abs(dy)
    px = 2 * dy_abs - dx_abs
    py = 2 * dx_abs - dy_abs
    
    # The line is X-axis dominant
    if (dy_abs <= dx_abs): 
        if (dx >= 0): # Line is drawn left to right
            x = x1 
            y = y1 
            xe = x2
        else: # Line is drawn right to left (swap ends)
            x = x2 
            y = y2 
            xe = x1
        
        loc = y*width + x
        allPaths.append( loc )
        
        i = 0
        while (x < xe):
            x = x + 1
            if (px < 0):
                px = px + 2 * dy_abs
            else :
                if ((dx < 0 and dy < 0) or (dx > 0 and dy > 0)):
                    y = y + 1
                else:
                    y = y - 1
                px = px + 2 * (dy_abs - dx_abs)
   
            loc = y*width + x
            allPaths.append( loc )
            i += 1

    # The line is Y-axis dominant
    else: 
       
        if (dy >= 0): # Line is drawn bottom to top
            x = x1 
            y = y1 
            ye = y2
        else: # Line is drawn top to bottom
            x = x2 
            y = y2 
            ye = y1

        loc = y*width + x
        allPaths.append( loc )
        
        i = 0
        while(y < ye):
            y = y + 1
            if (py <= 0):
                py = py + 2 * dx_abs
            else:
                if ((dx < 0 and dy<0) or (dx > 0 and dy > 0)):
                    x = x + 1
                else:
                    x = x - 1
                py = py + 2 * (dx_abs - dy_abs)

            loc = y*width + x
            allPaths.append( loc )
            i += 1