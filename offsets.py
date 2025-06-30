# -*- coding: utf-8 -*-
"""
OffsetsJoeLight - A Hexaboard and Sensor Placement Analysis Tool
By: Paolo Jordano
6/24/2025
"""

"""
    Q&A

Q.1: What is the default distance between center locating pins in the cassette?
    A: 166.94 is the Nominal Baseplate Width, + the Nominal Gap width should be 0.700 so....
    167.64 is Baseplate width + gap. (Theoretically this is the same distance from one center hole to another)
    this number appies for both HXB and baseplate

Q.2: Is Susanne's Gap calculation including the tolerance of the hexaboard width?
    A: YES, In a world where X, Y, and Theta are all zero (the Control) and the Tolerance is the Independent variable.
    The HXB Gap would have a minimum of 487um, and a max of 850um
Q.2b: What does this mean for how we treat the purple, yellow, and red envelopes?
    Lets Call the 700um gap the Theoretical Gap, and lets call the 487um the "Gap left for offsets"
    The purple envelope should be the nominal + tolerance Edge location -"Gap left for Offsets"/2

    Nominal Hexaboard Width: 166.79
    Nominal RT Hexaboard GAP: 0.850um
    Nominal RT CenterPin_Distance = (166.79 + 0.850) = 167.64             167.64 = 
    RT Middle Line = CenterPin_distance/2 = 83.82

    This is what we've been calling HXB 50% gap : 83.82

    Minimum Gap At RT = 487um
    Min Half Gap RT = 243.5um

    Maximum Extension of Hexaboard under the Influence of the hexaboard tolerances:
    83.82 - 0.2435 = 83.5765

    this is what I've been calling HXB 0% gap :: 83.5765

    Which makes the opposite 100 % :: 84.0635    
    83.82 + 0.2435 = 84.0635
    
Q.2c: What is the proper interpretation of  "50% of the gap"?
    A: Midpoint between two centerpins on the cassette.

Q.3 Why doesnt the Gap grow when the environement goes to cold?
    A: you forget the Cassete itself, it also moves. Use the Warm Gap to avoid confusion. 


"""

import numpy as np
import math

"""Establishing the Nominals, Tolerances, and Tiling Conditions of the Modules and Casstte."""
#Casstte Gap Size at Operating and Room Tempurature (mm);
    #from Susanne Kyre's 6/24/25 UCSB MAC group meeting slides:
#Minimum Gap at Rt
WarmGap = 0.487;
#Minimum Half Gap at RT:
HalfGap = WarmGap/2;

#Hexagon Size and Gap Size
w = 166.79
w_t = 0.850
w_naut = w_t + w
Env_Yellow = w_naut/2
Env_Purple = Env_Yellow - HalfGap
Env_Red    = Env_Yellow + HalfGap

#CLean This UP VVVVVVVVVVVVVVVVVVVVVVV

# Circumcircle Radius (@edge of tolerance) -->  cos(30) = adj/hpt    hpt = adj/cos(30deg)  
cr = r_naut/np.cos(0.523599)
R = 2*cr

# Slope of a hexagons sides that arent parallel to an axis:
m = np.sqrt(3);

#print("Apothem,"","","","",)


#Defining our Grading Envelopes
# Apothem : r, Nominal Hexaboard Value: 83.395
r = 83.394999999

    #green is by definition, not the other 3. 
r_p = cr - WarmGap/2; #~83.2765   Nominal - 50% Gap
r_y = cr + WarmGap/2; #~83.7635   Nominal + 50% Gap
r_r = cr + WarmGap;   #~84.007    Nominal + 100% Gap
    
#print(r_p, r_y, r_r)    

#Main:
#Takes 3 Offsets as Inputs and Outputs the Status of Corners on a hexabaord. 

