import RPi.GPIO as GPIO 
import time

a=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)

while a:
	if GPIO.input(17):  #zero counter
		print ("17 is open")        
	else:
		print ("17 is closed") 
	if GPIO.input(27):  
		print ("27 is open")
	else:
		print("27 is closed")
	time.sleep(1)
	
