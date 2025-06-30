# UCSB-HGCAL-Module-Edges
A short geometrical study on the placement and tiling mechanics of the HGCAL Modules and Cassette

Part 1: Offsets: offsets.py 
A Hexaboard Placement Analysis Tool
By: Paolo Jordano
original creation date: 6/24/2025

Part 2: OffsetsController.py
A framework for testing large datasets and drawing conclusions. 




OverFlow Notes and Explainations:
# From My Own measurements; Actual Value for Hexaboard Apothem r: 
#   PRESERIES HDF avg: 83.37086806
#   PRESERIES LDF avg: 83.39973333
#   PRESERIES LD5 avg: 83.381375

"""Definition; Apothem: The line segment from the center of the hexagon to the midpoint of any side."""

    

    PROCESS

1.The Nominal Apothem of a hexaboard is 83.47
2.The Measured Value is lower, but is not being used becuase
    a. there are small parts that protrude past the edge, (artifacts created from cutting out the PCB)
    b. By Adopting 83.47 instead of 83.40, (We are being MORE conservative/careful)
3.We add 0.05 to that value to account for the 0.05mm of tolerance. (Also being MORE conservtive/careful)
4.Radius is Calculated From that Number: Radius = (83.52/np.sqrt(3))

    Explaination

The Envelopes, 
            -50% Gap     0% Gap      50% Gap     100% Gap
                |   Purple  |   Green   |  Yellow   |   Red    |
The purpose of these envelopes is the calssify each corner into these four classes

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