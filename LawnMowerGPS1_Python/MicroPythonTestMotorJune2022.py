import time
#import board
#import busio
#import bno055
#from analogio import AnalogIn
#from digitalio import DigitalInOut, Direction, Pull
import machine
from bno055 import *
from machine import UART
from machine import Pin, SoftI2C

qq=0
analog_in1 = machine.ADC(machine.Pin(36))#wheel
analog_in1.atten(machine.ADC.ATTN_11DB) 
analog_in2 = machine.ADC(machine.Pin(39))#Box pot
analog_in2.atten(machine.ADC.ATTN_11DB)
switch1 = machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_UP)
switch2 = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP)
switch3 = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)
switch4 = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

Out1 = machine.Pin(27, machine.Pin.OUT) #ENB Channel Pin 14 
Out2 = machine.Pin(13, machine.Pin.OUT)  #RENA Channel Pin 12
#Out3 = machine.Pin(13, machine.Pin.OUT)
#Out4 = machine.Pin(14, machine.Pin.OUT)
motorout1 =machine.PWM(machine.Pin(12)) #PWM Cahnnel Pin 27
motorout1.freq(50)
stat = True
uart = UART(2, tx=17, rx=16)
#uart = UART(1, baudrate=19200)
uart.init(19200, bits=8, parity=None, stop=1,timeout = 10)

i2c = machine.I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
imu = BNO055(i2c)
calibrated = False
zerosett =1820
cursterringang = 0

def getbnoangle():
    global imu
    dd = imu.euler()
    ee = int(dd[0])
    if ee  > 180:
        ee=ee-360
    ee = ee*4000/270   
    return ee

def setpwm(ww, power):
    global motorout1,Out1,Out2,cursterringang,qq,motorsteer
    #print(power)
    dd = 0
    if power >14:
        dd = 900
    elif power == 5:
        dd = 300
    elif power == 2:
        dd =150
    #print (ww)
    
    motorout1.duty(dd)
    
    if ww > 2: #turn off poweer to steering
        if cursterringang > -30*14.8:
            Out1.value(1) 
            Out2.value(0)
            motorsteer = "Right_" + str(power)
            #if qq>20:
            #    print ("Right")
                
        else:
            Out1.value(0) 
            Out2.value(0)
            motorsteer = "RightNoMore"
            if qq>20:
                print ("Turn Right no more",str(cursterringang),str(-30*14.8))         
    elif ww < 2:
        if cursterringang < 30*14.8:
            Out1.value(0) 
            Out2.value(1)
            motorsteer = "Left_" + str(power)
            
            #if qq >20:
            #    print("Left")
         #   if qq>99:
         #       print("Turn Left            ",str(cursterringang),str(45*14.8))
        else:
            Out1.value(0) 
            Out2.value(0)
            motorsteer = "LeftNoMore"
            if qq>20:
                print("Turn Left no more      ",str(cursterringang),str(30*14.8))
    elif ww == 2:
        Out1.value(0) 
        Out2.value(0)
        motorout1.duty(0)
        motorsteer = "Off"
        #if qq>99:
        #    print("Straight on")
def getwheelangle():
    global analog_in1
    x = analog_in1.read()
    #print("WheelAngle =",str(x))
    return x # need multiplier here to convert voltage to degrees

def getpotangle():
    global analog_in2
    x = analog_in2.read()
    if x<1350:
        x=1350
    if x>2400:
        x =2400
    #print("PotAngle =",str(x))
    
    return x # need multiplier here to convert voltage to degrees


def readserialdata(newangle):
    global uart,qq,curheading
    data = uart.readline()
    
    if data is not None:
        
        #print (data)
        dd = right(data,4)
        print (data,"_________",dd)
        try:
            newangle = int(dd)*4000/270
        except:
            print("Serial data error")
        
        ff = str(curheading/14.8)#+"\n"
        
        #print(ff)
        
        uart.write(ff)
        
    return int(newangle)


def right(s, amount):
    return s[-amount:]


def loadBNO():
    global imu
    calibrated = False
    while not calibrated:
        time.sleep(1)
        if not calibrated:
            calibrated = imu.calibrated()
            print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
  
