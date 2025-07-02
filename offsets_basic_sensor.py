# -*- coding: utf-8 -*-
"""
OffsetsJoeLight - A Hexaboard and Sensor Placement Analysis Tool
By: Paolo Jordano
6/24/2025
"""

import numpy as np
import math

"""Establishing the Nominals, Tolerances, and Tiling Conditions of the Modules and Casstte."""
#Casstte Gap Size at Operating and Room Tempurature (mm);
    #from Susanne Kyre's 6/24/25 UCSB MAC group meeting slides:

w = 166.94                    #Baseplate Nominal Width
w_t = 0.2                     #Baseplate Wodth tolerance
w_n = (w - w_t)/2             #Baseplate Envelope, Minimum Allowed Apothem
s = (166.57)/2                #Sensor Width (Tolerances are negligible for sensors) (Hamamatsu does a good job) 
scr = s/np.cos(0.523599)      #Circumcircle radius of Sensor 
r_r = w_n                     #Red Envelope = Baseplate Envelope
m = np.sqrt(3);               #Slope of the sides of a hexagon

#print(s, w_n)

def Main(Xoff, Yoff, ThetaOff):
    AngleOff = ThetaOff;
    
    #Establishing Polar Coorinates for Each Corner, Adding Polar Offsets
    v1_o = [scr, 120 + AngleOff];
    v2_o = [scr, 60 + AngleOff];
    v3_o = [scr, 0  + AngleOff];
    v4_o = [scr, 300 + AngleOff];
    v5_o = [scr, 240 + AngleOff];
    v6_o = [scr, 180 + AngleOff]; 
    
    #Converting Polar Coordinates to Cartisian, Adding Cartisian Offsets
    v1 = (v1_o[0] * math.cos(math.radians(v1_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v1_o[1]))+ Yoff)
    v2 = (v1_o[0] * math.cos(math.radians(v2_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v2_o[1]))+ Yoff)
    v3 = (v1_o[0] * math.cos(math.radians(v3_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v3_o[1]))+ Yoff)
    v4 = (v1_o[0] * math.cos(math.radians(v4_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v4_o[1]))+ Yoff)
    v5 = (v1_o[0] * math.cos(math.radians(v5_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v5_o[1]))+ Yoff)
    v6 = (v1_o[0] * math.cos(math.radians(v6_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v6_o[1]))+ Yoff)
    
    v1_r= False; v2_r= False; v3_r= False; v4_r= False; v5_r= False; v6_r = False; 

    #Check Each Verticie for Its location with respect to 3 established Envelopes, assign a colorgrade
    #V1 - Top Left
    if v1[1] <= r_r and v1[1] <= (m*v1[0] + r_r*2):
        v1_r = False;
    else: 
        v1_r = True;
    
    #V2 - Top right
    if v2[1] <= r_r and v2[1] <= (-m*v2[0] + r_r*2):
        v2_r = False;
    else: 
        v2_r = True;
    
    #V3 - Mid right
    if v3[1] >= (m*v3[0] - r_r*2) and v3[1] <= (-m*v3[0] + r_r*2):
        v3_r = False;
    else: 
        v3_r = True;
    

    #V4 - Bottom Right
    if v4[1] >= -r_r and v4[1] >= (m*v4[0] - r_r*2):
        v4_r = False;
    else: 
        v4_r = True;
        
    
    #V5 - Bottom Right
    if v5[1] >= -r_r and v5[1] <= (-m*v5[0] + r_r*2):
        v5_r = False;
    else: 
        v5_r = True;    
    

    #V6 - Bottom Right
    if v6[1] >= (-m*v6[0] - r_r*2) and v6[1] <= (m*v6[0] + r_r*2):
        v6_r = False;
    else: 
        v6_r = True;    
        

    if v1_r:
        S1 = 'Red'
    else:
        S1 = 'Green'
        

    if v2_r:
        S2 = 'Red'
    else:
        S2 = 'Green'


    if v3_r:
        S3 = 'Red'
    else:
        S3 = 'Green'


    if v4_r:
        S4 = 'Red'
    else:
        S4 = 'Green'
        

    if v5_r:
        S5 = 'Red'
    else:
        S5 = 'Green'


    if v6_r:
        S6 = 'Red'
    else:
        S6 = 'Green'

    #Return the Colorgrade for each of the 6 Verticies. 
    print(S1, S2, S3, S4, S5, S6) 
    return S1, S2, S3, S4, S5, S6
    
    #print(v1_g)
    
#Main(-0.2,-0.1,0.500)