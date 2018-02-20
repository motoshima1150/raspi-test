import wiringpi as pi
import time
from isl29125 import isl29125

isl29125_addr = 0x44

pi.wiringPiSetupGpio()
i2c = pi.I2C()
color = isl29125( i2c, isl29125_addr )

while True:
    red = color.read_red()
    green = color.read_green()
    blue = color.read_blue()
    
    print( "Red:", red, " Green:", green, " Blue:", blue )
    time.sleep(1)