def ControlStering():
    #loadBNO()
    global zerosett,Switch1,Switch2,Switch3,cursterringang,qq,curheading,motorsteer

    newangle = 45
    curheading = 0
    cursterringang = 0
    GoGo = True
    manual = False
    stat = False
    motorsteer = "Off"
    while GoGo:
        stat = not switch2.value()
        print ("Stat = ",str(stat), "Manual ",str(manual))
        #stat = True #need to remove when real
        if stat == False:
            if manual == False:
                setpwm(2,0)
        while stat:
        #Get values
            curheading = getbnoangle()
            #print (curheading)
            ff= getwheelangle()
            cursterringang = ff - zerosett
            newangle = readserialdata(newangle)
            #newangle = -70*15
            newangle =0
            #newsterringangle = newangle-curheading
            newsterringangle = curheading - newangle
            if newsterringangle > 2664: #180 *14.8)
                #newsterringangle = 5324-newsterringangle
                newsterringangle = newsterringangle-5324
            if newsterringangle < -2664: #-180 *14.8)
                #newsterringangle = newsterringangle-5324
                newsterringangle = 5324-newsterringangle
            
            
            organg = newsterringangle
            
            
            if newsterringangle > 450:#30*4000/270:
                newsterringangle = 450
            if newsterringangle < -450:
                newsterringangle = -450               
            newsetangle = newsterringangle-cursterringang  # need multiplier here
            newsetangle = round(newsetangle,0)
            #if newsetangle > 444:#45*4000/270:
            #    newsetangle = 444
            #if newsetangle < -444:
            #    newsetangle = -444            
            
            
            
            a = round(curheading,0)
            b = round(newsterringangle,0)
            c = round(cursterringang,0)
            d = round(newsetangle,0) 
            e = round(newangle,0)
                
            
            if qq > 24:
                
                
                print("Head=",str(a)," NewSteertA=",str(b),"CurSteerA=",str(c) ,"NewSetA",str(d),"NewA=",str(e),motorsteer,str(ff),str(newsetangle))
                qq = 0
            qq = qq+1 
            if newsetangle > 400:
                setpwm(1,15)
            elif newsetangle > 200:
                setpwm(1,5)
            elif newsetangle > 10:
                setpwm(1,2)
                print("Head=",str(a)," NewSteertA=",str(b),"CurSteerA=",str(c) ,"NewSetA",str(d),"NewA=",str(e),motorsteer,str(ff),str(newsetangle))
               
            elif newsetangle < -400:
                setpwm(3,15)
            elif newsetangle < -200:
                setpwm(3,5)
            elif newsetangle < -10:
                setpwm(3,2)
                print("Head=",str(a)," NewSteertA=",str(b),"CurSteerA=",str(c) ,"NewSetA",str(d),"NewA=",str(e),motorsteer,str(ff),str(newsetangle))
               
            else:
                setpwm(2,0)
               # if qq>99: 
               #     print(" bingo ")
                #time.sleep( 1)
            #time.sleep(.1)
         
         
            #if switch1.status == 0:
             #      stat = false  #quit loop  (run steering calibration)
            stat = not switch2.value()  #Need to uncomment for real
        manual = not switch1.value()
        if manual == True:
            setpwm(2,0)
        while manual:
            
            xx = getwheelangle()
            yy = getpotangle()
            newsetangle = yy - xx
            
            if qq> 99:
                print (xx,yy,newsetangle)
                qq = 0 
            qq= qq+1
            if newsetangle > 400:
                setpwm(1,15)
            elif newsetangle > 200:
                setpwm(1,5)
            elif newsetangle > 30:
                setpwm(1,2)
            elif newsetangle < -400:
                setpwm(3,15)
            elif newsetangle < -200:
                setpwm(3,5)
            elif newsetangle < -30:
                setpwm(3,2)
            else:
                setpwm(2,0)
                #if qq>99:
                #    print(" bingo ")
            
            #time.sleep(.1)
            manual = not switch1.value()
            if not switch3.value():
                zerosett = getpotangle()
                print("Zerosett = ",str(zerosett))
                
                
def testmotor():
    global Out1,Out2,motorout1
    ee = 1
    Out1.value(1) 
    Out2.value(0)
    while ee:
        ff= getwheelangle()
        dd = 500* ff/16400
        motorout1.duty(dd)
testmotor()

#ControlStering()

print("Finishing") 
