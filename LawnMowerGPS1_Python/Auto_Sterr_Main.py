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


#AutoSteer_Setup.Loadconfigfile()
#load Field Data
#filedData = np.genfromtxt('myfile.csv',delimiter=',')

#def I2Cwrite(value):  #i2C stuff
#    bus.write_byte_data(address, 0, value)
#    return -1


GV.startx = 1
GV.starty = 1

#GV.finishx = 200.4
#GV.finishy = 50.12
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


def FieldRunLoop():
   # global GV.startx, GV.starty, GV.finishx, GV.finishy, GV.currentx1, GV.currenty1, GV.CurrentHeader, GV.Set_SteerAng,Simstopstart
  

    #load field into array
    #start field
    #get field size
    fieldpoints = 100
    fieldpoints = 2

    fieldpoints = len(GV.PointX)-1
    GV.gogo = 0 #90
    GV.dist =[0]


    #test cords.


    print("Round1")
   # flogtrack= open("logtrack.csv","w+")
    GV.flogtrack.write("AimAng1,AimAang2,Aimx,Aimy,GV.currentx1,GV.currenty1,GV.startx,GV.starty,GV.finishx,GV.finishy,dist,GV.Set_SteerAng,GV.Steerangle,GV.gogo,GV.ToEndPoint,GVQual")
    GV.flogtrack.write('\n')   

    for i in range(0 ,(fieldpoints)) :
        #co py fieldpoint i to global variable
        #updqate .ini file for current position

        j=1
        GV.startx = GV.PointX[i]
        GV.starty  = GV.PointY[i]
        GV.finishx  = GV.PointX[i+1]
        GV.finishy = GV.PointY[i+1]
        GV.CurPathAng = math.atan2((GV.finishy-GV.starty),(GV.finishx-GV.startx ))  #needed for drift correction calculation
        #print (GV.startx,GV.starty  )
        NextX = GV.PointX[i+2]
        NextY = GV.PointY[i+2]
        slopeline = Auto_Steer_Trig.GetSlope(GV.startx,GV.starty,GV.finishx,GV.finishy)
        slopeline2 =  Auto_Steer_Trig.GetSlope(GV.finishx,GV.finishy,NextX, NextY)
        con = Auto_Steer_Trig.FindC(GV.startx,GV.starty,slopeline)
        con2 = Auto_Steer_Trig.FindC(NextX,NextY,slopeline2)
        print(i)
        lengthofrun = Auto_Steer_Trig.distance2Point(GV.startx,GV.starty,GV.finishx,GV.finishy) #cal max lenght of run
