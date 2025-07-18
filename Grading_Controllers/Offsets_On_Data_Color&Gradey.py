# -*- coding: utf-8 -*-
"""
Controller 'On Data' File:
    Compares Old and New Mechanincal Grading Systems. Outputs Statistics. 
@author: Paolo Jordano
"""
import numpy as np
from collections import Counter
import Grading_Code.offsets_HB as test
import Grading_Code.offsets_SR as test2 
import Grading_Code.offsets_HB_old as test_b
import Grading_Code.offsets_SR_old as test2_b

# Read tab-separated file
def process_file(filepath):
    
    Versions = ["new","old"]
    for Version in Versions:
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
                    if Version == "new":
                        S1, S2, S3, S4, S5, S6 = test2.Main(sxoff, syoff, sangle) #Sensor
                    elif Version == "old": 
                        S1, S2, S3, S4, S5, S6 = test2_b.Main(sxoff, syoff, sangle) #Sensor
                    colors = [S1, S2, S3, S4, S5, S6]

                    # Count colors
                    scount = Counter(colors)

                    # Get color results from function
                    if Version == "new":
                        S1, S2, S3, S4, S5, S6 = test.Main(hxoff, hyoff, hangle) #Hexaboard
                    elif Version == "old": 
                        S1, S2, S3, S4, S5, S6 = test_b.Main(hxoff, hyoff, hangle) #Hexaboard
                    colors = [S1, S2, S3, S4, S5, S6]

                    # Count colors
                    hcount = Counter(colors)

                    # Add purple if it's a possible outcome
                    total = {
                        'Red Sensor': scount.get('Red', 0),
                        'Red Hexaboards': hcount.get('Red', 0),
                        'Yellow Sensor': scount.get('Yellow', 0),
                        'Yellow Hexaboards': hcount.get('Yellow', 0),

                    }

                    color_counts_list.append(total)

                except Exception as e:
                    print(f"Error processing line: {line.strip()} → {e}")
                    continue

                

        # 📊 Statistics Section
        results = color_counts_list;

        # === Module-Level Red Statistics ===
        sensor_red_modules = sum(1 for r in results if r['Red Sensor'] > 0)
        hexaboard_red_modules = sum(1 for r in results if r['Red Hexaboards'] > 0)
        yellow_sensor_modules = sum(1 for r in results if r['Yellow Sensor'] > 0)
        yellow_hexaboard_modules = sum(1 for r in results if r['Yellow Hexaboards'] > 0)

        num_readings = len(results)

        yellow_sensor_pct = (yellow_sensor_modules / num_readings) * 100 if num_readings else 0
        yellow_hexaboard_pct = (yellow_hexaboard_modules / num_readings) * 100 if num_readings else 0


        sensor_red_pct = (sensor_red_modules / num_readings) * 100 if num_readings else 0
        hexaboard_red_pct = (hexaboard_red_modules / num_readings) * 100 if num_readings else 0
        module_red_ratio = (sensor_red_modules / hexaboard_red_modules) if hexaboard_red_modules else float('inf')



        # === Additional Module-Level Stats ===
        total_modules = len(results)

        modules_with_no_red_or_yellow = sum(
            1 for r in results if all(
                r[k] == 0 for k in ['Red Sensor', 'Red Hexaboards', 'Yellow Sensor', 'Yellow Hexaboards']
                    )
        )
        no_color_pct = (modules_with_no_red_or_yellow / total_modules) * 100 if total_modules else 0

        # Modules with no red at all 
        modules_with_no_red = sum( 
            1 for r in results if r['Red Sensor'] == 0 and r['Red Hexaboards'] == 0 
        )   

        modules_with_any_yellow = sum(
            1 for r in results if r['Yellow Sensor'] > 0 or r['Yellow Hexaboards'] > 0
        )

        sensor_red_modules = sum(1 for r in results if r['Red Sensor'] > 0)
        hexaboard_red_modules = sum(1 for r in results if r['Red Hexaboards'] > 0)

        yellow_module_pct = (modules_with_any_yellow / total_modules) * 100 if total_modules else 0

        no_red_pct = (modules_with_no_red / total_modules) * 100 if total_modules else 0

        modules_with_any_red = sum(
            1 for r in results if r['Red Sensor'] > 0 or r['Red Hexaboards'] > 0
        )
        any_red_pct = (modules_with_any_red / total_modules) * 100 if total_modules else 0

        print(f"\n📦 MODULE-LEVEL STATISTICS [{Version.upper()} VERSION]:")
        print(f"Sensor modules with ≥1 Red corner: {sensor_red_modules}")
        print(f"Sensor modules with ≥1 Yellow corner: {yellow_sensor_modules}")
        print(f"Hexaboard modules with ≥1 Red corner: {hexaboard_red_modules}")
        print(f"Hexaboard modules with ≥1 Yellow corner: {yellow_hexaboard_modules}")
        print(f"Red Sensor Module %: {sensor_red_pct:.2f}%")
        print(f"Yellow Sensor Module %: {yellow_sensor_pct:.2f}%")
        print(f"Red Hexaboard Module %: {hexaboard_red_pct:.2f}%")
        print(f"Yellow Hexaboard Module %: {yellow_hexaboard_pct:.2f}%")

        print(f"\n📋 OVERALL MODULE SUMMARY:")
        print(f"Modules with NO red or yellow (sensor & hexaboard): {modules_with_no_red_or_yellow}")
        print(f"Percentage of modules with no red or yellow: {no_color_pct:.2f}%")
        print(f"Percentage of modules with no red: {no_red_pct:.2f}%")
        print(f"Total modules processed: {total_modules}")
        print(f"Modules with any Yellow (sensor or hexaboard): {modules_with_any_yellow}")
        print(f"Percentage of modules with any yellow: {yellow_module_pct:.2f}%")
        print(f"Modules with any Red (sensor or hexaboard): {modules_with_any_red}")
        print(f"Percentage of modules with any red: {any_red_pct:.2f}%")

        print(f"{Version} {sensor_red_modules} {sensor_red_pct:.2f} {yellow_sensor_modules} {yellow_sensor_pct:.2f} {hexaboard_red_modules} {hexaboard_red_pct:.2f} {yellow_hexaboard_modules} {yellow_hexaboard_pct:.2f} {modules_with_no_red_or_yellow} {no_color_pct:.2f} {total_modules}")
        
        
    return color_counts_list

#Example usage
results = process_file("input.txt")

#print(results)