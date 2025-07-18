# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:09:43 2025

@author: Admin
"""

import numpy as np
from collections import Counter
import offsets as test
import offsets_basic_sensor as test2
import offsets_RongShyeng as test_b
import offsets_RongShyeng_Sensor as test2_b

def process_manual_data():
    Versions = ["new", "old"]

    # === Automatically generate input combinations ===

    angles = np.linspace(1, -1, 22)  # Covers a smoother gradient of angle offsets
    xoffs = np.linspace(-0.5, 0.5, 100)  # High-resolution offset grid
    yoffs = np.linspace(-0.5, 0.5, 100)

    for Version in Versions:
        color_counts_list = []

        for sangle in angles:
            for y in yoffs:
                for x in xoffs:
                    try:
                        sx = x / 1000
                        sy = y / 1000
                        hx = x / 1000
                        hy = y / 1000
                        hangle = sangle

                        if Version == "new":
                            sensor_colors = test2.Main(sx, sy, sangle)
                            hex_colors = test.Main(hx, hy, hangle)
                        else:
                            sensor_colors = test2_b.Main(sx, sy, sangle)
                            hex_colors = test_b.Main(hx, hy, hangle)

                        scount = Counter(sensor_colors)
                        hcount = Counter(hex_colors)

                        total = {
                            'Red Sensor': scount.get('Red', 0),
                            'Yellow Sensor': scount.get('Yellow', 0),
                            'Red Hexaboards': hcount.get('Red', 0),
                            'Yellow Hexaboards': hcount.get('Yellow', 0),
                        }

                        color_counts_list.append(total)

                    except Exception as e:
                        print(f"Error at angle {sangle:.5f}, x={x:.3f}, y={y:.3f}: {e}")


        # 📊 MODULE-LEVEL STATISTICS
        results = color_counts_list
        total_modules = len(results)

        sensor_red_modules = sum(1 for r in results if r['Red Sensor'] > 0)
        hexaboard_red_modules = sum(1 for r in results if r['Red Hexaboards'] > 0)
        yellow_sensor_modules = sum(1 for r in results if r['Yellow Sensor'] > 0)
        yellow_hexaboard_modules = sum(1 for r in results if r['Yellow Hexaboards'] > 0)

        modules_with_no_red_or_yellow = sum(
            1 for r in results if all(r[k] == 0 for k in ['Red Sensor', 'Red Hexaboards', 'Yellow Sensor', 'Yellow Hexaboards'])
        )
        modules_with_no_red = sum(
            1 for r in results if r['Red Sensor'] == 0 and r['Red Hexaboards'] == 0
        )
        modules_with_any_red = sum(
            1 for r in results if r['Red Sensor'] > 0 or r['Red Hexaboards'] > 0
        )

        # 📈 Percentages
        sensor_red_pct = (sensor_red_modules / total_modules) * 100 if total_modules else 0
        hexaboard_red_pct = (hexaboard_red_modules / total_modules) * 100 if total_modules else 0
        yellow_sensor_pct = (yellow_sensor_modules / total_modules) * 100 if total_modules else 0
        yellow_hexaboard_pct = (yellow_hexaboard_modules / total_modules) * 100 if total_modules else 0
        no_red_pct = (modules_with_no_red / total_modules) * 100 if total_modules else 0
        no_color_pct = (modules_with_no_red_or_yellow / total_modules) * 100 if total_modules else 0
        any_red_pct = (modules_with_any_red / total_modules) * 100 if total_modules else 0

        print(f"\n📦 MODULE-LEVEL STATISTICS [{Version.upper()} VERSION]:")
        print(f"Sensor modules with ≥1 Red corner: {sensor_red_modules}")
        print(f"Hexaboard modules with ≥1 Red corner: {hexaboard_red_modules}")
        print(f"Sensor modules with ≥1 Yellow corner: {yellow_sensor_modules}")
        print(f"Hexaboard modules with ≥1 Yellow corner: {yellow_hexaboard_modules}")
        print(f"Red Sensor Module %: {sensor_red_pct:.2f}%")
        print(f"Red Hexaboard Module %: {hexaboard_red_pct:.2f}%")
        print(f"Yellow Sensor Module %: {yellow_sensor_pct:.2f}%")
        print(f"Yellow Hexaboard Module %: {yellow_hexaboard_pct:.2f}%")
        print(f"\n📋 OVERALL MODULE SUMMARY:")
        print(f"Modules with NO red or yellow: {modules_with_no_red_or_yellow} ({no_color_pct:.2f}%)")
        print(f"Modules with NO red: {modules_with_no_red} ({no_red_pct:.2f}%)")
        print(f"Modules with ANY red: {modules_with_any_red} ({any_red_pct:.2f}%)")
        print(f"Total modules processed: {total_modules}")

process_manual_data()