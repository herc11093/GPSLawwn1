import serial
import pynmea2
import utm
global UTMxy




def OpenSERPort():
    global serialPort
    port = "/dev/serial0"
    serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)

def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        #print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats)
        UTMxy = utm.from_latlon(msg.lat, msg.lon)
 

def GetGPSS_Cord():
    global serialPort
    OpenSERPort()
    while True:

        str = serialPort.readline()
        parseGPS(str)



      