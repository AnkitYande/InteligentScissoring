def bresenham(x1,y1,x2, y2, width, height, allPaths):
    # Iterators, counters required by algorithm
    # Calculate line deltas
    dx = x2 - x1
    dy = y2 - y1
    # Create a positive copy of deltas (makes iterating easier)
    dx_abs = abs(dx)
    dy_abs = abs(dy)
    # Calculate error intervals for both axis
    px = 2 * dy_abs - dx_abs
    py = 2 * dx_abs - dy_abs
    
    # The line is X-axis dominant
    if (dy_abs <= dx_abs): 
        # Line is drawn left to right
        if (dx >= 0):
            x = x1 
            y = y1 
            xe = x2
        else: # Line is drawn right to left (swap ends)
            x = x2 
            y = y2 
            xe = x1
        
        #print(x, y) # Draw first pixel
        loc = y*width + x
        allPaths.append( loc )
        
        # Rasterize the line
        i = 0
        while (x < xe):
            x = x + 1
            # Deal with octants...
            if (px < 0):
                px = px + 2 * dy_abs
            else :
                if ((dx < 0 and dy < 0) or (dx > 0 and dy > 0)):
                    y = y + 1
                else:
                    y = y - 1
                px = px + 2 * (dy_abs - dx_abs)
            # Draw pixel from line span at
            # currently rasterized position
            # print(x, y)
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

        # print(x, y) # Draw first pixel
        loc = y*width + x
        allPaths.append( loc )
        
        # Rasterize the line
        i = 0
        while(y < ye):
            y = y + 1
            # Deal with octants...
            if (py <= 0):
                py = py + 2 * dx_abs
            else:
                if ((dx < 0 and dy<0) or (dx > 0 and dy > 0)):
                    x = x + 1
                else:
                    x = x - 1
                py = py + 2 * (dx_abs - dy_abs)

            # Draw pixel from line span at
            # currently rasterized position
            # print(x, y)
            loc = y*width + x
            allPaths.append( loc )
            i += 1