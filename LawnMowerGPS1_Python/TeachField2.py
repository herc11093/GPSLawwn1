import GV
import _thread
import threading
import TempPy
import Serial_NMEA
from tkinter import ttk
from tkinter.messagebox import showerror
import tkinter as tk

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)



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



def UpdateGUI():
     global labelcurx,labelcury,,labeltoend
     labelcurx.config(text = round(GV.currentx1,1) )
     labelcury.config(text = round(GV.currenty1,1) )
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

def TeachField():
    oldcposx = 1
    oldposy = 1
    runtime  = True
    keyswitch=True
    timestr = time.strftime("%Y%m%d-%H%M")
    fname = "/Teach/"+timestr + "_boundary.csv"
    text = "p,x,y"
    fout1 = open(fname, "a+")
    fout1.write(text)
    pointnumber=1
    
    while runtime:
        keyswitch = GPIO.input(17)
        while keyswitch:
            try:
                UpdateGUI()
            except:
                print("Failed to update GUI")
            cposx = GV.currentx1
            cposy = GV.currenty1
            ddis = Auto_Steer_Trig.distance2Point(cposx,cposy,oldcposx,oldposy)
            if ddis>2:
                text = str(p)+","+str(cposx)+","+str(cposy)
                p=p+1
                fout1.write(text)
                print(text)


print("Starting")



#status = threading.Thread(target=TempPy.RunSimFile)
status = threading.Thread(target= Serial_NMEA.UbloxRead)
status.start()
print("Starting 2")
status2 = threading.Thread(target=TeachField)
status2.start()
print("Load GUI")

LoadGUI()