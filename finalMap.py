# ENPM 661 PROJECT 2
# Varun Asthana, Jaad Lepak, Anshuman Singh

# =====SECTION 1: LIBRARIES=====
import numpy as np
import copy as cp
import math
import matplotlib.pyplot as plt
import cv2
import time

# =====SECTION 2: MAPS=====

# Final fixed map that has five obstacles
class FinalMap():
    def __init__(self, height, width, clr):
        """Initializes final map
        height:     row dimension [pixels]
        width:      column dimension [pixels]
        clr:        clearance from map border"""
        height+=1
        width+=1
        self.c = clr
        self.grid= np.ones([height,width,3], dtype ='uint8')*255
        # self.steps= ['T','L','R','B','TL', 'TR', 'BL', 'BR']
        self.grid[0:(clr+1),:,0] = 0
        self.grid[height-(clr+1):height,:,0] = 0
        self.grid[:,0:(clr+1),0] = 0
        self.grid[:, width-(clr+1):width,0] = 0

    # Obstacle in top left
    def shape1(self):
        """Fixed polygon shape for obstacle in top-left of map"""
        m1, c1 = 13.0, -140
        m2, c2 = 0, 185
        m3, c3 = 7.0/5, 80
        m4, c4 = 1, 100
        m5, c5 = -(7.0/5), 290
        m6, c6 = (6.0/5), 30
        m7, c7 = -(6.0/5), 210
        for x in range(self.grid.shape[1]/2):
            for y in range (self.grid.shape[0]):
                y1= m1*x + c1 + (self.c)*math.sqrt(1+(m1**2))
                y2= m2*x + c2 + (self.c)*math.sqrt(1+(m2**2))
                y3= m3*x + c3 - (self.c)*math.sqrt(1+(m3**2))
                y4= m4*x + c4 - (self.c)*math.sqrt(1+(m4**2))
                if(y<=y1 and y<=y2 and y>=y3 and y>=y4):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=0
                y3a= m3*x + c3 + (self.c)*math.sqrt(1+(m3**2))
                y5= m5*x + c5 + (self.c)*math.sqrt(1+(m5**2))
                y6= m6*x + c6 - (self.c)*math.sqrt(1+(m6**2))
                y7= m7*x + c7 - (self.c)*math.sqrt(1+(m7**2))
                if(y<=y3a and y<=y5 and y>=y6 and y>=y7):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=0

                if(y<=y2 and y>y5 and y>(self.c) and y<(self.grid.shape[0]-(self.c+1))):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=255

                if(y>y2 and y<y3a and y>(self.c) and y<(self.grid.shape[0]-(self.c+1))):
                    self.grid[self.grid.shape[0]-1-y,x, 0]=255
        # Highlighting the vertices of the polygons
        self.grid[self.grid.shape[0]-1-120,75,0:2]= 0
        self.grid[self.grid.shape[0]-1-185,25,0:2]= 0
        self.grid[self.grid.shape[0]-1-185,75,0:2]= 0
        self.grid[self.grid.shape[0]-1-150,100,0:2]= 0
        self.grid[self.grid.shape[0]-1-150,50,0:2]= 0
        self.grid[self.grid.shape[0]-1-120,20,0:2]= 0
        return

    # Obstacle in center
    def ellipse(self, major, minor, h, w):
        """Customiazble ellipse obstacle
            major:  major axis dimension [pixels]
            minor:  minor axis dimension [pixels]
            h:      ellipse center location in map's coordinate system
            w:      ellipse center location in map's coordinate system"""
        finalMajor= major + self.c
        finalMinor= minor + self.c
        if(h- finalMinor <=0):
            ha= 0
        else:
            ha= h - finalMinor
        if(h+finalMinor >= self.grid.shape[0]):
            hb= self.grid.shape[0]
        else:
            hb= h + finalMinor

        if(w- finalMajor <=0):
            wa= 0
        else:
            wa= w-finalMajor

        if(w+finalMajor >= self.grid.shape[1]):
            wb= self.grid.shape[1]
        else:
            wb= w + finalMajor

        for i in range(wa, wb):
            for j in range(ha, hb):
                if ((float(i - w) / finalMajor) ** 2 + (float(j - h) / finalMinor) ** 2) <= 1:
                    self.grid[200-j, i, 0] = 0
        return

    # Obstacle in top right
    def circ(self, radius, h, w):
        """Customizable circle obstacle
            radius:     radius dimention [pixels]
            h:          circle center location in map's coordinate system
            w:          circle center location in map's coordinate system"""
        finalRad = radius + self.c
        if(h-finalRad<0):
            ha=0;
        else:
            ha= h - finalRad

        if(h+finalRad >= self.grid.shape[0]):
            hb= self.grid.shape[0]
        else:
            hb= h + finalRad

        if(w-finalRad<0):
            wa=0;
        else:
            wa= w - finalRad

        if(w+finalRad >= self.grid.shape[1]):
            wb= self.grid.shape[1]
        else:
            wb= w + finalRad

        for h_ in range(ha, hb):
            for w_ in range(wa, wb):
                eqn= (h_-h)**2 + (w_-w)**2
                if(eqn<=(finalRad**2)):
                    self.grid[h_,w_,0] = 0
        return

    # Obstacle in bottom right
    def rohmbus(self):
        """Fixed polygon shape for obstacle in bottom-right of map"""
        m1, c1 = -(3.0/5), 295
        m2, c2 = (3.0/5), 25
        m3, c3 = -(3.0/5), 325
        m4, c4 = (3.0/5), 55

        # for y in range(self.grid.shape[0]):
        for x in range(self.grid.shape[1]):
            for y in range (self.grid.shape[0]):
                y1= m1*x + c1 - (self.c)*math.sqrt(1+(m1**2))
                y2= m2*x + c2 - (self.c)*math.sqrt(1+(m2**2))
                y3= m3*x + c3 + (self.c)*math.sqrt(1+(m3**2))
                y4= m4*x + c4 + (self.c)*math.sqrt(1+(m4**2))
                if(y>=y1 and y>=y2 and y<=y3 and y<=y4):
                    self.grid[y,x, 0]=0
        # Highlighting the rohmbus vertices
        self.grid[175,200,0:2]= 0
        self.grid[160,225,0:2]= 0
        self.grid[175,250,0:2]= 0
        self.grid[190,225,0:2]= 0
        return

    # Obstacle in bottom left
    def rect(self):
        """Fixed polygon shape for obstacle in bottom-left of map"""
        m1, c1 = -(9.0/5), 186
        m2, c2 = (38.0/65), (1333.0/13)
        m3, c3 = -(9.0/5), 341
        m4, c4 = (38.0/65), (1488.0/13)
        for x in range(self.grid.shape[1]):
            for y in range (self.grid.shape[0]):
                y1= m1*x + c1 - (self.c)*math.sqrt(1+(m1**2))
                y2= m2*x + c2 - (self.c)*math.sqrt(1+(m2**2))
                y3= m3*x + c3 + (self.c)*math.sqrt(1+(m3**2))
                y4= m4*x + c4 + (self.c)*math.sqrt(1+(m4**2))
                if(y>=y1 and y>=y2 and y<=y3 and y<=y4):
                    self.grid[y,x, 0]=0
        # Highlighting the rectangle vertices
        self.grid[132,30,0:2]= 0
        self.grid[123,35,0:2]= 0
        self.grid[161,100,0:2]= 0
        self.grid[170,95,0:2]= 0
        return
