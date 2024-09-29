#Credits to The Bored Robot @ Youtube (https://www.youtube.com/watch?v=PhDPnjF3_tA&list=PLDQbF7EgWNg9_Aem8LEkfW5HC1zEHC3BM&index=3&t=162s)

import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import csv

SampleRate = 200

SERIAL_PORT = "com6"
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

time_stamp = []
gyroX = []
gyroY = []
gyroZ = []
accelX = []
accelY = []
accelZ = []

def read_serial(ser):
    data = ser.readline().decode('utf-8').strip()
    data = data.split("\t")
    
    time_stamp.append(float(data[0]))
    gyroX.append(float(data[1]))
    gyroY.append(float(data[2]))
    gyroZ.append(float(data[3]))
    accelX.append(float(data[4]))
    accelY.append(float(data[5]))
    accelZ.append(float(data[6]))

    print(f'gyrox: {data[1]}, gyroy: {data[2]}, gyroz: {data[3]}, accelx: {data[4]}, accely: {data[5]}, accelz: {data[6]}')

def update_graph(frame):
    read_serial(ser)
    plt.cla()
    plt.plot(time_stamp, gyroX, label='gyroX')
    plt.plot(time_stamp, gyroY, label='gyroY')
    plt.plot(time_stamp, gyroZ, label='gyroZ')
    plt.plot(time_stamp, accelX, label='accelX')
    plt.plot(time_stamp, accelY, label='accelY')
    plt.plot(time_stamp, accelZ, label='accelZ')
    plt.xlabel('time (s)')
    plt.ylabel('acceleration (m/s^2) + gyro (deg/s)')
    plt.legend(loc='upper left')
    #plt.tight_layout()
    plt.legend()

def on_close(event):
    with open('pico_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['time_stamp', 'gyroX', 'gyroY', 'gyroZ', 'accelX', 'accelY', 'accelZ']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t, gx, gy, gz, ax, ay, az in zip(time_stamp, gyroX, gyroY, gyroZ, accelX, accelY, accelZ):
            writer.writerow({
                'time_stamp': t,
                'gyroX': gx,
                'gyroY': gy,
                'gyroZ': gz,
                'accelX': ax,
                'accelY': ay,
                'accelZ': az
                })

def on_close_dummy(event):
    pass

fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update_graph, interval=SampleRate)
plt.show()
input("Press Enter to exit...")