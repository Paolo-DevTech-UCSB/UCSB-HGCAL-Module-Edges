# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:09:43 2025

@author: Admin
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import offsets_basic_sensor as test

# Define parameter ranges
#angles =[1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.00781, 0.0039, 0.00195, 0, 0, -0.00195, -0.0039, -0.00781, -0.015625, -0.03125, -0.0625, -0.125, -0.25, -0.5, -1]
#angles = [0.7, 0.5, 0.35, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.00781, 0]
angles = [0.5, 0.250, 0.1250, 0.0625, 0.03125, 0.0156, 0.0078125, 0.0039, 0.00195, 0.0]
#xoffs = [1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.00781, 0.0039, 0.00195, 0, 0, -0.00195, -0.0039, -0.00781, -0.015625, -0.03125, -0.0625, -0.125, -0.25, -0.5, -1] # mm
#yoffs = [1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.00781, 0.0039, 0.00195, 0, 0, -0.00195, -0.0039, -0.00781, -0.015625, -0.03125, -0.0625, -0.125, -0.25, -0.5, -1] # mm


#angles = np.linspace(1, -1, 22)  # Keeping angles range intact
xoffs = np.linspace(-0.5, 0.5, 100)  # More points in the -1 to 1 range
yoffs = np.linspace(-0.5, 0.5, 100)  # More points in the -1 to 1 range


# Dictionary to store discrete color values (RGB) for each angle
failure_data = defaultdict(lambda: np.zeros((len(xoffs), len(yoffs), 3)))  # RGB color grid
zero_counts = {}  # Dictionary to store zero-error counts per angle



# Collect data
for ai, angle in enumerate(angles):
    zero_counter = 0  # Track number of zero-error spots per angle
    
    extreme_green_values = []

    for xi, xoff in enumerate(xoffs):
        for yi, yoff in enumerate(yoffs):
            
            S1, S2, S3, S4, S5, S6 = test.Main(xoff, yoff, angle)
            if S1 == 'Red' or S2 == 'Red' or S3 == 'Red' or S4 == 'Red' or S5 == 'Red' or S6 == 'Red':
                redcorners = 1;
            else:
                redcorners = 0; 
            
            if S1 == 'Yellow' or S2 == 'Yellow' or S3 == 'Yellow' or S4 == 'Yellow' or S5 == 'Yellow' or S6 == 'Yellow':
                yellowcorners = 1;
            else:
                yellowcorners = 0;

            if redcorners > 0:  # Full failures
                failure_data[angle][xi, yi] = [1, 0, 0]  # Red
            elif yellowcorners > 0:  # Near failures
                failure_data[angle][xi, yi] = [1, 1, 0]  # Yellow
            else:  # Zero failure spots
                failure_data[angle][xi, yi] = [0, 1, 0]  # Green
                extreme_green_values.append((xoff, yoff))
                zero_counter += 1  # Count zero-error locations
    
    # Sort by x and y offset extremes
    extreme_green_values.sort(key=lambda v: (abs(v[0]), abs(v[1])), reverse=True)

    # Print the most extreme cases
    #print("Most extreme green values:")
    #for xoff, yoff in extreme_green_values[:5]:  # Print top 5 extreme cases
    #    print(f"X Offset: {xoff}, Y Offset: {yoff}")
    print("Finished With:", angle)
    
    zero_counts[angle] = zero_counter  # Store zero-count per angle






# Create subplots for each angle
fig, axes = plt.subplots(2, 5, figsize=(15, 6), constrained_layout=True)
axes = axes.flatten()

for i, angle in enumerate(angles):
    ax = axes[i]
    im = ax.imshow(failure_data[angle], origin="lower",
                   extent=[min(yoffs), max(yoffs), min(xoffs), max(xoffs)])
    
    # Add a marker at (0.50, -0.50)
    #ax.plot(-0.50, 0.50, 'ro', markersize=8)  # 'ro' = red circle


    ax.set_title(f"Angle {angle} (Zero Spots: {zero_counts[angle]})")
    ax.set_xlabel("Y Offset (mm)")
    ax.set_ylabel("X Offset (mm)")

plt.show()