

import serial
import time
timestr = time.strftime("%Y%m%d-%H%M")

SerialPort_On = True
startx =5.0
starty =5.0
finishx =200.0
finishy =10.0
currentx1 =2.0
currenty1 =2.0
CurrentHeader =0
Set_SteerAng =5.0
Simstopstart = 1.0
Steerangle = 0
gogo = 0
PointX = []
PointY = []
filename  = timestr+"_logtrack.csv"
flogtrack= open(filename,"w+")
Qual =0
GV.dist = 0
#next section for to compensate for error drift
ErrDist =[0,0,0,0,0,0,0,0,0,0]
CurPathAng = 0
Left = False



    
