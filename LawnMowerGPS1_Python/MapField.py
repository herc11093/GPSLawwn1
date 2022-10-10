import GV
import Auto_Steer_Trig
#import loadField
import math
import threading
import time
import RPi.GPIO as GPIO 
#import Serial_NMEA
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror




def nextPoint(xx,yy,angle,midx,midy,widthb):    
    test1x = xx + math.cos(angle)*widthb
    test2x = xx - math.cos(angle)*widthb

    test1y = yy + math.sin(angle)*widthb
    test2y = yy - math.sin(angle)*widthb

    d1 = Auto_Steer_Trig.distance2Point(test1x,test1y,midx,midy)
    d2 = Auto_Steer_Trig.distance2Point(test2x,test2y,midx,midy)

    if d1<d2:
        xxx= test1x
        yyy = test1y
    else:
        xxx= test2x
        yyy = test2y

    return xxx,yyy



def printlisttofile():
    global labelfilename
    timestr = time.strftime("%Y%m%d-%H%M")
    fname = "field_" + timestr + ".csv"
    textfile = open(fname, "w")
    i=0
    labelfilename.config(text = fname)
    for element in GV.PointX:
         textfile.write( str(GV.PointX[i]) + "," + str(GV.PointY[i]) + "\n")
         i = i+1
    textfile.close()

def waitbuttonpress():

   GPIO.setmode(GPIO.BCM)
   GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)

   GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)


   a=1
   b=0
   while a:
        if not GPIO.input(17):  #zero counter
            b = 0        

        if not GPIO.input(27):  #lob  location
          

        
            time.sleep(1)
            print(b)
            print(GV.currentx1,GV.currenty1)
            time.sleep(1)
            print(GV.currentx1,GV.currenty1)
            time.sleep(1)
            print(GV.currentx1,GV.currenty1)
            time.sleep(1)
            print(GV.currentx1,GV.currenty1)
            GV.PointX.append(GV.currentx1)
            GV.PointY.append(GV.currenty1)
            #print(GV.PointX[b],GV.PointY[b])
            b=b+1
        else:
            x = GV.currentx1
            y = GV.currenty1
        if b == 4 :
            a =0


