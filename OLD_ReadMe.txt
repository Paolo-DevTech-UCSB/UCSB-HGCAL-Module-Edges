

Older Documentation:

Explaination of Hexaboard Changes:
    (M.O.) Reduce Module Rejection from HGCAL MACs
    By Assigning The Modules with This Colorgrading system, We Introduce a means of finding the tilability of badly placed modules.
        Tiliability Rules: 
            Red Corners Make a Module Untileable. 
            Yellow Corners can only be installed next to purple corners. 

The Envelopes:
        |   -50% Gap     0% Gap      50% Gap     100% Gap       |
        |        |   Purple  |   Green   |  Yellow   |   Red    |



Part 1: Offsets: offsets.py 

    Summary: 
        1. Establish Tolerance and Nominal Values of Hexaboard
        2. Establish 6 Verticies of the Hexagon In a Polar Coordinate system, Apply Angular Offsets
        3. Convert to Cartisian Coordinate system, Apply Linear Offsets
        4. Check Each Verticie for Its location with respect to 3 established Envelopes, assign a colorgrade
        5. Return the Colorgrade for each of the 6 Verticies. 

Part 2: OffsetsController.py
 Discription:
    Summary: 
        1. Recives a set of offsets from input, requests Offsets.py returns the colorgrade of the hexagons verticies.
        2. Organizes Data into Visualizations.
    
Q&A

Q.1: What is the default distance between center locating pins in the cassette?
    A: 166.94 is the Nominal Baseplate Width, + the Nominal Gap width should be 0.700 so....
    167.64 is Baseplate width + gap. (Theoretically this is the same distance from one center hole to another)
    this number can be calculated from both HXB and baseplate (gap + width).

Q.2: Is Susanne's Gap calculation including the tolerance of the hexaboard width?
    A: YES, In a world where X, Y, and Theta are all zero (the Control) and the Tolerance is the Independent variable.
    The HXB Gap would have a minimum of 487um, and a max of 850um
Q.2b: What does this mean for how we treat the purple, yellow, and red envelopes?
    Lets Call the 700um gap the Theoretical Gap, and lets call the 487um the "Gap left for offsets" (or "Gap Left after effects of all tolerances")
    The purple envelope should be the nominal + tolerance Edge location -"Gap left for Offsets"/2

    Nominal Hexaboard Width: 166.79
    Nominal RT Hexaboard GAP: 0.850um
    Nominal RT CenterPin_Distance = (166.79 + 0.850) = 167.64         
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
