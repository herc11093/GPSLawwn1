
import pynmea2,pyproj,GV,time,os
#import utm





def dm(x):
    degrees = int(float(x)) // 100
    minutes = float(x) - 100*degrees
    #print(degrees,minutes)
     
    return degrees, minutes

def decimal_degrees(degrees, minutes):
    return degrees + minutes/60 
#print (decimal_degrees(*dm(3648.5518)))

def RunSimFile():
    if os.path.exists("latlong,csv"):
        os.remove("latlong,csv")
    file = open('NMEA2.txt')
    fout = open("latlong,csv", "a+")
    p = pyproj.Proj(proj='utm', zone=29, ellps='WGS84')

    ddd = 0
    for line in file.readlines():
        try:          
            msg = pynmea2.parse(line)
            #print(repr(msg))
            #print(msg.lat,msg.lon)
            laty = decimal_degrees(*dm(msg.lat))
            lonx = decimal_degrees(*dm(msg.lon))*(-1)
            #print(lonx,laty)
    #        x,y = p(laty, lonx)
    #        ss = str(x)+","+str(y)+"\n"
    #        print(ss)
            x,y = p(lonx, laty)
            ddd=ddd+1   
            
            
            ss = str(x)+","+str(y)+","+str(ddd)+"\n"
            ee = int(ddd) % 10
            if ee == 1:
                print(repr(msg))
                print(ss)


        #    coordinate_1 = (lonx,laty)
        #    utm_conversion = utm.from_latlon(coordinate_1[0],coordinate_1[1])
        #    print(utm_conversion)

    #        coordinate_1 = (laty,lonx)
     #       utm_conversion = utm.from_latlon(coordinate_1[0],coordinate_1[1])
      #      print(utm_conversion)
       #     print("test")

            fout.write(ss)
            GV.currentx1 = x
            GV.currenty1 = y
            #print (GV.currentx1,GV.currenty1)
            time.sleep(0.05)
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue
