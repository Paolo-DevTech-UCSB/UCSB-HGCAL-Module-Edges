# -*- coding: utf-8 -*-
"""
Controller File:
    Plots 3D Tolerance space of a given grading system, In 2D Slices of Angle Offsets.
@author: Paolo Jordano
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import Grading_Code.offsets_SR as test

# Define parameter ranges
angles = [0.00195, 0.0025073, 0.0032226, 0.0041414, 0.0053234, 0.0068463, 0.0088086, 0.011333, 0.014574, 0.018719, 0.024002, 0.030719, 0.039239, 0.05002, 0.063519, 0.080304, 0.10107, 0.1272, 0.16017, 0.2, 0.24, 0.3, 0.35, 0.4, 0.45, 0.5]
xoffs = np.linspace(-1.0, 1.0, 300)  # wider range, finer steps
yoffs = np.linspace(-1.0, 1.0, 300)

# Dictionary to store discrete color values (RGB) for each angle
failure_data = defaultdict(lambda: np.zeros((len(xoffs), len(yoffs), 3)))
zero_counts = {}

# Helper to initialize extreme trackers for a color
def make_extreme_tracker():
    return {
        'max_x': None, 'max_x_pt': None,
        'min_x': None, 'min_x_pt': None,
        'max_y': None, 'max_y_pt': None,
        'min_y': None, 'min_y_pt': None,
        'max_abs_x': None, 'max_abs_x_pt': None,
        'max_abs_y': None, 'max_abs_y_pt': None,
        'count': 0
    }

# Store per-angle extremes and global extremes
angle_extremes = {}
global_extremes = {'Red': make_extreme_tracker(),
                   'Yellow': make_extreme_tracker(),
                   'Green': make_extreme_tracker()}

for ai, angle in enumerate(angles):
    zero_counter = 0
    # Track extremes per color for this angle
    extremes = {'Red': make_extreme_tracker(),
                'Yellow': make_extreme_tracker(),
                'Green': make_extreme_tracker()}

    for xi, xoff in enumerate(xoffs):
        for yi, yoff in enumerate(yoffs):
            S1, S2, S3, S4, S5, S6 = test.Main(xoff, yoff, angle)

            # determine color
            if S1 == 'Red' or S2 == 'Red' or S3 == 'Red' or S4 == 'Red' or S5 == 'Red' or S6 == 'Red':
                color = 'Red'
                failure_data[angle][xi, yi] = [1, 0, 0]
            elif S1 == 'Yellow' or S2 == 'Yellow' or S3 == 'Yellow' or S4 == 'Yellow' or S5 == 'Yellow' or S6 == 'Yellow':
                color = 'Yellow'
                failure_data[angle][xi, yi] = [1, 1, 0]
            else:
                color = 'Green'
                failure_data[angle][xi, yi] = [0, 1, 0]
                zero_counter += 1

            # update extremes for this color (angle-level)
            t = extremes[color]
            t['count'] += 1

            # max x
            if t['max_x'] is None or xoff > t['max_x']:
                t['max_x'] = xoff
                t['max_x_pt'] = (xoff, yoff)
            # min x
            if t['min_x'] is None or xoff < t['min_x']:
                t['min_x'] = xoff
                t['min_x_pt'] = (xoff, yoff)
            # max y
            if t['max_y'] is None or yoff > t['max_y']:
                t['max_y'] = yoff
                t['max_y_pt'] = (xoff, yoff)
            # min y
            if t['min_y'] is None or yoff < t['min_y']:
                t['min_y'] = yoff
                t['min_y_pt'] = (xoff, yoff)
            # max abs x
            if t['max_abs_x'] is None or abs(xoff) > t['max_abs_x']:
                t['max_abs_x'] = abs(xoff)
                t['max_abs_x_pt'] = (xoff, yoff)
            # max abs y
            if t['max_abs_y'] is None or abs(yoff) > t['max_abs_y']:
                t['max_abs_y'] = abs(yoff)
                t['max_abs_y_pt'] = (xoff, yoff)

            # update global extremes as well
            g = global_extremes[color]
            # max x
            if g['max_x'] is None or xoff > g['max_x']:
                g['max_x'] = xoff
                g['max_x_pt'] = (xoff, yoff, angle)
            # min x
            if g['min_x'] is None or xoff < g['min_x']:
                g['min_x'] = xoff
                g['min_x_pt'] = (xoff, yoff, angle)
            # max y
            if g['max_y'] is None or yoff > g['max_y']:
                g['max_y'] = yoff
                g['max_y_pt'] = (xoff, yoff, angle)
            # min y
            if g['min_y'] is None or yoff < g['min_y']:
                g['min_y'] = yoff
                g['min_y_pt'] = (xoff, yoff, angle)
            # max abs x
            if g['max_abs_x'] is None or abs(xoff) > g['max_abs_x']:
                g['max_abs_x'] = abs(xoff)
                g['max_abs_x_pt'] = (xoff, yoff, angle)
            # max abs y
            if g['max_abs_y'] is None or abs(yoff) > g['max_abs_y']:
                g['max_abs_y'] = abs(yoff)
                g['max_abs_y_pt'] = (xoff, yoff, angle)

    angle_extremes[angle] = extremes
    zero_counts[angle] = zero_counter
    print(f"Finished With: {angle}  (Zero Spots: {zero_counter})")

# Store area values per color per angle
area_stats = {}
dx = xoffs[1] - xoffs[0]
dy = yoffs[1] - yoffs[0]
cell_area = dx * dy

for angle in angles:
    red_area = 0
    yellow_area = 0
    green_area = 0

    grid = failure_data[angle]
    for xi in range(len(xoffs)):
        for yi in range(len(yoffs)):
            r, g, b = grid[xi, yi]
            if r == 1 and g == 0 and b == 0:
                red_area += cell_area
            elif r == 1 and g == 1 and b == 0:
                yellow_area += cell_area
            elif r == 0 and g == 1 and b == 0:
                green_area += cell_area

    area_stats[angle] = {
        'Red': red_area,
        'Yellow': yellow_area,
        'Green': green_area
    }

# Sum of color areas across all angles
total_color_areas = {'Red': 0, 'Yellow': 0, 'Green': 0}
for stats in area_stats.values():
    for color in total_color_areas:
        total_color_areas[color] += stats[color]

total_all = sum(total_color_areas.values())
print("\nTotal Area by Color Across All Angles:")
for color in ['Red', 'Yellow', 'Green']:
    pct = (total_color_areas[color] / total_all) * 100 if total_all != 0 else 0.0
    #print(f"{color}: {total_color_areas[color]:.6f} units ({pct:.2f}%)")

# Print per-angle extremes (top-level summary)
"""print("\nPer-angle extreme points (showing max/min X and Y for each color):")
for angle in angles:
    print(f"\nAngle {angle}:")
    for color in ['Red', 'Yellow', 'Green']:
        t = angle_extremes[angle][color]
        print(f"  {color} - count: {t['count']}")
        print(f"    max_x: {t['max_x']} at {t['max_x_pt']}")
        print(f"    min_x: {t['min_x']} at {t['min_x_pt']}")
        print(f"    max_y: {t['max_y']} at {t['max_y_pt']}")
        print(f"    min_y: {t['min_y']} at {t['min_y_pt']}")
        print(f"    max_abs_x: {t['max_abs_x']} at {t['max_abs_x_pt']}")
        print(f"    max_abs_y: {t['max_abs_y']} at {t['max_abs_y_pt']}")"""

print("Angle,Y_max_x,Y_max_y,Y_min_x,Y_min_y,G_max_x,G_max_y,G_min_x,G_min_y")

def fmt(val):
    return f"{float(val):.6f}" if isinstance(val, (float, int, np.float64)) else str(val)

for angle in angles:
    y_data = angle_extremes[angle]['Yellow']
    g_data = angle_extremes[angle]['Green']

    def safe_coord(data, key):
        pt = data.get(key)
        return fmt(pt[0]) if pt else "" , fmt(pt[1]) if pt else ""

    y_max_x, y_max_y = safe_coord(y_data, 'max_x_pt')
    y_min_x, y_min_y = safe_coord(y_data, 'min_x_pt')
    g_max_x, g_max_y = safe_coord(g_data, 'max_x_pt')
    g_min_x, g_min_y = safe_coord(g_data, 'min_x_pt')

    print(f"{angle},{y_max_x},{y_max_y},{y_min_x},{y_min_y},{g_max_x},{g_max_y},{g_min_x},{g_min_y}")
     
# Create subplots for each angle
n_angles = len(angles)
cols = min(5, n_angles)
rows = int(np.ceil(n_angles / cols))
fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows), constrained_layout=True)
if n_angles == 1:
    axes = np.array([axes])
axes = axes.flatten()

for i, angle in enumerate(angles):
    ax = axes[i]
    im = ax.imshow(failure_data[angle], origin="lower",
                   extent=[min(yoffs), max(yoffs), min(xoffs), max(xoffs)])
    ax.set_title(f"Angle {angle} (Zero Spots: {zero_counts[angle]})")
    ax.set_xlabel("Y Offset (mm)")
    ax.set_ylabel("X Offset (mm)")

# hide any unused axes
for j in range(len(angles), len(axes)):
    axes[j].axis('off')

plt.show()