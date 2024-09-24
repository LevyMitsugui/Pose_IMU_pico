import Serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

importcsv

SERIAL_PORT = "com9"
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
    data = line.split("\t")
    
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