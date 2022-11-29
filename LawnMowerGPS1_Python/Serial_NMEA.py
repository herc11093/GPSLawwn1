import io

import pynmea2,time,pyproj
import serial
import pyproj
import GV,os
import time


import socket
import sys

#nmeaser = False
#nmeasoc = True

#nmeasoc = True   #8/11
def SetInput(nmeaser,nmeasoc):
    if nmeaser == True :
        ser = serial.Serial('/dev/ttyACM0', 38400, timeout=0.1)
        #ser = serial.Serial('COM9', 38400, timeout=0.1)
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    if nmeasoc == True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 2224)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)




    #ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
    #ser = serial.Serial('COM9', 38400, timeout=0.1)
    #sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    #sio = open("NMEA.txt", "r")
    timestr = time.strftime("%Y%m%d-%H%M")
    fname = timestr + "NMEA_log.csv"
    fout = open(fname, "a+")

def readsoc():
    #global sock
    try:
        request_line = b""
        while not request_line.endswith(b'\n'):
            request_line += sock.recv(1)
        aa = request_line.decode("utf-8") 
        ff = len(aa)-2
        aa = aa[:ff]
        #print(aa)
        return aa
    except:
        print("Failed Socket")


def dm(x):
    degrees = int(float(x)) // 100
    minutes = float(x) - 100*degrees
    #print(degrees,minutes)     
     
    return degrees, minutes

def decimal_degrees(degrees, minutes):
     
    return degrees + minutes/60 
        #print (decimal_degrees(*dm(3648.5518)))

def UbloxRead():
    ddd=0
    p = pyproj.Proj(proj='utm', zone=29, ellps='WGS84')

    while 1:
        line = ""
        if nmeaser == True:
            line = sio.readline()
        if nmeasoc == True:
            line = readsoc()
        #line = sio.readline()
        fout.write(line)
        #print(line)
        #print( line[1:6])
        if line[1:6] == "GNGGA"or line[1:6] == "GPGGA":
            try:    
                msg = pynmea2.parse(line)
                #print(repr(msg))
                laty = decimal_degrees(*dm(msg.lat))
                lonx = decimal_degrees(*dm(msg.lon))
                lonx = lonx*(-1)
                qual = msg.gps_qual
                GV.Qual = qual
                print(lonx,laty)
                x,y = p(lonx, laty)
        
  #              
  #              ddd=ddd+1
  #              ss = str(x)+","+str(y)+","+str(ddd)
  #              print(ss)
                
                ddd=ddd+1
                ss = str(x)+","+str(y)+","+str(qual)+","+str(ddd)
                #print(ss)
               # ss= msg+",,,"+ss
                fout.write(str(msg))
                fout.write(",,,,")
                fout.write(ss)
                fout.write("\n")
                GV.currentx1 = x
                GV.currenty1 = y
                #print (GV.currentx1,GV.currenty1)
            except serial.SerialException as e:
                print('Device error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                continue
            time.sleep(0.1)
            

#UbloxRead()
