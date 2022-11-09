import math
import time
import GV
import keyboard
import random

currentheader = 0
GV.SerialPort_On = False
GV.currentx1 = 100
GV.currenty1 = 100

def Runsimulator():
#    global GV.SteerAng ,GV.startx ,GV.currentheader ,GV.currentx1 ,GV.currenty1,GV.Set_SteerAng,Simstopstart

    Speed = 0.5   # 1M per second
#    GV.currentx1 = GV.startx
#    GV.currenty1 = GV.startx -20
    #currentheader = 0
#    GV.Simstopstart = 1
    GV.gogo = 90
#    GV.Set_SteerAng = 0
    print("Start_Simulator")
    while GV.Simstopstart == 1:
        
        if GV.Set_SteerAng-GV.Steerangle>20:
            GV.Steerangle = GV.Steerangle + 20
        elif GV.Set_SteerAng - GV.Steerangle > 6:
            GV.Steerangle = GV.Steerangle + 6
        elif GV.Set_SteerAng - GV.Steerangle > 2:
            GV.Steerangle = GV.Steerangle + 3
        elif GV.Set_SteerAng - GV.Steerangle > 0.1:
            GV.Steerangle = GV.Set_SteerAng


        if GV.Set_SteerAng- GV.Steerangle < -20:
            GV.Steerangle = GV.Steerangle - 20
        elif GV.Set_SteerAng- GV.Steerangle < -4:
            GV.Steerangle = GV.Steerangle - 6
        elif GV.Set_SteerAng- GV.Steerangle < -2:
            GV.Steerangle = GV.Steerangle - 3
        elif GV.Set_SteerAng- GV.Steerangle < -.01:
            GV.Steerangle = GV.Set_SteerAng

        if GV.Steerangle > 20:
           GV.gogo = GV.gogo +20
        elif GV.Steerangle > 10:
           GV.gogo = GV.gogo + 8
        elif GV.Steerangle > 4:
           GV.gogo = GV.gogo + 5
        elif GV.Steerangle > 1:
           GV.gogo = GV.gogo + 1

        if GV.Steerangle < -20:
           GV.gogo = GV.gogo -20
        elif GV.Steerangle < -10:
           GV.gogo = GV.gogo - 8
        elif GV.Steerangle < -4:
           GV.gogo = GV.gogo - 5
        elif GV.Steerangle < -1:
           GV.gogo = GV.gogo - 1
        
        if GV.SerialPort_On == True:  #if serial port turned on readback number from ESP32 
            SerialString = GV.ser.readline()
            GV.gogo = int(SerialString)#*0.0174533
         
        #GV.gogo = GV.Steerangle
        #print(" Set_SteerAng  Steerangle",GV.Set_SteerAng,GV.Steerangle)
        newx = GV.currentx1 + Speed* math.sin(math.radians(GV.gogo))#+(random.randint(-1,1)*0.1)
        newy = GV.currenty1 + Speed* math.cos(math.radians(GV.gogo))#+(random.randint(-1,1)*0.1)
      #  a = Speed* math.cos(math.radians(GV.gogo))
       # b = Speed* math.sin(math.radians(GV.gogo))
    #    print("Sim x y",round(a,2) ,round(b,2))


        GV.currentx1 = newx
        GV.currenty1 = newy
        time.sleep (.05)
       # print(newx,newy)

        if keyboard.is_pressed('q'):  # if key 'q' is pressed quit program
            j = 1000
            i=10000
            GV.Simstopstart = 1000
            print('Quitting simulator')