# take out drift erro form the previous line

        AveErr = sum(GV.ErrDist)/len(GV.ErrDist)
        if (AveErr) > .075:
            Gv.gogo = Gv.gogo+AveErr
        elif (AveErr) < -.075:
            Gv.gogo = Gv.gogo+AveErr
        else:
            GV.gogo = Gv.gogo
        GV.ErrDist.clear()


        while j == 1:
            GV.dist = round(Auto_Steer_Trig.shortest_distance(GV.currentx1, GV.currenty1, slopeline, con),2)
            #Drift error compensation section
            if GV.Left:
                GV.dist = GV.dist*(-1)
            if (GV.dist > 0 AND GV.dist <1.5):
                GV.ErrDist.append(GV.dist)
        #        GV.ErrDist.pop(0)
            if (GV.dist < 0 AND GV.dist >-1.5):
                GV.ErrDist.append(GV.dist)
        #        GV.ErrDist.pop(0)

        
        
            #GV.dist = round(Auto_Steer_Trig.shortest_distance(GV.currentx1, GV.currenty1, slopeline2, con2),1)
            Auto_Steer_Trig.getSteerAngle()
            print (GV.dist)
            #print("Set_Steerang", GV.Set_SteerAng )
            #GV.ToEndPoint = round(Auto_Steer_Trig.distance2Point(GV.currentx1,GV.currenty1,GV.finishx,GV.finishy),)
            GV.ToEndPoint = round(Auto_Steer_Trig.shortest_distance(GV.currentx1, GV.currenty1, slopeline2, con2),1)
            #GV.currentx1=round(GV.currentx1,2)
            #GV.currenty1=round(GV.currenty1,2)

            print('{} - {};   {} - {};   {} - {}; error {}   {},{} ,   {}, To End-{}'  .format((round(GV.currentx1,1)), (round(GV.currenty1,1)),(round( GV.startx,1)), (round(GV.starty,1)), (round(GV.finishx,1)), (round(GV.finishy)),round(GV.dist,1), (GV.Set_SteerAng), GV.Steerangle, GV.gogo,GV.ToEndPoint ))           
            GV.flogtrack.write('{},{},{},{},{},{}, {},{},{},{},{},{}'  .format(GV.currentx1, GV.currenty1, GV.startx, GV.starty, GV.finishx, GV.finishy,GV.dist, GV.Set_SteerAng, GV.Steerangle, GV.gogo,GV.ToEndPoint,GV.Qual ))
            GV.flogtrack.write('\n')
            try:
                UpdateGUI()
            except:
                print("Failed to update GUI")
            #print(GV.Set_SteerAng)
            #dd = "    "+str(GV.Set_SteerAng)
            dd = str(GV.Set_SteerAng)
            
           
            #print(GV.SerialPort_On)
            if GV.  SerialPort_On:
                #GV.ser.write( dd)
                ser.write(bytes(dd, 'UTF-8'))
            
                #ser.write(bytes(dd))
                print("Set Steeering angle                                              ",dd)
                ee = ser.readline()   #  need to come back to
                #ee = 10
                print (ee)  
                try:
                    GV.Steerangle = float(ee   )
                except:
                    print("Invalid heading entry")    
                #print(ee)
                #ser.write(bytes(tim, 'UTF-8'))
                #ser.write(bytes(str(GV.Set_SteerAng), 'UTF-8'))
                print(dd,"______________________________",ee)
                
                #time.sleep(0.5)
                
            #disfromstart= Auto_Steer_Trig.distance2Point(GV.startx,GV.starty,GV.currentx1,GV.currenty1)
            #ddee = lengthofrun - disfromstart
            #print (GV.startx,GV.starty,GV.currentx1,GV.currenty1)
            #print (lengthofrun,disfromstart,ddee)
            
            #if ddee <3:
            if GV.ToEndPoint < 3.0:
                
                j=2 #fF nish CurrentLine
           # if keyboard.is_pressed('q'):  # if key 'q' is pressed quit program
           #     print("key pressed")
           #     j = 1000
           #     i=10000
           #     i=fieldpoints
           #     GV.Simstopstart = 1000
           #     print('Quitting track')
           #     GV.flogtrack.close
           #     print("Close File")
                #GV.ser.close()
            time.sleep (.05)
def UpdateGUI():
     global labelcurx,labelcury,labelfinx,labelfiny,labeldist,labelsetang,labelgogo,labeltoend,labelactang
     labelcurx.config(text = round(GV.currentx1,1) )
     labelcury.config(text = round(GV.currenty1,1) )
     labelfinx.config(text =  round(GV.finishx,1) )
     labelfiny.config(text = round(GV.finishy))
     labeldist.config(text = round(GV.dist,1) )
     labelsetang.config(text = GV.Set_SteerAng )
     labelactang.config(text = GV.Steerangle )
     labelgogo.config(text = GV.gogo)
     labeltoend.config(text = GV.ToEndPoint )
