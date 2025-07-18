# -*- coding: utf-8 -*-
"""
offsets_HB_old Hexaboard Grading Classification using old System
"""

import numpy as np
import math

# --- Constants and Nominals ---
WarmGap = 0.487
HalfGap = WarmGap / 2
w = 166.79
w_t = 0.850
w_naut = w_t + w
Env_Yellow = w_naut / 2
Env_Purple = Env_Yellow - HalfGap
Env_Red = Env_Yellow + HalfGap

r_p = Env_Purple
r_y = Env_Yellow
r_r = Env_Red
cr = Env_Purple / np.cos(0.523599)
R = 2 * cr
m = np.sqrt(3)

# --- Rule-Based Classification ---
def classify_by_rules(X, Y, Theta):
    if abs(X) <= 0.075 and abs(Y) <= 0.075 and abs(Theta) <= 0.04:
        return 'A'
    if (abs(X) > 0.12 and abs(Y) == 0.085) or \
       (abs(Y) > 0.12 and abs(X) == 0.085) or \
       (abs(Theta) > 0.04 and (abs(X) == 0.085 or abs(Y) == 0.085)) or \
       (abs(Theta) > 0.1):
        return 'C'
    return 'B'

# --- Main Function ---
def Main(Xoff, Yoff, ThetaOff):
    AngleOff = ThetaOff

    # Establishing polar coordinates (same for all vertices)
    angles = [120, 60, 0, 300, 240, 180]
    vertices = []

    for a in angles:
        rad = math.radians(a + AngleOff)
        x = cr * math.cos(rad) + Xoff
        y = cr * math.sin(rad) + Yoff
        vertices.append((x, y))

    # Apply classification to all 6 vertices
    vertex_colors = []
    for _ in vertices:
        classification = classify_by_rules(Xoff, Yoff, ThetaOff)
        if classification == 'A':
            vertex_colors.append('Green')
        elif classification == 'B':
            vertex_colors.append('Yellow')
        elif classification == 'C':
            vertex_colors.append('Red')
        else:
            vertex_colors.append('Unknown')

    #print(*vertex_colors)
    return tuple(vertex_colors)

# Example usage
#Main(-0.2, -0.1, 0.500)