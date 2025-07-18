import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import offsets_SR_old as test

# Parameter space (centers)
angles = np.array([0.0, 0.00195, 0.0039, 0.0078125, 0.0156, 0.03125, 0.0625, 0.1250, 0.250, 0.5])
xoffs = np.linspace(-1, 1, 100)
yoffs = np.linspace(-1, 1, 100)

# Generate edges from centers for voxel dimensions (+1 point each)
angle_edges = np.linspace(angles[0], angles[-1], len(angles) + 1)
x_edges = np.linspace(xoffs[0], xoffs[-1], len(xoffs) + 1)
y_edges = np.linspace(yoffs[0], yoffs[-1], len(yoffs) + 1)

# Meshgrid for voxel edges
X, Y, Z = np.meshgrid(y_edges, x_edges, angle_edges, indexing='ij')  # Shape: (101, 101, 11)

# Create voxel data structures
filled = np.zeros((len(angles), len(xoffs), len(yoffs)), dtype=bool)
colors = np.zeros((len(angles), len(xoffs), len(yoffs), 4))  # RGBA

# Populate voxel data, excluding 'Red' states
for ai, angle in enumerate(angles):
    for xi, xoff in enumerate(xoffs):
        for yi, yoff in enumerate(yoffs):
            S1, S2, S3, S4, S5, S6 = test.Main(xoff, yoff, angle)
            state_list = [S1, S2, S3, S4, S5, S6]

            # Skip voxels with 'Red' state
            if 'Red' in state_list:
                continue

            # Assign color based on state
            if 'Yellow' in state_list:
                col = [1, 1, 0, 0.6]  # Yellow, semi-transparent
            else:
                col = [0, 1, 0, 1.0]  # Green, opaque

            colors[ai, xi, yi] = col
            filled[ai, xi, yi] = True


# Create plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot voxels (transposing to match x/y/z axes)
ax.voxels(X, Y, Z, filled.transpose(2,1,0), facecolors=colors.transpose(2,1,0,3), edgecolor='k')

ax.set_xlabel('Y Index')
ax.set_ylabel('X Index')
ax.set_zlabel('Angle Index')
ax.set_box_aspect([
    len(yoffs),     # Y axis length
    len(xoffs),     # X axis length
    len(angles)     # Z axis length
])
# Calculate voxel centers from edges
angle_centers = 0.5 * (angle_edges[:-1] + angle_edges[1:])

# Set Z ticks at these centers
ax.set_zticks(angle_centers)
ax.set_zticklabels([f"{a:.4f}" for a in angles])

plt.title('3D Voxel Map of Failure States')
plt.show()