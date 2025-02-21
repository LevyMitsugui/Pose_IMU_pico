import numpy as np
import pandas as pd

# Load IMU data from CSV
file_path = './pico_data_1.csv'
imu_data = pd.read_csv(file_path)

# Constants
alpha = 0.98  # Complementary filter constant

# Extract time in seconds
imu_data['time'] = imu_data['time_stamp'] / 1000.0  # Convert ms to seconds
dt = np.diff(imu_data['time'])  # Time step (s)

# Initial values for position, velocity, and orientation
position = np.zeros(3)  # [x, y, z]
velocity = np.zeros(3)  # [vx, vy, vz]
orientation = np.zeros(3)  # [roll, pitch, yaw]

# Function to apply complementary filter for orientation
def complementary_filter(accel_data, gyro_data, orientation, dt, alpha):
    # Roll and pitch estimation from accelerometer
    accel_pitch = np.arctan2(accel_data[1], np.sqrt(accel_data[0]**2 + accel_data[2]**2))
    accel_roll = np.arctan2(-accel_data[0], accel_data[2])
    
    # Gyro integration for roll and pitch
    orientation[0] = alpha * (orientation[0] + gyro_data[0] * dt) + (1 - alpha) * accel_roll
    orientation[1] = alpha * (orientation[1] + gyro_data[1] * dt) + (1 - alpha) * accel_pitch
    
    # Yaw estimation (only from gyro)
    orientation[2] += gyro_data[2] * dt
    
    return orientation

# Function to estimate velocity and position from accelerometer
def update_position(accel_data, velocity, position, dt):
    roll, pitch, yaw = orientation
    
    # Convert orientation to rotation matrix
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    
    # Rotation matrix from local to global frame
    R = Rz @ Ry @ Rx
    
    # Convert local acceleration to global frame
    global_accel = R @ accel_data
    
    # Update velocity (v = v0 + at)
    velocity += global_accel * dt
    
    # Update position (x = x0 + vt)
    position += velocity * dt
    
    return velocity, position


results = []
# Loop through the IMU data
for i in range(len(dt)):
    accel_data = imu_data.loc[i, ['accelX', 'accelY', 'accelZ']].values
    gyro_data = imu_data.loc[i, ['gyroX', 'gyroY', 'gyroZ']].values
    current_dt = dt[i]
    
    # Estimate orientation using complementary filter
    orientation = complementary_filter(accel_data, gyro_data, orientation, current_dt, alpha)
    
    # Update velocity and position based on accelerometer data
    velocity, position = update_position(accel_data, velocity, position, current_dt)
    
    # Print the results for each time step
    print(f"Time: {imu_data['time'][i]:.2f}s | Position: {position} | Orientation (rpy): {np.degrees(orientation)}")
    results.append([imu_data['time'][i], *position, *np.degrees(orientation)])

output_file_path = '../output/imu_results.csv'
columns = ['time', 'pos_x', 'pos_y', 'pos_z', 'roll', 'pitch', 'yaw']
results_df = pd.DataFrame(results, columns=columns)
results_df.to_csv(output_file_path, index=False)