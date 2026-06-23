# UCSB-HGCAL-Module-Edges

A geometrical and engineering study of HGCAL module edge placement, tiling, and mechanical grading.

By Paolo Jordano and Sussanne Kyre

## Overview

This repository contains a geometry-focused tolerance analysis for the HGCAL module and cassette assembly. It is designed to:

- compute vertex-level grading for hexagonal module parts,
- evaluate allowed offsets and rotational misalignments,
- compare new and old mechanical grading systems,
- generate visual and statistical outputs for engineering decision-making.

The work is centered on two main grading systems:

- `Grading_Code/offsets_HB.py`: the Hexaboard tolerance grading process,
- `Grading_Code/offsets_SR.py`: the Sensor tolerance grading process.

The remaining controller scripts in `Grading_Controllers/` use these grading routines to plot tolerance maps, process assembly data, and calculate yield statistics.

## Engineering Concept

The HGCAL modules are modeled as hexagonal elements with nominal dimensions and thermal/assembly tolerances.

### Geometry and grading

- Each module is represented by a hexagon whose vertices are computed from a central offset and a rotation angle.
- The code converts polar coordinates for the six hexagon corners into Cartesian coordinates.
- Each vertex is compared against a set of envelope boundaries:
  - `Purple`: best-fit region inside the most restrictive tolerance envelope,
  - `Yellow`: intermediate region inside a larger envelope,
  - `Green`: acceptable region between the yellow and red boundaries,
  - `Red`: failure region outside the allowed assembly envelope.

These color grades correspond to how far each vertex of a module sits from the nominal cassette placement and how much tolerance budget remains for assembly error.

### Nominal dimensions

The grading code uses measured assembly dimensions and tolerance values such as:

- Hexaboard nominal width and gap sizes,
- Cassette center-to-center spacing,
- Sensor nominal width and baseplate tolerance range,
- Envelope radii derived from the half-gap and hexagon circumcircle calculations.

This makes the project suitable as a geometric study of module edge clearance, tiling alignment, and tolerance stack-up.

## Repository Structure

- `Grading_Controllers/`
  - high-level controller scripts for plotting, data processing, and grading comparisons.
- `Grading_Controllers/Grading_Code/`
  - core tolerance grading functions for sensors and hexaboards.
- `input.txt`
  - sample input data used by the `On_Data` controllers.
- `coords_angle_0_*.csv`
  - coordinate files for specific angle or color cases (supporting plotting or validation).

## Key Files and What They Do

### `Grading_Controllers/Grading_Code/offsets_HB.py`

- Computes hexaboard vertex positions from offsets and angle.
- Uses hexagon geometry and cassette envelope calculations.
- Assigns vertex color grades based on whether each vertex lies within purple, yellow, green, or red envelopes.
- Returns a color grade for each of the six vertices.

### `Grading_Controllers/Grading_Code/offsets_SR.py`

- Computes sensor vertex positions and grading similarly to the hexaboard grading.
- Uses sensor circumcircle geometry and baseplate tolerance envelopes.
- Evaluates corner grade across the same color scheme, then returns six vertex grades.

### `Grading_Controllers/OffsetsController.py`

- Runs a parameter sweep over translational offsets and rotation angles.
- Generates a 2D grid showing whether each offset combination is green, yellow, or red.
- Produces plots of the allowed assembly region for different rotation angles.

### `Grading_Controllers/Offsets_On_Data.py`

- Reads `input.txt` with tab-separated assembly measurements.
- Converts recorded offsets from microns to millimeters.
- Evaluates both sensor and hexaboard grading for each data row.
- Prints summary statistics for modules with red or yellow corners.

### `Grading_Controllers/Offsets_On_Data_Yeild_Info.py`

- Similar to `Offsets_On_Data.py`, but designed to compare new and old grading systems.
- Reports how red/yellow outcomes change between versions.
- Helps quantify yield improvements from the new tolerance grading definitions.

### `Grading_Controllers/Offsets_On_Data_Color&Gradey.py`

- Reads the same assembly input data file.
- Generates counts of red and yellow corners for sensors and hexaboards.
- Supports color-based analysis for grading and failure mapping.

## Using the Code

### 1. Plot the tolerance space

Open and run `Grading_Controllers/OffsetsController.py`.

- It sweeps a dense grid of `x` and `y` offsets around the nominal position.
- It tests several rotation angles.
- The resulting plot shows the allowed region where no vertex enters the red failure zone.

### 2. Evaluate real assembly data

- Place your assembly readings into `input.txt`.
- Each line should provide:
  - sensor X offset, sensor Y offset, sensor angle,
  - hexaboard X offset, hexaboard Y offset, hexaboard angle.
- Values are read as floats and divided by `1000` inside the controllers, so keep units consistent with the existing input format.

Then run one of the `Offsets_On_Data` controllers:

- `Offsets_On_Data.py` for basic yield statistics,
- `Offsets_On_Data_Yeild_Info.py` for version comparison,
- `Offsets_On_Data_Color&Gradey.py` for color-count outputs.

### 3. Inspect the grading logic

- `Grading_Code/offsets_HB.py` and `offsets_SR.py` contain the core geometric grading logic.
- `Grading_Code/offsets_HB_old.py` and `offsets_SR_old.py` preserve previous grading behavior for comparison.

## Engineering Use

This repository is meant to support early-stage engineering evaluation of module tolerance budgets. It can be used to:

- visualize how sensor and hexaboard placement errors map to corner-level failure risks,
- compare old and new grading schemes,
- quantify the percentage of modules that remain within acceptable mechanical tolerances,
- guide design decisions for cassette tiling and assembly acceptance.

## Notes

- The grading colors are intentionally mapped to engineering risk levels: `Purple` and `Green` are acceptable, `Yellow` is marginal, and `Red` is unacceptable.
- The code emphasizes edge/corner tolerance rather than full 3D assembly simulation.
- This is a geometry-driven study of mechanical fit and module edge behavior.

