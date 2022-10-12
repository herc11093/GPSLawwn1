#import numpy
import math
from pyproj import Proj   #Lat Long to UTM
#gloabal variables
#global startx,starty,finishx,finishy,currentheader,currentx1,currenty1

import GV

def GetSlope(x1,y1,x2,y2):
    if x1-x2 ==0:
        slope =0
    else:
        slope = (y2-y1)/(x2-x1)
    return slope


def FindC(x1,y1,m):
    #y =mx+c
    #c = y-mx
    c = y1 - m*x1
    return c

def GetAngle(x1,y1,x2,y2):
    xx= x1-x2
    yy =y1-y2
    ang = math.atan2(yy,xx)
    ang = ang*57.2958
    return ang



def shortest_distance(x1, y1, m, c):
    #ax +by + c =0  : make b -1
    b = -1
    d = abs((m * x1 + b * y1 + c)) / (math.sqrt(m * m + b * b)) 
    #print("Perpendicular distance is"),d
    return d


def distance2Point(x1,y1,x2,y2):
    a = (x1-x2)*(x1-x2)
    b= (y1-y2)*(y1-y2)
    c = math.sqrt(a+b)
    return c

def FindPerpInters(m1,c1,m2,c2):
    n = m1-m2
    d= c2-c1
    x = d/n
    return x


def get_aim_point(cx1,cy1):
   #global GV.startx,GV.starty,GV.finishx,GV.finishy
    slope = GetSlope(GV.startx,GV.starty,GV.finishx,GV.finishy)
    c = FindC(GV.finishx,GV.finishy,slope)

    #disformline = shortest_distance(cx1,cy1, slope, c)
    if slope ==0:
       slope2 = 20000
    else:
        slope2  = (1/slope)*(-1)
    c2 = FindC( cx1,cy1,  slope2)
    px = FindPerpInters(slope,c,slope2,c2)

    py = slope2*px+c2
    #print(px,py)
    #aimx = movedixXalongline(px,py,7)#modified 13_may_21
    aimx = movedixXalongline(px,py,1)  
    aimy = slope * aimx+c
    #print("AimPoint ",round(aimx,2),round(aimy,2))

    return aimx
    
def movedixXalongline(sx1,sy1,dis):
#    global GV.finishx,GV.finishy
    

    ang = math.atan2((GV.finishy -GV.starty),(GV.finishx-GV.startx))
    newx = sx1+dis*math.cos(ang)
    newy = sy1+dis*math.sin(ang)
    #print(newx,newy)
    
    return newx


def getSteerAngle():
    #global GV.startx,GV.starty,GV.finishx,GV.finishy,GV.currentheader,GV.currentx1,GV.currenty1
    #aimx = get_aim_point(10, 20)
    aimx = get_aim_point(GV.currentx1,GV.currenty1)
    slope = GetSlope(GV.startx,GV.starty,GV.finishx,GV.finishy)
    c = FindC(GV.finishx,GV.finishy,slope)
    aimy = aimx*slope+c
    slopetopoint = GetSlope(GV.currentx1,GV.currenty1,aimx,aimy)
    #ang = math.atan(slopetopoint)
    # ang = math.atan2((aimy-GV.currenty1 ),(aimx-GV.currentx1))  # origional formula
    ang = math.atan2((aimx-GV.currentx1),(aimy-GV.currenty1 ),)    #rotate angle 90 anti clockwore   swop x and y co-ordinates

    ang = round(math.degrees(ang))
 
 
    #ang = round(math.degrees(ang))
    #print("AimAngle ",ang)

    GV.flogtrack.write("'{},".format(ang))

    ang = ang -GV.gogo
    GV.flogtrack.write("'{},{},{},".format(ang,aimx,aimy))

    #print("AimAngle2 ",ang)
  #  if ang > 40:
  #      ang =40
  #  if ang < -40:
  #      ang = -40
    GV.Set_SteerAng = ang



    #drift error compensation section
    angle = math.atan2((aimy-GV.currenty1),(aimx-GV.currentx1))
    angle = GV.CurPathAng - angle
    if angle>0:
           GV.Left = True
    else:
           GV.Left = False



  
def LatLongTM(lat,long):
    p = pyproj.Proj(proj='utm', zone=29, ellps='WGS84')
    x,y = p(lat,long)
    return x,y