def Main(Xoff, Yoff, ThetaOff):
    AngleOff = ThetaOff;
    
    #Establishing Polar Coorinates for Each Corner, Adding Polar Offsets
    #Using R: Hypotenuse of a a hexagon with the Apothem of 83.47 + 0.05
    v1_o = [cr, 120 + AngleOff];
    v2_o = [cr, 60 + AngleOff];
    v3_o = [cr, 0  + AngleOff];
    v4_o = [cr, 300 + AngleOff];
    v5_o = [cr, 240 + AngleOff];
    v6_o = [cr, 180 + AngleOff]; 
    
    #Converting Polar Coordinates to Cartisian, Adding Cartisian Offsets
    v1 = (v1_o[0] * math.cos(math.radians(v1_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v1_o[1]))+ Yoff)
    v2 = (v1_o[0] * math.cos(math.radians(v2_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v2_o[1]))+ Yoff)
    v3 = (v1_o[0] * math.cos(math.radians(v3_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v3_o[1]))+ Yoff)
    v4 = (v1_o[0] * math.cos(math.radians(v4_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v4_o[1]))+ Yoff)
    v5 = (v1_o[0] * math.cos(math.radians(v5_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v5_o[1]))+ Yoff)
    v6 = (v1_o[0] * math.cos(math.radians(v6_o[1])) + Xoff, v1_o[0] * math.sin(math.radians(v6_o[1]))+ Yoff)
    


    # Checking the coordinate values of the verticies against the purple envelope.
        # y < 83.2765
    if v1[1] <= r_p:
        if v1[1] <= (m*v1[0] + r_p*2):
            v1_p = True;
        else:
            v1_p = False;
    else: 
        v1_p = False;
        
        
        
    if v2[1] <= r_p:
        if v2[1] <= (-m*v2[0] + r_p*2):
            v2_p = True;
        else: 
            v2_p = False;
    else: 
        v2_p = False;
        
        
        
    if v3[1] <= (-m*v3[0] + r_p*2):
        if v3[1] >= (m*v3[0] - r_p*2):
            v3_p = True;
        else: 
            v3_p = False;
    else: 
        v3_p = False;
    
    
    
    if v4[1] >= -r_p:
        if v4[1] >= (m*v4[0] - r_p*2):
            v4_p = True;
        else: 
            v4_p = False;
    else: 
        v4_p = False;
        
        
        
    if v5[1] >= -r_p:
        if v5[1] >= (-m*v5[0] - r_p*2):
            v5_p = True;
        else: 
            v5_p = False;
    else: 
        v5_p = False;
        
        
        
    if v6[1] >= (-m*v6[0] - r_p*2):
        if v6[1] <= (m*v6[0] + r_p*2):
            v6_p = True;
        else: 
            v6_p = False;
    else: 
        v6_p = False;
        
    

    #print(v1[1], r)
    
    
    
    
    if v1[1] <= r:
        if v1[1] <= (m*v1[0] + r*2):
            v1_g = True;
            v1_y = False;
            v1_r = False;
        else:
            v1_g = False;
            v1_y = False;
            v1_r = False;

        if v1[1] <= r_y:
            if v1[1] <= (m*v1[0] + r_y*2):
                v1_y = True;
        else: 
            v1_y = False;
            v1_r = True;


        
        
    if v2[1] <= r:
        if v2[1] <= (-m*v2[0] + r*2):
            v2_g = True;
            v2_y = False;
            v2_r = False;
        else:
            v2_g = False;
            v2_y = False;
            v2_r = False;
    else: 
        v2_g = False;
        if v2[1] <= r_y:
            if v2[1] <= (-m*v2[0] + r_y*2):
                v2_y = True;
                v2_r = False;
        else: 
            v2_y = False;
            v2_r = True;
                
                
    #print(v3[1] , (-m*v3[0] + r_y*2))
    #print(v3[1] , (m*v3[0] - r_y*2))
    
    if v3[1] <= (-m*v3[0] + r*2):
        if v3[1] >= (m*v3[0] - r*2):
            v3_g = True;
            v3_y = False;
            v3_r = False;
        else:
            v2_g = False;
            v3_y = False;
            v3_r = False;
    else: 
        v3_g = False;
        if v3[1] <= (-m*v3[0] + r_y*2):
            if v3[1] >= (m*v3[0] - r_y*2):
                v3_y = True;
                v3_r = False;
        else: 
            v3_y = False;
            v3_r = True;

        
    if v4[1] >= -r:
        if v4[1] >= (m*v4[0] - r*2):
            v4_g = True;
            v4_y = False;
            v4_r = False;
        else:
            v4_g = False;
            v4_y = False;
            v4_r = False;


    if v4[1] >= -r_y:
        if v4[1] >= (m*v4[0] - r_y*2):
            v4_y = True;
            v4_r = False;
    else: 
        v4_y = False;
        v4_r = True;

                
        
    if v5[1] >= -r:
        if v5[1] >= (-m*v5[0] - r*2):
            v5_g = True;
            v5_y = False;
            v5_r = False;
        else:
            v5_g = False;
            v5_y = False;
            v5_r = False;
    else: 
        v5_g = False;
        if v5[1] >= -r_y:
            if v5[1] >= (-m*v5[0] - r_y*2):
                v5_y = True;
                v5_r = False;
        else: 
            v5_y = False;
            v5_r = True;
            

        
    if v6[1] >= (-m*v6[0] - r*2):
        if v6[1] <= (m*v6[0] + r*2):
            v6_g = True;
            v6_y = False;
            v6_r = False;
        else:
            v6_g = False;
            v6_y = False;
            v6_r = False;
    else: 
        v6_g = False;
        if v6[1] >= (-m*v6[0] - r_y*2):
            if v6[1] <= (m*v6[0] + r_y*2):
                v6_y = True;
                v6_r = False;
        else: 
            v6_y = False;
            v6_r = True;

    #print('Purple:',v1_p, v2_p, v3_p, v4_p, v5_p, v6_p)
    #print('Green:',v1_g, v2_g, v3_g, v4_g, v5_g, v6_g)
    #print('Yellow:',v1_y, v2_y, v3_y, v4_y, v5_y, v6_y)
    #print('Red:',v1_r, v2_r, v3_r, v4_r, v5_r, v6_r)
    
    if v1_p:
        S1 = 'Purple'
    elif v1_g:
        S1 = 'Green'
    elif v1_y:
        S1 = 'Yellow'
    elif v1_r:
        S1 = 'Red'
    else:
        S1 = 'Unknown'
        
    if v2_p:
        S2 = 'Purple'
    elif v2_g:
        S2 = 'Green'
    elif v2_y:
        S2 = 'Yellow'
    elif v2_r:
        S2 = 'Red'
    else:
        S2 = 'Unknown'

    if v3_p:
        S3 = 'Purple'
    elif v3_g:
        S3 = 'Green'
    elif v3_y:
        S3 = 'Yellow'
    elif v3_r:
        S3 = 'Red'
    else:
        S3 = 'Unknown'

    if v4_p:
        S4 = 'Purple'
    elif v4_g:
        S4 = 'Green'
    elif v4_y:
        S4 = 'Yellow'
    elif v4_r:
        S4 = 'Red'
    else:
        S4 = 'Unknown'
        
    if v5_p:
        S5 = 'Purple'
    elif v5_g:
        S5 = 'Green'
    elif v5_y:
        S5 = 'Yellow'
    elif v5_r:
        S5 = 'Red'
    else:
        S5 = 'Unknown'

    if v6_p:
        S6 = 'Purple'
    elif v6_g:
        S6 = 'Green'
    elif v6_y:
        S6 = 'Yellow'
    elif v6_r:
        S6 = 'Red'
    else:
        S6 = 'Unknown'

    print(S1, S2, S3, S4, S5, S6)

    

    



    
    
    #print(v1_g)
    
Main(0,0,0.000)