def LoadGUI():
    global labelcurx,labelcury,labelfinx,labelfiny,labeldist,labelsetang,labelgogo,labeltoend,labelactang
    root = tk.Tk()
    root.title('AutoSteer Field')
    root.geometry('700x400')
    root.resizable(False, False)
    frame = ttk.Frame(root)
    print("Starting Gui")

    # field options
    options = {'padx': 10, 'pady': 20}
    labelx = ttk.Label(frame, text='X Coord')
    labelx.grid(column=1, row=2,  **options)
    labely = ttk.Label(frame, text='Y Coord')
    labely.grid(column=4, row=2,  **options)
    labelcurx = ttk.Label(frame, font=('Arial', 20),text='54321.123')
    labelcurx.grid(column=2, row=2, sticky='W', **options)
    labelcury = ttk.Label(frame,  font=('Arial', 20),text='4567.21')
    labelcury.grid(column=5, row=2,  **options)


    labelfx = ttk.Label(frame, text='FinishX')
    labelfx.grid(column=1, row=1,  **options)
    labelfinx = ttk.Label(frame, text='-0')
    labelfinx.grid(column=2, row=1,  **options)
    labelfy = ttk.Label(frame, text='FinishX')
    labelfy.grid(column=4, row=1,  **options)
    labelfiny = ttk.Label(frame, text='-0')
    labelfiny.grid(column=5, row=1,  **options)

    
    labeldi = ttk.Label(frame, text='Error')
    labeldi.grid(column=1, row=3,  **options)
    labeldist = ttk.Label(frame, font=('Arial', 20),text='-0')
    labeldist.grid(column=2, row=3,  **options)
    labelang = ttk.Label(frame, text='Set Ang')
    labelang.grid(column=4, row=3,  **options)
    labelsetang = ttk.Label(frame, text='-0')
    labelsetang.grid(column=5, row=3,  **options)
    labelact = ttk.Label(frame, text='Set Ang')
    labelact.grid(column=4, row=5,  **options)
    labelactang = ttk.Label(frame, text='-0')
    labelactang.grid(column=5, row=5,  **options)

    labelgo = ttk.Label(frame, text='Gogo')
    labelgo.grid(column=1, row=4,  **options)
    labelgogo = ttk.Label(frame, text='-0')
    labelgogo.grid(column=2, row=4,  **options)
    labelto = ttk.Label(frame, text='To End')
    labelto.grid(column=4, row=4,  **options)
    labeltoend = ttk.Label(frame, font=('Arial', 20), text='-0')
    labeltoend.grid(column=5, row=4,  **options)

  #  SP_button = ttk.Button(frame,text='Save point')
  #  SP_button.grid(column=1, row=6,  ipady=20, ipadx=15,**options)
  #  SP_button.configure(command=SP_button_clicked)
  #  UP_button = ttk.Button(frame, text='Update point')
  #  UP_button.grid(column=3, row=6,  ipady=20, ipadx=15, **options)
  #  UP_button.configure(command=UP_button_clicked)
    exit_button = ttk.Button(frame,    text='Exit', command=lambda: root.quit())
    exit_button.grid(column=5, row=6, ipady=15, ipadx=15, **options)
    
    frame.grid(padx=6, pady=6)
    # start the GUI
    print("loading GUI loop")
    
    root.mainloop()

print("Starting")
#thread2 = _thread.start_new_thread(AutoSteerSumulator.Runsimulator,())

#thread1 = _thread.start_new_thread(FieldRunLoop(),())
#thread2 = _thread.start_new_thread(TempPy.RunSimFile(),())


#status = threading.Thread(target=TempPy.RunSimFile)
status = threading.Thread(target= Serial_NMEA.UbloxRead)
status.start()
print("Starting 2")
status2 = threading.Thread(target=FieldRunLoop)
status2.start()
print("Load GUI")

LoadGUI()
#freeze_support()
#status = multiprocessing.Process(target=TempPy.RunSimFile)
#status.start()
#print("Starting 2")
#status2 = multiprocessing.Process(target=FieldRunLoop)
#status2.start()

#TempPy.RunSimFile()

##FieldRunLoop()

print("Finishing")



