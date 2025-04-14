import serial
import threading
import time
from collections import deque
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import csv

# === CONFIG ===
SERIAL_PORT = 'COM8'  # Change as needed
BAUD_RATE = 115200
SAMPLE_RATE_HZ = 100
ROLLING_WINDOW_SECONDS = 5
MAX_DEQUE_LEN = SAMPLE_RATE_HZ * ROLLING_WINDOW_SECONDS
PRINT_INTERVAL_MS = 50  # Match plot update rate

# === Serial Setup ===
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# === Full history lists (for logging) ===
full_time = []
full_gyroX, full_gyroY, full_gyroZ = [], [], []
full_accelX, full_accelY, full_accelZ = [], [], []

# === Deques for plotting (fixed size) ===
plot_time = deque(maxlen=MAX_DEQUE_LEN)
plot_gyroX = deque(maxlen=MAX_DEQUE_LEN)
plot_gyroY = deque(maxlen=MAX_DEQUE_LEN)
plot_gyroZ = deque(maxlen=MAX_DEQUE_LEN)
plot_accelX = deque(maxlen=MAX_DEQUE_LEN)
plot_accelY = deque(maxlen=MAX_DEQUE_LEN)
plot_accelZ = deque(maxlen=MAX_DEQUE_LEN)

# === Most recent value for printing ===
latest_sample = None

# === Threading ===
def serial_reader():
    global latest_sample
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            data = line.split("\t")
            if len(data) != 7:
                continue  # skip malformed lines

            t = float(data[0])
            gx, gy, gz = float(data[1]), float(data[2]), float(data[3])
            ax, ay, az = float(data[4]), float(data[5]), float(data[6])

            # Save to full history
            full_time.append(t)
            full_gyroX.append(gx)
            full_gyroY.append(gy)
            full_gyroZ.append(gz)
            full_accelX.append(ax)
            full_accelY.append(ay)
            full_accelZ.append(az)

            # Add to plot window (adjust time to be relative to latest sample)
            if full_time:
                t0 = full_time[-1] - ROLLING_WINDOW_SECONDS
                if t >= t0:
                    plot_time.append(t)
                    plot_gyroX.append(gx)
                    plot_gyroY.append(gy)
                    plot_gyroZ.append(gz)
                    plot_accelX.append(ax)
                    plot_accelY.append(ay)
                    plot_accelZ.append(az)

            # Update latest sample for printing
            latest_sample = (t, gx, gy, gz, ax, ay, az)

        except Exception as e:
            print(f"Error reading serial: {e}")

# Start serial reading thread
thread = threading.Thread(target=serial_reader, daemon=True)
thread.start()

# === PyQtGraph Setup ===
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Real-Time IMU Data")
win.resize(1000, 600)
win.show()

plot = win.addPlot(title="Gyroscope and Accelerometer")
plot.addLegend()
plot.setLabel('left', 'Value')
plot.setLabel('bottom', 'Time (s)')

curve_gx = plot.plot(pen='r', name='Gyro X')
curve_gy = plot.plot(pen='g', name='Gyro Y')
curve_gz = plot.plot(pen='b', name='Gyro Z')
curve_ax = plot.plot(pen='m', name='Accel X')
curve_ay = plot.plot(pen='y', name='Accel Y')
curve_az = plot.plot(pen='c', name='Accel Z')

def update():
    if not plot_time:
        return

    t0 = plot_time[-1] - ROLLING_WINDOW_SECONDS
    times = [t for t in plot_time if t >= t0]
    idx_start = len(plot_time) - len(times)
    curve_gx.setData(times, list(plot_gyroX)[idx_start:])
    curve_gy.setData(times, list(plot_gyroY)[idx_start:])
    curve_gz.setData(times, list(plot_gyroZ)[idx_start:])
    curve_ax.setData(times, list(plot_accelX)[idx_start:])
    curve_ay.setData(times, list(plot_accelY)[idx_start:])
    curve_az.setData(times, list(plot_accelZ)[idx_start:])

    # Print latest sample
    if latest_sample:
        print(f"t={latest_sample[0]:.2f}, gx={latest_sample[1]:.2f}, gy={latest_sample[2]:.2f}, gz={latest_sample[3]:.2f}, "
              f"ax={latest_sample[4]:.2f}, ay={latest_sample[5]:.2f}, az={latest_sample[6]:.2f}")

# Update plot and print every 50 ms (20 FPS)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(PRINT_INTERVAL_MS)

# === Save on close ===
def save_data():
    try:
        with open('pico_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['time', 'gyroX', 'gyroY', 'gyroZ', 'accelX', 'accelY', 'accelZ'])
            for row in zip(full_time, full_gyroX, full_gyroY, full_gyroZ, full_accelX, full_accelY, full_accelZ):
                writer.writerow(row)
        print("Data saved to pico_data.csv")
    except Exception as e:
        print(f"Error saving CSV: {e}")

# Connect save to close event
def on_close():
    save_data()
    app.quit()

# Hook close event
def handle_close():
    on_close()

win.closeEvent = lambda ev: (handle_close(), ev.accept())

# Run Qt app
app.exec_()
