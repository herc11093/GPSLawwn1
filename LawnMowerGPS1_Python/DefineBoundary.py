
import GV
import Auto_Steer_Trig
#import loadField
import math
import threading
import time
#import RPi.GPIO as GPIO 
#import Serial_NMEA
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from tkinter import filedialog

import os



def importboundry():

    from csv import reader
    # iterate over each line as a ordered dictionary and print only few column by column Number
    #with open('field2.csv', 'r') as read_obj:
    #with open('Field3.csv', 'r') as read_obj:
    root = tk.Tk()
    root.withdraw() 

    file_path = filedialog.askopenfilename()
    print(file_path)
    with open(file_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        oldx=0
        oldy=0
        for row in csv_reader:
          
            a = row[0]
            b = row[1]
           # print(a,b)
            try:
                aa = float(a)
                bb = float(b)
                dis = Auto_Steer_Trig.distance2Point(aa,bb,oldx,oldy)
                if dis>1 :
                    GV.PointX.append(aa)
                    GV.PointY.append(bb)
                    print(aa, bb)
                    oldx = aa
                    oldy= bb
            except:
                print("bad data")
                
            


    #print (GV.PointY,GV.PointY)
def saveboundary():
    fname = "boundary1234.csv"
    try:
            os.remove(fname)
    except:
        print("no file to delete")
    fout1 = open(fname, "a+")
    x=1
    oldx = 0
    oldy = 0

    while x < len(GV.PointX):
        aa=GV.PointX[x]
        bb=GV.PointY[x]
        slope = Auto_Steer_Trig.GetSlope(aa,bb,oldx,oldy)
        cc = Auto_Steer_Trig.GetAngle(aa,bb,oldx,oldy)
        dis = Auto_Steer_Trig.distance2Point(aa,bb,oldx,oldy)

        txt = str(GV.PointX[x]) + ","+str(GV.PointY[x])+","+ str(slope)+","+str(cc) + "\n"
        print(txt)
        fout1.write(txt)
        x=x+1
        oldx=aa
        oldy=bb

    fout1.close

importboundry()
saveboundary()