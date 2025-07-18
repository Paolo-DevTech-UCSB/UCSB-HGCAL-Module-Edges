# -*- coding: utf-8 -*-
"""
Offsets_SR - A Sensor Tolerance Process
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
w_b = (w + w_t)/2             #Baseplate Envelope, Maximum Allowed Apothem
s = (166.57)/2                #Sensor Width (Tolerances are negligible for sensors) (Hamamatsu does a good job) 
scr = s/np.cos(0.523599)      #Circumcircle radius of Sensor 
r_y = w_n                     #YELLOW Envelope = Baseplate Envelope
r_r = w_b                       #RED Envelope = Baseplate Envelope
m = np.sqrt(3);               #Slope of the sides of a hexagon

#print(scr, w_n)

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
    v1_o= False; v2_o= False; v3_o= False; v4_o= False; v5_o= False; v6_o = False; 

    #Check Each Verticie for Its location with respect to 3 established Envelopes, assign a colorgrade
    #V1 - Top Left
    if v1[1] <= r_r and v1[1] <= (m*v1[0] + r_r*2):
        if v1[1] <= r_y and v1[1] <= (m*v1[0] + r_y*2):
            v1_g = True;
        else: 
            v1_o = True;
    else: 
        v1_r = True;
    
    #V2 - Top right
    if v2[1] <= r_r and v2[1] <= (-m*v2[0] + r_r*2):
        if v2[1] <= r_y and v2[1] <= (-m*v2[0] + r_y*2):
            v2_g = True;
        else: 
            v2_o = True;
    else: 
        v2_r = True;
    
    #V3 - Mid right
    if v3[1] >= (m*v3[0] - r_r*2) and v3[1] <= (-m*v3[0] + r_r*2):
        if v3[1] >= (m*v3[0] - r_y*2) and v3[1] <= (-m*v3[0] + r_y*2):
            v3_g = True;
        else: 
            v3_o = True;
    else: 
        v3_r = True;
    

    #V4 - Bottom Right
    if v4[1] >= -r_r and v4[1] >= (m*v4[0] - r_r*2):
        if v4[1] >= -r_y and v4[1] >= (m*v4[0] - r_y*2):
            v4_g = True;
        else: 
            v4_o = True;
    else: 
        v4_r = True;
        
    
    #V5 - Bottom Right
    if v5[1] >= -r_r and v5[1] <= (-m*v5[0] + r_r*2):
        if v5[1] >= -r_y and v5[1] <= (-m*v5[0] + r_y*2):
            v5_g = True;
        else: 
            v5_o = True;    
    else: 
        v5_r = True;    
    

    #V6 - Bottom Right
    if v6[1] >= (-m*v6[0] - r_r*2) and v6[1] <= (m*v6[0] + r_r*2):
        if v6[1] >= (-m*v6[0] - r_y*2) and v6[1] <= (m*v6[0] + r_y*2):
            v6_g = True;
        else: 
            v6_o = True;    
    else: 
        v6_r = True;    
        

    if v1_r:
        S1 = 'Red'
    elif v1_o:
        S1 = 'Yellow'
    elif v1_g:
        S1 = 'Green'
        

    if v2_r:
        S2 = 'Red'
    elif v2_o:
        S2 = 'Yellow'
    elif v2_g:
        S2 = 'Green'


    if v3_r:
        S3 = 'Red'
    elif v3_o:
        S3 = 'Yellow'
    elif v3_g:
        S3 = 'Green'


    if v4_r:
        S4 = 'Red'
    elif v4_o:
        S4 = 'Yellow'
    elif v4_g:
        S4 = 'Green'
        

    if v5_r:
        S5 = 'Red'
    elif v5_o:
        S5 = 'Yellow'
    elif v5_g:
        S5 = 'Green'


    if v6_r:
        S6 = 'Red'
    elif v6_o:
        S6 = 'Yellow'
    elif v6_g:
        S6 = 'Green'

    #Return the Colorgrade for each of the 6 Verticies. 
    #print(S1, S2, S3, S4, S5, S6) 
    return S1, S2, S3, S4, S5, S6
    
    #print(v1_g)
    
#Main(-0.2,-0.1,0.500)