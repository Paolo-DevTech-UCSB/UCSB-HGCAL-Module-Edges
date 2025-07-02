# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:09:43 2025

@author: Admin
"""
import numpy as np
from collections import Counter
import offsets as test
import offsets_basic_sensor as test2 

# Read tab-separated file
def process_file(filepath):
    color_counts_list = []

    with open(filepath, 'r') as file:
        for line in file:
            try:
                # Parse tab-separated values
                s_xoff_str, s_yoff_str, s_angle_str, h_xoff_str, h_yoff_str, h_angle_str  = line.strip().split()
                sxoff = float(s_xoff_str)
                syoff = float(s_yoff_str)
                sangle = float(s_angle_str)
                hxoff = float(h_xoff_str)
                hyoff = float(h_yoff_str)
                hangle = float(h_angle_str)

                # Get color results from function
                S1, S2, S3, S4, S5, S6 = test2.Main(sxoff, syoff, sangle)
                colors = [S1, S2, S3, S4, S5, S6]

                # Count colors
                scount = Counter(colors)

                # Get color results from function
                S1, S2, S3, S4, S5, S6 = test.Main(hxoff, hyoff, hangle)
                colors = [S1, S2, S3, S4, S5, S6]

                # Count colors
                hcount = Counter(colors)

                # Add purple if it's a possible outcome
                total = {
                    'Red Sensor': scount.get('Red', 0),
                    'Red Hexaboards': hcount.get('Red', 0),
                }

                color_counts_list.append(total)

            except Exception as e:
                print(f"Error processing line: {line.strip()} → {e}")
                continue

    return color_counts_list

# Example usage
results = process_file("input.txt")
print(results)