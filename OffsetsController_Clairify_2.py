# -*- coding: utf-8 -*-
"""
Dual-Grading Visualization of Hexaboard Corner Classifications
@author: You
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Placeholder for dual grading systems — replace with actual modules
import offsets_RongShyeng_Sensor as test_old
import offsets_basic_sensor as test_new

# --- Define parameter sweeps ---
angles = [0.0, 0.00195, 0.0039, 0.0078125, 0.0156, 0.03125, 0.0625, 0.1250, 0.250, 0.5]
xoffs = np.linspace(-0.5, 0.5, 50)
yoffs = np.linspace(-0.5, 0.5, 50)

# --- Define color blending logic ---
def combine_colors(g1, g2):
    if g1 == 'Green' and g2 == 'Green':
        return [1, 1, 1]        # White
    elif g1 == 'Green' and g2 == 'Yellow':
        return [0, 1, 1]        # Turqoise
    elif g1 == 'Yellow' and g2 == 'Green':
        return [0, 1, 0]        # Green
    elif g1 == 'Yellow' and g2 == 'Yellow':
        return [1, 1, 0]        # Yellow
    elif 'Red' in [g1, g2] and 'Green' in [g1, g2]:
        return [1, 0.5, 0]        # Yellow (or tune this to your liking)
    elif 'Red' in [g1, g2] and 'Yellow' in [g1, g2]:
        return [1, 0.5, 0]      # Orange
    elif g1 == 'Red' and g2 == 'Red':
        return [1, 0, 0]        # Red
    else:
        return [0.5, 0.5, 0.5]  # Gray

# --- Initialize data containers ---
failure_data = defaultdict(lambda: np.zeros((len(xoffs), len(yoffs), 3)))
zero_counts = {}

# --- Data collection loop ---
for ai, angle in enumerate(angles):
    zero_counter = 0
    for xi, xoff in enumerate(xoffs):
        for yi, yoff in enumerate(yoffs):
            # Run both grading systems
            S_old = test_old.Main(xoff, yoff, angle)
            S_new = test_new.Main(xoff, yoff, angle)

            # Evaluate combined grading per corner
            color_flags = []
            for c1, c2 in zip(S_old, S_new):
                color_flags.append(combine_colors(c1, c2))

            # Final color: max severity among all corners (Red > Orange > Yellow > etc.)
            final_color = [0, 1, 0]  # Default: Green
            final_color = [0, 1, 0]  # Default: Green
            for cf in color_flags:
                if cf == [1, 0, 0]: final_color = cf; break    # Red
                elif cf == [1, 0.5, 0]: final_color = cf       # Orange
                elif cf == [1, 0.75, 1] and final_color == [1, 0.5, 0]: final_color = cf  #yellowish
                elif cf == [1, 1, 0] and final_color not in [[1, 0.5, 0]]: final_color = cf  # Yellow
                elif cf == [0, 1, 0] and final_color == [0, 1, 0]: continue  # Green stays unless upgraded
                elif cf == [0, 1, 1] and final_color == [0, 1, 0]: final_color = cf           # Turq
                elif cf == [1, 1, 1] and final_color == [0, 1, 1]: final_color = cf           # White

            failure_data[angle][xi, yi] = final_color
            if final_color == [1, 1, 1]: zero_counter += 1

    zero_counts[angle] = zero_counter
    print(f"Finished With: {angle}")

# --- Plot results ---
fig, axes = plt.subplots(2, 5, figsize=(15, 6), constrained_layout=True)
axes = axes.flatten()

for i, angle in enumerate(angles):
    ax = axes[i]
    im = ax.imshow(failure_data[angle], origin="lower",
                   extent=[min(yoffs), max(yoffs), min(xoffs), max(xoffs)])
    ax.set_title(f"Angle {angle:.4f} (White: {zero_counts[angle]})")
    ax.set_xlabel("Y Offset (mm)")
    ax.set_ylabel("X Offset (mm)")

plt.show()