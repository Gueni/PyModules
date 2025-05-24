import RPi.GPIO as GPIO
from time import sleep

gpio_pins = [2,3,6,7,8,9,10,11,12,13,16,17,18,19,20,21]

for gpio_pin in gpio_pins:
    GPIO.setup(gpio_pin, GPIO.OUT)

for x in range(1, 17):
    print(" Testing GPIO :" +" "+ str(x))  
    GPIO.output(gpio_pins[x], GPIO.HIGH)
    sleep(2)
    GPIO.output(gpio_pins[x], GPIO.LOW)
    sleep(2)