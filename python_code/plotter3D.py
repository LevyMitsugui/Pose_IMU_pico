import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Load the CSV file with results
results_path = '../output/imu_results.csv'
data = pd.read_csv(results_path)

# Set up the figure and 3D axes for animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize plot elements
line, = ax.plot([], [], [], 'b-', lw=2)
point, = ax.plot([], [], [], 'ro')
quiver = None

# Set the plot limits based on data
ax.set_xlim(min(data['pos_x']), max(data['pos_x']))
ax.set_ylim(min(data['pos_y']), max(data['pos_y']))
ax.set_zlim(min(data['pos_z']), max(data['pos_z']))

# Function to update arrows (frame of reference) using roll, pitch, and yaw
def update_arrows(roll, pitch, yaw, pos_x, pos_y, pos_z):
    # Define local axis vectors for the IMU
    imu_axes = np.identity(3)  # Local x, y, z axes (should be orthogonal)

    # Rotation matrices for roll, pitch, and yaw
    # Yaw (around z-axis)
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    # Pitch (around y-axis)
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    # Roll (around x-axis)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    
    # Apply rotations: roll -> pitch -> yaw (order matters)
    rotation_matrix = Rz @ Ry @ Rx
    rotated_axes = rotation_matrix @ imu_axes

    # Increase the length of the arrows
    arrow_length = 40.0  # Adjust this value as needed

    # Create quivers to represent the arrows (x: red, y: green, z: blue)
    quivers = []
    colors = ['r', 'g', 'b']  # Colors for the IMU's x, y, z axes
    for i in range(3):
        quivers.append(ax.quiver(pos_x, pos_y, pos_z,
                                 rotated_axes[0, i], rotated_axes[1, i], rotated_axes[2, i],
                                 color=colors[i], length=arrow_length, normalize=True))

    return quivers

# Update function for animation
def update(num):
    global quiver  # Make the quiver global so we can clear previous arrows

    # Clear previous quivers if they exist
    if quiver:
        for q in quiver:
            q.remove()

    # Update the line (robot trajectory)
    line.set_data(data['pos_x'][:num], data['pos_y'][:num])
    line.set_3d_properties(data['pos_z'][:num])

    # Update the point (current position)
    point.set_data([data['pos_x'][num]], [data['pos_y'][num]])  # Needs to be a sequence
    point.set_3d_properties([data['pos_z'][num]])  # Also as a sequence

    # Get roll, pitch, and yaw values
    roll = np.radians(data['roll'][num])
    pitch = np.radians(data['pitch'][num])
    yaw = np.radians(data['yaw'][num])

    # Update quivers for the IMU orientation
    quiver = update_arrows(roll, pitch, yaw, data['pos_x'][num], data['pos_y'][num], data['pos_z'][num])

    return line, point, *quiver

# Create animation
ani = FuncAnimation(fig, update, frames=len(data), interval=50)

# Show the plot
plt.show()
