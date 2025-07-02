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
                sxoff = float(s_xoff_str)/1000
                syoff = float(s_yoff_str)/1000
                sangle = float(s_angle_str)
                hxoff = float(h_xoff_str)/1000
                hyoff = float(h_yoff_str)/1000
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

# 📊 Statistics Section
results = process_file("input.txt")

# === Module-Level Red Statistics ===
sensor_red_modules = sum(1 for r in results if r['Red Sensor'] > 0)
hexaboard_red_modules = sum(1 for r in results if r['Red Hexaboards'] > 0)

num_readings = len(results)

sensor_red_pct = (sensor_red_modules / num_readings) * 100 if num_readings else 0
hexaboard_red_pct = (hexaboard_red_modules / num_readings) * 100 if num_readings else 0
module_red_ratio = (sensor_red_modules / hexaboard_red_modules) if hexaboard_red_modules else float('inf')

# === Additional Module-Level Stats ===
total_modules = len(results)

# Modules with no red at all
modules_with_no_red = sum(
    1 for r in results if r['Red Sensor'] == 0 and r['Red Hexaboards'] == 0
)
no_red_pct = (modules_with_no_red / total_modules) * 100 if total_modules else 0


print("\n📦 MODULE-LEVEL RED STATISTICS:")
print(f"Sensor modules with ≥1 Red corner: {sensor_red_modules}")
print(f"Hexaboard modules with ≥1 Red corner: {hexaboard_red_modules}")
print(f"Red Sensor Module %: {sensor_red_pct:.2f}%")
print(f"Red Hexaboard Module %: {hexaboard_red_pct:.2f}%")
print(f"Sensor-to-Hexaboard Red Module Ratio: {module_red_ratio:.2f}")

print("\n📋 OVERALL MODULE SUMMARY:")

print(f"Modules with NO red (sensor & hexaboard): {modules_with_no_red}")
print(f"Percentage of modules with no red: {no_red_pct:.2f}%")
print(f"Total modules processed: {total_modules}")

# Example usage
#results = process_file("input.txt")
#print(results)