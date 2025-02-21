#Credits to The Bored Robot @ Youtube (https://www.youtube.com/watch?v=PhDPnjF3_tA&list=PLDQbF7EgWNg9_Aem8LEkfW5HC1zEHC3BM&index=3&t=162s)

import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import csv

SampleRate = 200

SERIAL_PORT = "com6"
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)


names = []

def smartParser(ser): #Parse data from the serial port, every separate string is the name of the variable and the number following it is the value
    data = ser.readline().decode('utf-8').strip()
    data = data.split("\t")
    print(data)
    for variable in data:
        if variable.split(":")[0] in names:
            print("recieving ", len(names), " variables")
            break
        names.append(variable.split(":")[0])
    
    


def read_serial(ser):
    data = ser.readline().decode('utf-8').strip()
    data = data.split("\t")


    print(f'gyrox: {data[1]}, gyroy: {data[2]}, gyroz: {data[3]}, accelx: {data[4]}, accely: {data[5]}, accelz: {data[6]}')

def update_graph(frame):
    read_serial(ser)
    plt.cla()
    #plt.plot(time_stamp, gyroX, label='gyroX')
    plt.xlabel('time (s)')
    plt.ylabel(names)
    plt.legend(loc='upper left')
    #plt.tight_layout()
    plt.legend()

def on_close_dummy(event):
    pass

#ig, ax = plt.subplots()
#fig.canvas.mpl_connect('close_event', on_close_dummy)

#ani = FuncAnimation(fig, update_graph, interval=SampleRate)
#plt.show()

while True:
    smartParser(ser)
input("Press Enter to exit...")