import math
import loadField
import serial
import GV
import Auto_Steer_Trig
import AutoSteerSumulator
import AutoSteer_Setup
import keyboard
import time
import _thread
import threading
import TempPy
import Serial_NMEA
from tkinter import ttk
from tkinter.messagebox import showerror
import tkinter as tk
GV.currentx1 = 2
GV.currenty1 = 2
#GV.CurrentntHeader = 0
GV.Set_SteerAng = 0.0

if GV.SerialPort_On: 
    #ser=serial.Serial(port = "COM3", baudrate=19200,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
     ser = serial.Serial(            
     port='/dev/serial0',
     baudrate = 19200,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS,
     timeout=0.1
     )
     print ("Starting serl port")
     tim = "30"
     ser.write(bytes(tim, 'UTF-8'))




def TeachField()
    cposx = GV.currentx1    
    cposy = GV.currenty1







print("Starting")
timestr = time.strftime("%Y%m%d-%H%M")
fname = timestr + "_boundary.csv"
fout1 = open(fname, "a+")


#status = threading.Thread(target=TempPy.RunSimFile)
status = threading.Thread(target= Serial_NMEA.UbloxRead)
status.start()
print("Starting 2")
status2 = threading.Thread(target=TeachField)
status2.start()