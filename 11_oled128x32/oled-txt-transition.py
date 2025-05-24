

import os
import math
import time
import subprocess                 
from time import sleep
from smbus import SMBus 
from lib_oled96 import ssd1306
from PIL import ImageFont, ImageDraw, Image

i2cbus = SMBus(1)
oled = ssd1306(i2cbus)
draw = oled.canvas   
padding = 2
shape_width = 20
top = padding
bottom = oled.height - padding - 1
x = padding
oled.display()
font = ImageFont.truetype('FreeMono.ttf', 14)

while True:
        ipaddress = os.popen("ifconfig wlan0 \
                            | grep 'inet addr' \
                            | awk -F: '{print $2}' \
                            | awk '{print $1}'").read()
        ssid = os.popen("iwconfig wlan0 \
                        | grep 'ESSID' \
                        | awk '{print $4}' \
                        | awk -F\\\" '{print $2}'").read()
        ipaddresseth = os.popen("ifconfig eth0 \
                            | grep 'inet addr' \
                            | awk -F: '{print $2}' \
                            | awk '{print $1}'").read()
        ssideth = os.popen("iwconfig eth0 \
                        | grep 'ESSID' \
                        | awk '{print $4}' \
                        | awk -F\\\" '{print $2}'").read()
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=255, fill=1)
        oled.display()
        sleep(3)
        logo = Image.open('pi_logo.png')
        draw.bitmap((32, 0), logo, fill=0)
        oled.display()
        sleep(4)
        oled.cls()
        sleep(3)
        font = ImageFont.truetype('FreeMono.ttf', 14)
        draw.text((x+5, top+20), 'TIMEBOX 4.0', font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.text((x, top), "ssid: ", font=font, fill=1)
        draw.text((x, top+30), str(ssid), font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.text((x, top), "IP: ", font=font, fill=1)
        draw.text((x, top+30), str(IP), font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.text((x, top+30), str(CPU), font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.text((x, top+30), str(MemUsage), font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.text((x, top+30), str(Disk), font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.text((x, top), "ipaddresseth: ", font=font, fill=1)
        draw.text((x, top+30), str(ipaddresseth), font=font, fill=1)
        oled.display()
        sleep(4)
        oled.cls()
        draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=255, fill=1)
        oled.display()
        sleep(3)