def importboundry():

    from csv import reader
    # iterate over each line as a ordered dictionary and print only few column by column Number
    #with open('field2.csv', 'r') as read_obj:
    #with open('Field3.csv', 'r') as read_obj:
    with open('Boundry.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
    
        for row in csv_reader:
        
            a = row[0]
            b = row[1]
           # print(a,b)
            aa = float(a)
            bb = float(b)
        #    print(aa,bb)

            GV.PointX.append(aa)
            GV.PointY.append(bb)
        
            print(a, b)

    print (GV.PointY)



def SP_button_clicked():
    global b
    try:
        GV.PointX.append(GV.currentx1)
        GV.PointY.append(GV.currenty1)
        print(GV.currentx1,GV.currenty1)
        b=b+1
        labelfilename.config(text = "")
        if b == 4 :
            clacpathway()
            printlisttofile()
            GV.PointX.clear()
            GV.PointY.clear()
            b=0
        labelsavepoint.config(text= b)
        labelcurx.config(text = round(GV.currentx1,2))
        labelcury.config(text = round(GV.currenty1,2))
        
    except ValueError as error:
        showerror(title='Error', message=error)

def UP_button_clicked():
    labelcurx.config(text = round(GV.currentx1,2))
    labelcury.config(text = round(GV.currenty1,2))
    labelfilename.config(text = "")

def LoadGUI():
    global labelcurx,labelcury,labelsavepoint,labelfilename
    root = tk.Tk()
    root.title('Map Field')
    root.geometry('700x300')
    root.resizable(False, False)
    frame = ttk.Frame(root)


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
    labelsp = ttk.Label(frame, text='Save Point')
    labelsp.grid(column=4, row=1,  **options)
    labelsavepoint = ttk.Label(frame, text='-0')
    labelsavepoint.grid(column=5, row=1,  **options)
    labelfilename = ttk.Label(frame, text='')
    labelfilename.grid(column=1, row=4,  **options)
    SP_button = ttk.Button(frame,text='Save point')
    SP_button.grid(column=1, row=3,  ipady=20, ipadx=15,**options)
    SP_button.configure(command=SP_button_clicked)
    UP_button = ttk.Button(frame, text='Update point')
    UP_button.grid(column=3, row=3,  ipady=20, ipadx=15, **options)
    UP_button.configure(command=UP_button_clicked)
    exit_button = ttk.Button(frame,    text='Exit', command=lambda: root.quit())
    exit_button.grid(column=5, row=3, ipady=15, ipadx=15, **options)
    
    frame.grid(padx=6, pady=6)
    # start the GUI
    root.mainloop()

def clacpathway():
    widthoftravel = 0.25

    M1 = Auto_Steer_Trig.GetSlope(GV.PointX[0],GV.PointY[0],GV.PointX[1],GV.PointY[1])
    M2 = Auto_Steer_Trig.GetSlope(GV.PointX[1],GV.PointY[1],GV.PointX[2],GV.PointY[2])
    M3 = Auto_Steer_Trig.GetSlope(GV.PointX[2],GV.PointY[2],GV.PointX[3],GV.PointY[3])
    M4 = Auto_Steer_Trig.GetSlope(GV.PointX[3],GV.PointY[3],GV.PointX[0],GV.PointY[0])

    ang1 = math.atan(M1)
    ang2 = math.atan(M2)
    ang3 = math.atan(M3)
    ang4 = math.atan(M4)


    C1= Auto_Steer_Trig.FindC(GV.PointX[0],GV.PointY[0],M1)
    C2= Auto_Steer_Trig.FindC(GV.PointX[1],GV.PointY[1],M2)
    C3= Auto_Steer_Trig.FindC(GV.PointX[2],GV.PointY[2],M3)
    C4= Auto_Steer_Trig.FindC(GV.PointX[3],GV.PointY[3],M4)


    MidX = (GV.PointX[0]+GV.PointX[1]+GV.PointX[2]+GV.PointX[3])/4
    MidY = (GV.PointY[0]+GV.PointY[1]+GV.PointY[2]+GV.PointY[3])/4
    print ("Mid")
    print (MidX,MidY)



    print("Starting")
    rowaround = 0
    for i in range(10):
        nextpoint = nextPoint(GV.PointX[(0+rowaround)],GV.PointY[(0+rowaround)],ang4,MidX,MidY,widthoftravel)
        GV.PointX.append(nextpoint[0])
        GV.PointY.append(nextpoint[1])
        print (nextpoint)
        nextpoint = nextPoint(GV.PointX[(1+rowaround)],GV.PointY[(1+rowaround)],ang2,MidX,MidY,widthoftravel)
        GV.PointX.append(nextpoint[0])
        GV.PointY.append(nextpoint[1])
        print (nextpoint)
        nextpoint = nextPoint(GV.PointX[(2+rowaround)],GV.PointY[(2+rowaround)],ang2,MidX,MidY,widthoftravel)
        GV.PointX.append(nextpoint[0])
        GV.PointY.append(nextpoint[1])
        print (nextpoint)
        nextpoint = nextPoint(GV.PointX[(3+rowaround)],GV.PointY[(3+rowaround)],ang4,MidX,MidY,widthoftravel)
        GV.PointX.append(nextpoint[0])
        GV.PointY.append(nextpoint[1])
        print (nextpoint)
        rowaround = rowaround+4

def loadpopints():
    GV.PointX.append(613505.44)
    GV.PointY.append(5842725.3)
    
    GV.PointX.append(613505.44)
    GV.PointY.append(5842725.3)
    
    GV.PointX.append(613505.44)
    GV.PointY.append(5842725.3)
    
    GV.PointX.append(613505.44)
    GV.PointY.append(5842725.3)
    

def loadnewpoints():
    global status,b
    b =0
    
    print("Starting Gui")
    LoadGUI()
#    importboundry()
##    waitbuttonpress()
#    clacpathway()
#    printlisttofile()
    #status.stop()



status = threading.Thread(target= Serial_NMEA.UbloxRead)
status.start()
time.sleep(2)
print("Starting 2")
status2 = threading.Thread(target=loadnewpoints)
status2.start()










