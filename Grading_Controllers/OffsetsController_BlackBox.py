# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:09:43 2025

@author: Admin
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.patches import Rectangle
import Grading_Code.offsets_SR as test

angles = [0.0, 0.002, 0.008, 0.016, 0.032, 0.04, 0.064, 0.1, 0.2, 0.5]
xoffs = np.linspace(-0.5, 0.5, 100)
yoffs = np.linspace(-0.5, 0.5, 100)

failure_data = defaultdict(lambda: np.zeros((len(xoffs), len(yoffs), 3)))
zero_counts = {}

for ai, angle in enumerate(angles):
    zero_counter = 0
    extreme_green_values = []

    for xi, xoff in enumerate(xoffs):
        for yi, yoff in enumerate(yoffs):
            S1, S2, S3, S4, S5, S6 = test.Main(xoff, yoff, angle)
            redcorners = int(any(s == 'Red' for s in [S1, S2, S3, S4, S5, S6]))
            yellowcorners = int(any(s == 'Yellow' for s in [S1, S2, S3, S4, S5, S6]))

            if redcorners:
                failure_data[angle][xi, yi] = [1, 0, 0]
            elif yellowcorners:
                failure_data[angle][xi, yi] = [1, 1, 0]
            else:
                failure_data[angle][xi, yi] = [0, 1, 0]
                extreme_green_values.append((xoff, yoff))
                zero_counter += 1

    extreme_green_values.sort(key=lambda v: (abs(v[0]), abs(v[1])), reverse=True)
    print("Finished With:", angle)
    zero_counts[angle] = zero_counter

fig, axes = plt.subplots(2, 5, figsize=(15, 6), constrained_layout=True)
axes = axes.flatten()

for i, angle in enumerate(angles):
    ax = axes[i]
    im = ax.imshow(failure_data[angle], origin="lower",
                   extent=[min(yoffs), max(yoffs), min(xoffs), max(xoffs)])

    # Add black box only for angles ≤ 0.04
    if angle <= 0.04:
        box = Rectangle(
            (-0.04, -0.04),
            0.08,
            0.08,
            linewidth=1,
            edgecolor='black',
            facecolor='none'
        )
        ax.add_patch(box)

    ax.set_title(f"Angle {angle} (Zero Spots: {zero_counts[angle]})")
    ax.set_xlabel("Y Offset (mm)")
    ax.set_ylabel("X Offset (mm)")

plt.show()