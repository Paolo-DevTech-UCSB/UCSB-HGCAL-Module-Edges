# UCSB-HGCAL-Module-Edges
A geometrical tool for the placement and tiling mechanics of the HGCAL Modules and Cassette
    By Paolo Jordano, Sussanne Kyre
Explaination:
    (M.O.) Reduce Module Rejection from HGCAL MACs
    By Assigning The Modules with This Colorgrading system, We Introduce a means of finding the tilability of badly placed modules.
        Tiliability Rules: 
            Red Corners Make a Module Untileable. 
            Yellow Corners can only be installed next to purple corners. 

The Envelopes:
_______________________________________________________
|   -50% Gap     0% Gap      50% Gap     100% Gap       |
|        |   Purple  |   Green   |  Yellow   |   Red    |
________________________________________________________


Part 1: Offsets: offsets.py 
A Hexaboard Placement Analysis Tool
By: Paolo Jordano
original creation date: 6/24/2025

    Summary: 
        1. Establish Tolerance and Nominal Values of Hexaboard
        2. Establish 6 Verticies of the Hexagon In a Polar Coordinate system, Apply Angular Offsets
        3. Convert to Cartisian Coordinate system, Apply Linear Offsets
        4. Check Each Verticie for Its location with respect to 3 established Envelopes, assign a colorgrade
        5. Return the Colorgrade for each of the 6 Verticies. 

Part 2: OffsetsController.py
 Discription:
    A framework for testing large datasets and drawing conclusions. 
    OffsetController contains no geometery, 
    It is Just for displaying, reading, and organizing data. 

`   Summary: 
        1. Recives a set of offsets from input, requests Offsets returns the colorgrade of the hexagons verticies.
        2. Organizes Data into Visualizations.


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
























OverFlow Notes and Explainations:
# From My Own measurements; Actual Value for Hexaboard Apothem r: 
#   PRESERIES HDF avg: 83.37086806
#   PRESERIES LDF avg: 83.39973333
#   PRESERIES LD5 avg: 83.381375

"""Definition; Apothem: The line segment from the center of the hexagon to the midpoint of any side."""

    

    PROCESS

    
Purple is just "Edge Location" - Gap/2. However There are a few choices within that definition:
    1. Are we using 83.40 or 83.47 for the "Edge Location"
    2. is the tolerance for "Edge Location" 0.05mm, 0.013mm, or both: 0.063mm
        3 * 2, Gives us 6 different possibilities for what "Edge Location" is. 
    3. for Gap, we could use the Warm or Cold Gap.
        3 * 2 * 2 gives 12 different possibilities for the Purple Envelope. 

The Green Edge is the easiest, By Definition, It is NOT     purple, yellow, and red. 
    1.    Purple Envelope < Green < Yellow Envelope

The Yellow Envelope also follows similar rules to the Purple Envelope. "Edge Location" + Gap/2
    1.  Are we using 83.40 or 83.47 for the "Edge Location"
    2. is the tolerance for "Edge Location" 0.05mm, 0.013mm, or both: 0.063mm
    3. for Gap, we could use the Warm or Cold Gap.

The Red Envelope is the same as Yellow except it's Edge Loco + Gap. no term multiplyed by 1/2. 

               ( HXB Width + HXB Total Tolerance*(2 modules))/(2) + relative gap location
    Yellow == ((166.79 + 0.363)/2)mm + (243.5)um       ''''
    RED == ((166.79 + 0.363)/2)mm + (487)um            ''''