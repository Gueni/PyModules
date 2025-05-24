
import os
import socket
import fcntl
import struct
import RPi.GPIO as GPIO
import time
import subprocess

pinNum = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(pinNum,GPIO.OUT)

ifaces = ['eth0','wlan0']
connected = []
i = 0
for ifname in ifaces:
	ssid = os.popen("iwconfig wlan0 \
                | grep 'ESSID' \
                | awk '{print $4}' \
                | awk -F\\\" '{print $2}'").read()
	cmd = "hostname -I | cut -d\' \' -f1"
	IP = subprocess.check_output(cmd, shell = True )
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])
		connected.append(ifname)
		print("%s is connected" % ifname +" to " +"  SSID : " + ssid +"  " +" IP :" +"  "+ IP)
		while True:
			GPIO.output(pinNum,GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(pinNum,GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(pinNum,GPIO.LOW)
			time.sleep(2.0)
	except:
		print("%s is not connected" % ifname)
		GPIO.output(pinNum,GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(pinNum,GPIO.LOW)
		time.sleep(0.1)
		i += 1
print(connected)