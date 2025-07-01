import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import offsets as test  # Your hex failure classifier

# Define original data ranges
angles = [0.7, 0.5, 0.35, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.00781, 0]
xoffs = np.linspace(-0.5, 0.5, 10)
yoffs = np.linspace(-0.5, 0.5, 10)

nx, ny, nz = len(xoffs), len(yoffs), len(angles)
grid = np.zeros((nx, ny, nz, 4))  # RGBA

# Classify all voxel data
for ai, angle in enumerate(angles):
    for xi, xoff in enumerate(xoffs):
        for yi, yoff in enumerate(yoffs):
            S = test.Main(xoff, yoff, angle)
            # Update RGBA transparency levels
            if 'Red' in S:
                rgba = (1, 0, 0, 0.05)    # faint red
            elif 'Yellow' in S:
                rgba = (1, 1, 0, 0.25)    # medium yellow
            else:
                rgba = (0, 1, 0, 0.6)     # bold green

            grid[xi, yi, ai] = rgba

# Create boolean mask for filled voxels
filled = grid[:, :, :, 3] > 0

# Optional: soften outer shell for interior visibility
for xi in range(nx):
    for yi in range(ny):
        for ai in range(nz):
            is_edge = xi in (0, nx-1) or yi in (0, ny-1) or ai in (0, nz-1)
            if filled[xi, yi, ai] and is_edge:
                grid[xi, yi, ai, 3] = 0.15  # faint shell transparency

# Build plot
fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([nx, ny, nz])

ax.voxels(filled, facecolors=grid, edgecolor='k')

# Label axes with real values
x_ticks = np.linspace(0, nx-1, 5)
y_ticks = np.linspace(0, ny-1, 5)
z_ticks = np.linspace(0, nz-1, len(angles))

ax.set_xticks(x_ticks)
ax.set_xticklabels([f"{xoffs[int(i)]:.2f}" for i in x_ticks])
ax.set_yticks(y_ticks)
ax.set_yticklabels([f"{yoffs[int(i)]:.2f}" for i in y_ticks])
ax.set_zticks(z_ticks)
ax.set_zticklabels([f"{a:.4f}" for a in angles])

ax.set_xlabel("X Offset (mm)")
ax.set_ylabel("Y Offset (mm)")
ax.set_zlabel("Angle (deg)")
ax.set_title("3D Envelope Grid — Inner Cube Visibility")

plt.tight_layout()
plt.show()