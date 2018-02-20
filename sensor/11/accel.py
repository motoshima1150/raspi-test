import wiringpi as pi
from lis3dh import lis3dh
import time

SPI_CS = 0

SPI_SPEED = 100000

pi.wiringPiSPISetup (SPI_CS, SPI_SPEED)

accel = lis3dh( SPI_CS )

while True:
    ( x, y, z ) = accel.read_accel()
    print ("x:", x, "  y:", y, "  z:", z)

    ( x_angle, y_angle ) = accel.conv_angle( x, y, z )
    print ("X Angle:", x_angle , " Y Angle:", y_angle )    

    time.sleep(1)
